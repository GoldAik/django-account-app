from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required

from django.http.response import Http404

from .forms import RegisterBasicInfoForm, RegisterLoginInfoForm, LoginForm, RecoverPasswordEmailForm, RecoverPasswordNewPassword
from .decorators import logout_required, email_verificated
from .auth import username_from_login, send_verification_email, check_verification_url, send_email_recover_password, default_token_generator

from django.contrib.auth import get_user_model
User = get_user_model()

@email_verificated()
def home(request):
    return render(request, 'account/home.html', {})


@logout_required()
def login(request):
    if int(request.session.get('attempt') or 0) >= 5:
        # raise Http404
        pass


    form = LoginForm(request.POST or None)

    if form.is_valid():
        login = form.cleaned_data.get('login')
        password = form.cleaned_data.get('password')

        username = username_from_login(login)

        user = authenticate(request, username = username, password = password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')

        else:
            attempt = request.session.get('attempt') or 0
            request.session['attempt'] = attempt + 1

            form.errors['password'] = 'Invalid login or password'

    return render(request, 'account/login.html', {'form': form})


@logout_required()
def register_first_step(request):
    form = RegisterBasicInfoForm(request.POST or request.session.get('first_step_data') or None)
    if form.is_valid() and request.method == "POST":
        request.session['first_step_data'] = form.cleaned_data
        return redirect('register-second-step')

    return render(request, 'account/register-basic-info.html', {"form": form})


@logout_required()
def register_second_step(request):
    if not RegisterBasicInfoForm(request.session.get('first_step_data') or None).is_valid():
        return redirect('register-first-step')


    form = RegisterLoginInfoForm(request.POST or None)
    if form.is_valid():
        data = request.session['first_step_data']

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password2')

        data = data | {'username': username, 'password': password}

        try:
            user = User.objects.create_user(**data)
        except Exception as e:
            raise Http404
            
        if user:
            auth_login(request, user)
            return redirect('home')

    return render(request, 'account/register-login-info.html', {"form": form})


@logout_required()
def register(request):
    return redirect('register-first-step')


def logout(request):
    auth_logout(request)
    return redirect('login')


def email_verify(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.user.is_email_verified:
        return redirect('home')

    send_verification_email(request, request.user)

    email = request.user.email
    return render(request, 'account/register-verification.html', {"email": email})


def verification_email(request, uidb64, token):
    user = check_verification_url(uidb64, token)
    if user:
        user.is_email_verified = True
        user.save()
        return redirect('home')
    else:
        return HttpResponse("Invalid")


def recover_password_email(request):
    form = RecoverPasswordEmailForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data.get('email')
        try:
            user = User.objects.filter(email__iexact = email).first()
        except User.DoesNotExist:
            user = None
        
        if user:
            send_email_recover_password(request, user)
            return HttpResponse("Email was sent!")

    return render(request, 'account/recover-password-email.html', {"form": form})


def recover_password_new_password(request, uidb64, token):
    form = RecoverPasswordNewPassword(request.POST or None)

    if form.is_valid():

        user = check_verification_url(uidb64, token, default_token_generator)

        if user:
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            return HttpResponse('Password has been changed <a href="/login/">Login in</a>')
        
        else:
            raise Http404

    return render(request, 'account/recover-password-new-password.html', {"form": form})