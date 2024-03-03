"""
URL configuration for design_planner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user.views import register_func, login_func, logout_func, recover_password, send_password, check_password, check_users_passwords
from planner.views import home, creation_form, create_new_project, delete_project, go_to_project, add_photos, push_data, return_task, return_subtask, func_meeting, complete_task, complete_subtask, add_subtask_to_task, delete_task, delete_subtask, delete_meeting, change_meeting, change_project, finish_project, recover_project, recover_meeting
from my_calendar.views import new_date, filter_date
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_func, name='login_func'),
    path('logout/', logout_func, name='logout_func'),
    path('register/', register_func, name='register_func'),
    path('creation_form/', creation_form, name='creation_form'),
    path('create_new_project/', create_new_project, name='create_new_project'),
    path('push_data/<int:info_id>/<int:counter>', push_data, name='push_data'),
    path('delete_project/<int:id>', delete_project, name='delete_project'),
    path('go_to_project/<int:id>', go_to_project, name='go_to_project'), 
    path('home/', home, name='home'),
    path('add_photos/<int:info_id>/', add_photos, name='add_photos'),
    path('func_meeting/<int:info_id>', func_meeting, name='func_meeting'),
    path('return_task/<int:task_id>', return_task, name='return_task'),
    path('return_subtask/<int:task_id>/<int:subtask_id>', return_subtask, name='return_subtask'),
    path('add_subtask_to_task/<int:task_id>', add_subtask_to_task, name='add_subtask_to_task'),
    path('delete_task/<int:task_id>', delete_task, name='delete_task'),
    path('complete_task/<int:task_id>', complete_task, name='complete_task'),
    path('complete_subtask/<int:task_id>/<int:subtask_id>', complete_subtask, name='complete_subtask'),
    path('delete_subtask/<int:task_id>/<int:subtask_id>', delete_subtask, name='delete_subtask'),
    path('delete_meeting/<int:meeting_id>', delete_meeting, name='delete_meeting'),
    path('change_meeting/<int:meeting_id>', change_meeting, name='change_meeting'),
    path('recover_meeting/<int:meeting_id>', recover_meeting, name='recover_meeting'),
    path('change_project/<int:project_id>', change_project, name='change_project'),
    path('finish_project/<int:id>', finish_project, name='finish_project'),
    path('recover_project/<int:id>', recover_project, name='recover_project'),
    path('recover_password/', recover_password, name='recover_password'),
    path('send_password/', send_password, name='send_password'),
    path('check_password/', check_password, name='check_password'),
    path('check_users_passwords/<int:user_id>', check_users_passwords, name='check_users_passwords'),

    path('new_date', new_date, name='new_date'),
    path('filter_date', filter_date, name='filter_date'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
