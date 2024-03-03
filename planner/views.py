from django.shortcuts import render, redirect
from .models import Project, MultipleImages, Task, Subtask, Meetings
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from .forms import TaskForm, SubtaskForm, MeetingsForm, ProjectForm
from django.utils import timezone


def check_meeting_status(): # Проверяем статусы встреч active/completed.
    current_time = timezone.now().replace(second=0, microsecond=0).timestamp()
    active_meetings = Meetings.objects.filter(meeting_status = "active")
    for elem in active_meetings:
        if elem.meeting_time_start.timestamp() - current_time <= 0:
            elem.meeting_status = "completed"
            elem.save()


def home(request):
    check_meeting_status()
    data_projects = {
        'active_projects': Project.objects.filter(user=request.user, project_status='active'),
        'completed_projects': Project.objects.filter(user=request.user, project_status='completed'),
    }
    return render(request, 'home.html', data_projects)


def creation_form(request):
    check_meeting_status()
    return render(request, 'create_project.html')


def create_new_project(request):
    check_meeting_status()
    if request.method == "POST":
        project = Project()
        project.project_name = request.POST['project_name']
        project.description = request.POST['description']
    # для лого
        try:
            project.logo = request.FILES['logo']
        except: 
            project.logo = 'null'

        project.user = request.user
        project.save()
        return redirect("home")
    else:
       return render(request, 'home.html')

# смена названия проекта
def change_project(request, project_id):
    check_meeting_status()    
    if request.method == 'GET':
        project_name = Project.objects.get(id=project_id)
        context = {
            'form' : ProjectForm(instance=project_name),
            'project_name': project_name,
        }
        return render(request, 'change_project.html', context)
    else:
        try: #Проверка на загрузку нового лого по проекту
            new_logo = request.FILES['new_logo']
            Project.objects.get(id=project_id).logo.delete()
            Project.objects.get(id=project_id).logo.save(new_logo.name, new_logo, save=True)
        except:
            pass

        project_name = Project.objects.get(id=project_id)
        form = ProjectForm(request.POST, instance=project_name)
        form.save()
        return redirect('go_to_project', id=project_id)


def finish_project(request, id):
    check_meeting_status()
    Project.objects.filter(id=id).update(project_status='completed')
    return redirect('home')

def recover_project(request, id):
    check_meeting_status()
    Project.objects.filter(id=id).update(project_status='active')
    return redirect('home')

def delete_project(request, id):
    check_meeting_status()
    if Project.objects.get(id=id).logo:
        Project.objects.get(id=id).logo.delete(save=True)
        
    try:
        MultipleImages.objects.get(id=id).images.delete(save=True)
    except:
        pass

    Project.objects.get(id=id).delete()
    return redirect('home')


def go_to_project(request, id):
    check_meeting_status()
    data = {
        'info': Project.objects.get(id=id),
        'a': MultipleImages.objects.filter(img_id=id),
        'task_result_active':Task.objects.filter(project_id=id, task_status='active'),
        'task_result_completed': Task.objects.filter(project_id=id, task_status='completed'),
        'meetings_result_active': Meetings.objects.filter(project_id=id, meeting_status='active'),
        'meetings_result_completed': Meetings.objects.filter(project_id=id, meeting_status='completed'),
    }

    return render(request, 'go_to_project.html', data)


# Функция добавления фотографий (сразу для нескольких) 
def add_photos(request, info_id):
    check_meeting_status()
    if request.method == "POST":
        photos = request.FILES.getlist('images')
        for photo in photos:
            stuff = MultipleImages()
            stuff.images = photo
            stuff.img_id = info_id
            stuff.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'], )
    else:
       return redirect('home')


# Данная функция обрабатывает задачу и подзадачи
def push_data(request, info_id, counter):
    check_meeting_status()
    if request.method == 'POST':
        taskname = request.POST['taskname']
        deadline = request.POST['deadline']
        array = []
        for i in range(counter):
            d = []
            item = request.POST.get(f'subtaskname_{i + 1}', False)
            d.append(item)
            array.append(d)
        
        element = Task.objects.create(task=taskname, project_id=info_id, deadline=deadline)
        element.save()

        for k in array:
            el = Subtask.objects.create(subtask=k[0], tasks_id=element.id)
            el.save()
                
        return redirect('go_to_project', id=info_id)


# Данная функция обрабатывает встречи
def func_meeting(request, info_id):
    check_meeting_status()
    if request.method == 'POST':
        meeting_name = request.POST['meeting_name']
        meeting_time_start = request.POST['meeting_time_start']
        meeting_time_finish = request.POST['meeting_time_finish']
        meeting_notes = request.POST['meeting_notes']

        element = Meetings.objects.create(meeting_name=meeting_name, 
                                        meeting_time_start=meeting_time_start,
                                        meeting_time_finish=meeting_time_finish,
                                        meeting_notes=meeting_notes,
                                        project_id=info_id)
        element.save()
        return redirect('go_to_project', id=info_id)

def change_meeting(request, meeting_id):
    check_meeting_status()    
    if request.method == 'GET':
        meeting_name = Meetings.objects.get(id=meeting_id)
        context = {
            'form' : MeetingsForm(instance=meeting_name),
            'meeting': meeting_name,
        }
        return render(request, 'change_meeting.html', context)
    else:
        meeting_name = Meetings.objects.get(id=meeting_id)
        project_id = meeting_name.project_id
        form = MeetingsForm(request.POST, instance=meeting_name)
        form.save()
        return redirect('go_to_project', id=project_id)

def delete_meeting(request, meeting_id):
    check_meeting_status()
    if request.method == 'GET':
        meeting = Meetings.objects.get(id=meeting_id)
        meeting.delete()
        project_id = meeting.project_id
        return redirect('go_to_project', id=project_id)


