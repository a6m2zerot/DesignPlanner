from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth.models import User
from planner.models import PasswordToRecover
from django.db import IntegrityError
from django.urls import reverse
import random
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime, timedelta

# Здесь генерируем пароль
def password_generator():
    passgen = ''
    for i in range(0, 6):
        passgen += str(random.randint(0, 9))
    return passgen


def login_func(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'login.html', {'form': form, 'message': 'Пароль неверный. Попробуйте еще раз'})
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_func(request):
    logout(request)
    return redirect("login_func")


def register_func(request):
    if request.method == "POST":
        check_email=request.POST['email']
        if User.objects.filter(email=check_email).exists():
            return render(request, "register.html", {"form": UserRegistrationForm, 
                                                    "message": "Пользователь с таким email уже существует. Пожалуйста, попробуйте другой почтовый ящик"})
        else:
            if request.POST["password1"] == request.POST["password2"]:
                try:
                    user = User.objects.create_user(username=request.POST["username"], email=request.POST['email'], password=request.POST["password1"])
                    user.save()
                    login(request, user)
                    return redirect("home")
                except IntegrityError:
                    return render(request, "register.html",
                                {"form": UserRegistrationForm, "error": "Такой пользователь уже существует"})
            else:
                return render(request, "register.html", {"form": UserRegistrationForm, "error": "Пароли не совпадают"})

    return render(request, "register.html", {"form": UserRegistrationForm})


def recover_password(request):
    return render(request, 'recover_password.html')

def send_password(request):
    if request.method == "POST":
        user_email = request.POST['sendEmail']
        
        if User.objects.filter(email=user_email).exists():
            a = User.objects.get(email=user_email)
            password_to_send = password_generator()
            if PasswordToRecover.objects.filter(user_id=a.id).exists():
                PasswordToRecover.objects.filter(user_id=a.id).update(password_to_send=password_to_send, time_of_gen_password=timezone.now())
            else:
                PasswordToRecover.objects.create(user_id=a.id, password_to_send=password_to_send)
            
            subject = 'Восстановление пароля от DesignPlanner'
            message = f'Восстановление пароля для логина {a.username}. Пожалуйста, введите этот пароль в окно восстановления пароля на сайте DesignPlanner: {password_to_send}. Срок действия пароля - 15 минут.'
            from_email = 'a6m2zerot@gmail.com'
            recipient_list = [user_email]
            send_mail(subject, message, from_email, recipient_list)
            return render(request, "input_password.html")
        return render(request, "register.html", {"form": UserRegistrationForm})

def check_password(request):
    if request.method == "POST":
        entered_email = request.POST['entered_email']
        entered_password = request.POST['entered_password']

        if User.objects.filter(email=entered_email).exists():
            a = User.objects.get(email=entered_email)

            #Если прошло более 15 минут с момента генерации вспомогательного пароля (ф-ия password_generator()) на восстановление основного и он был введен позже, то такой пароль невалиден.
            current_time = timezone.now()
            b = PasswordToRecover.objects.get(user_id=a.id)
            time_difference = current_time - b.time_of_gen_password
            if time_difference > timedelta(minutes=15):
                return render(request, 'recover_password.html', {'message': "аролю больше 15 минут. Он более не действителен. Начните процедуру восттановления заново."})
            if PasswordToRecover.objects.filter(user_id=a.id, password_to_send=entered_password).exists():
                return render(request, 'enter_new_password.html', {'user_id': a.id})
            else:
                return render(request, 'recover_password.html', {'message': "Либо пароль не совпадает, либо почта указана неверно. Доступ закрыт. Попробуйте еще"})
        else:
            return render(request, 'recover_password.html', {'message': "Такой почты не существует. Проверьте правильность ввода почты"})


def check_users_passwords(request, user_id):
    if request.method == "POST":
        entered_pass_1 = request.POST['new_pass_1']
        entered_pass_2 = request.POST['new_pass_2']
        if entered_pass_1 == entered_pass_2:
            user = User.objects.get(id=user_id)
            user.set_password(entered_pass_1) 
            user.save()
            return redirect("login_func")
        else:
            render (request, 'enter_new_password.html', {'message': 'Пароли не совпадают. Попробуйте еще раз'}, {'user_id': user_id})
