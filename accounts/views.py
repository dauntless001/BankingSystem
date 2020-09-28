from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import LoginForm, RegisterForm, UserForm, AccountEditForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import User
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from .forms import ContactForm

# Create your views here.
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('accounts:dashboard')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    name = 'change_password.html'
    context = {
        'form':form
    }
    return render(request, name, context)
    


def welcome_view(request):
    name = 'welcome.html'
    return render(request, name)


def profile_view(request):
    user = request.user
    name = 'profile.html'
    context = {
        'user':user
    }
    return render(request, name)

def dashboard(request):
    user = request.user
    name = 'dashboard.html'
    context = {
        'user':user
    }
    return render(request, name)


def logout_view(request):
    logout(request)
    return redirect('welcome')

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'Welcome Back {request.user.username}')
                return redirect('accounts:dashboard')
            else:
                messages.success(request, f'Sorry, Account has been deactivated')
                return redirect('welcome')
    name = 'login.html'
    context = {
        'form' : form
    }
    return render(request, name, context)


User = get_user_model()
def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        new_user = User.objects.create_user(username=username, email=email,
        first_name=first_name, last_name=last_name, password=password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'Welcome {request.user.username} 60% of your profile has been completed. Try Updating')
                return redirect('accounts:dashboard')
            else:
                messages.success(request, f'Sorry, Account has been deactivated')
                return redirect('welcome')
        return redirect('welcome')
    name = 'login.html'
    context = {
        'form' : form
    }
    return render(request, name, context)


def userList(request):
    qs = User.objects.all()
    name = 'users.html'
    context = {
        'qs':qs
    }
    return render(request, name, context)


def profile_editview(request):
    user_f = UserForm(request.POST or None, instance=request.user)
    acc_f = AccountEditForm(request.POST or None, request.FILES or None, instance=request.user.account)
    if user_f.is_valid and acc_f.is_valid():
        user_f.save()
        acc_f.save()
        return redirect('accounts:dashboard')
    name = 'profileedit.html'
    context = {
        'user_f':user_f,
        'acc_f':acc_f
    }
    return render(request, name, context)


def report_view(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(request.user.email)
        print(form.cleaned_data['subject'])
        try:
            send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['message'],
                request.user.email,
                ['suntopmultimedia@gmail.com'],
                fail_silently=False,
            )
        except:
            messages.info(request, 'Error sending Message, Please check connection and try again')
            return redirect('accounts:report')
    name = 'change_password.html'
    context = {
        'form' : form
    }
    return render(request, name, context)