def recover_meeting(request, meeting_id):
    print(meeting_id, 'meeting_id')
    check_meeting_status()
    if request.method == 'GET':
        meeting_name = Meetings.objects.get(id=meeting_id)
        context = {
            'form' : MeetingsForm(instance=meeting_name),
            'meeting': meeting_name,
            #'notes': Meetings.objects.get(id=meeting_id).meeting_notes,  - не применять, т.к. работает forms.py
            #'name': Meetings.objects.get(id=meeting_id),   - не применять, т.к. работает forms.py
        }
        return render(request, 'recover_meeting.html', context)
    else:
        meeting = Meetings.objects.get(id=meeting_id)
        project_id = meeting.project_id

        meeting_name = request.POST['meeting_name']
        meeting_time_start = request.POST['meeting_time_start']
        meeting_time_finish = request.POST['meeting_time_finish']
        meeting_notes = request.POST['meeting_notes']

        element = Meetings.objects.get(id=meeting_id)
        element.meeting_name = meeting_name
        element.meeting_time_start = meeting_time_start
        element.meeting_time_finish = meeting_time_finish
        element.meeting_notes = meeting_notes
        element.meeting_status = 'active'
        element.save()
        return redirect('go_to_project', id=project_id)


def return_task(request, task_id):
    check_meeting_status()
    if request.method == 'GET':
        task = Task.objects.get(id=task_id)
        context = {
            'form' : TaskForm(instance=task),
            'task': task
        }
        return render(request, 'change_task.html', context)
    else:
        task = Task.objects.get(id=task_id)
        project_id = task.project_id
        form = TaskForm(request.POST, instance=task)
        form.save()
        return redirect('go_to_project', id=project_id)


def return_subtask(request, task_id, subtask_id):
    check_meeting_status()
    if request.method == 'GET':
        subtask = Subtask.objects.get(id=subtask_id)
        context = {
            'form' : SubtaskForm(instance=subtask),
            'task': Task.objects.get(id=task_id),
            'subtask': subtask,
        }
        return render(request, 'change_subtask.html', context)
    else:
        subtask = Subtask.objects.get(id=subtask_id)
        task = Task.objects.get(id=task_id)
        project_id = task.project_id
        form = SubtaskForm(request.POST, instance=subtask)
        form.save()
        return redirect('go_to_project', id=project_id)


# Данная функция добавляет подзадачу по id задачи   
def add_subtask_to_task(request, task_id): 
    check_meeting_status()   
    if request.method == 'GET':
        task = Task.objects.get(id=task_id)
        return render(request, 'add_subtask.html', {'task': task})
    else:
        subtaskname = request.POST['subtaskname']
        el = Subtask.objects.create(subtask=subtaskname, tasks_id=task_id)
        el.save()
        task = Task.objects.get(id=task_id)
        project_id = task.project_id
        return redirect('go_to_project', id=project_id)
    

def complete_task(request, task_id):
    check_meeting_status()
    Task.objects.filter(id=task_id).update(task_status='completed', completed_status_date=timezone.now())
    # Принудительно устанавливаем статус всех подзадач на "completed" 
    if len(Subtask.objects.filter(tasks_id=task_id)) > 0:
        Subtask.objects.filter(tasks_id=task_id).update(subtask_status='completed', completed_status_date=timezone.now())

    task = Task.objects.get(id=task_id)
    id = task.project_id
    data = {
        'info': Project.objects.get(id=id),
        'a': MultipleImages.objects.filter(img_id=id),
        'task_result_active':Task.objects.filter(project_id=id, task_status='active'),
        'task_result_completed': Task.objects.filter(project_id=id, task_status='completed'),
        'meetings_result_active': Meetings.objects.filter(project_id=id, meeting_status='active'),
        'meetings_result_completed': Meetings.objects.filter(project_id=id, meeting_status='completed'),
    }

    return render(request, 'go_to_project.html', data)
    

def complete_subtask(request, task_id, subtask_id):
    check_meeting_status()
    Subtask.objects.filter(id=subtask_id, subtask_status='active').update(subtask_status='completed', completed_status_date=timezone.now())

    #Проверка статусы подзадач: если все(!) подзадачи completed, то статус задачи тожк меняется на completed
    check_status = Subtask.objects.filter(tasks_id=task_id)
    counter = 0
    total_length = len(check_status)
    for elem in check_status:
        if 'completed' == elem.subtask_status:
            counter = counter + 1
    if counter == total_length and total_length > 0:      
        Task.objects.filter(id=task_id).update(task_status='completed', completed_status_date=timezone.now())
    else:
        Task.objects.filter(id=task_id).update(task_status='active')

    task = Task.objects.get(id=task_id)
    id = task.project_id
    data = {
        'info': Project.objects.get(id=id),
        'a': MultipleImages.objects.filter(img_id=id),
        'task_result_active':Task.objects.filter(project_id=id, task_status='active'),
        'task_result_completed': Task.objects.filter(project_id=id, task_status='completed'),
        'meetings_result_active': Meetings.objects.filter(project_id=id, meeting_status='active'),
        'meetings_result_completed': Meetings.objects.filter(project_id=id, meeting_status='completed'),
    }

    return render(request, 'go_to_project.html', data)
 

def delete_task(request, task_id):
    check_meeting_status()
    task = Task.objects.get(id=task_id)
    project_id = task.project_id
    task.delete()
    return redirect('go_to_project', id=project_id)


def delete_subtask(request, task_id, subtask_id):
    check_meeting_status()
    subtask = Subtask.objects.get(id=subtask_id)
    task = Task.objects.get(id=task_id)
    project_id = task.project_id
    subtask.delete()
    return redirect('go_to_project', id=project_id)






    