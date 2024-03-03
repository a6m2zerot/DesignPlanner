from django.shortcuts import render
from django.utils import timezone
import calendar
from calendar import monthrange
from time import strptime
from planner.models import Meetings, Task
import datetime
from django.db.models import Q
from planner.views import check_meeting_status # Импорт функции проверки статуса встреч


# Стартовая страница календаря с отображением ТЕКУЩЕГО месяца
def new_date(request):
    check_meeting_status()
    year = timezone.now().year       #  Лучше использовать timezone.now() вместо datetime.now(), так как timezone учитывает часовой пояс и не дает предупреждение: 
    month = timezone.now().month     # 'RuntimeWarning: DateTimeField Subtask.deadline received a naive datetime (2023-09-29 22:40:00) while time zone support is active.'
    year_col = {'January': 31,
                    'February': 28,
                    'March': 31,
                    'April': 30,
                    'May': 31,
                    'June': 30,
                    'July': 31,
                    'August': 31,
                    'September': 30,
                    'October': 31,
                    'November': 30,
                    'December': 31
                    }

    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 : # Проверка года на високосность
        year_col['february'] = 29

    events = Task.objects.filter(
                Q(deadline__month=month) & Q(deadline__year=year)
                                )
                                
    date = datetime.datetime(int(year), month, 1)
    meetings = Meetings.objects.filter(
        Q(meeting_time_start__month=month) & Q(meeting_time_start__year=year)
                                )

    return render(request,'calendar.html', {'year_col': year_col, 
                                            'year': year, 
                                            'month': calendar.month_name[month],
                                            'days_amount': range(1, monthrange(year, month)[1] + 1),
                                            'events': events,
                                            'range': range((date.isoweekday() - 1)),
                                            'meetings': meetings,
                                            })


# Здесь отображается страница с ВЫБРАННЫМ значением месяца и года (calendar.html)
def filter_date(request):
    check_meeting_status()
    if request.method == 'POST':
        year = int(request.POST['year'])
        month = request.POST['month']
        year_col = {'January': 31,
                        'February': 28,
                        'March': 31,
                        'April': 30,
                        'May': 31,
                        'June': 30,
                        'July': 31,
                        'August': 31,
                        'September': 30,
                        'October': 31,
                        'November': 30,
                        'December': 31
                        }

        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 :  # Проверка года на високосность
            year_col['february'] = 29

        month_number = strptime(f'{month}'[:3], '%b').tm_mon # В этой строке получаем НОМЕР месяца для того, чтобы сообщить его в Events.objects.filter()
        events = Task.objects.filter(
                    Q(deadline__month=month_number) & Q(deadline__year=int(year))
                                    )
        meetings = Meetings.objects.filter(
            Q(meeting_time_start__month=month_number) & Q(meeting_time_start__year=int(year))
                                    )
        # А здесь сдвигаем блоки в календаре, чтоб по красоте было
        # Для этого вычислим кол-во блоков-дней предыдущего месяца
        date = datetime.datetime(int(year), month_number, 1)

        return render(request,'calendar.html', {'year_col': year_col, 
                                                'year': year, 
                                                'month': month,
                                                'days_amount': range(1, monthrange(year, month_number)[1] + 1),
                                                'events': events,
                                                'range': range((date.isoweekday() - 1)),
                                                'meetings': meetings,
                                                })



