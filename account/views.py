from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required

from django.http.response import Http404

from .forms import RegisterBasicInfoForm, RegisterLoginInfoForm, LoginForm
from .decorators import logout_required, email_verificated

from django.contrib.auth import get_user_model
User = get_user_model()

@email_verificated()
def home(request):
    return render(request, 'account/home.html', {})


@logout_required()
def login(request):
    if int(request.session.get('attempt') or 0) >= 5:
        raise Http404


    form = LoginForm(request.POST or None)

    if form.is_valid():
        login = form.cleaned_data.get('login')
        password = form.cleaned_data.get('password')

        username = login

        if '@' in login:     # only because validate username without '@'s
            email = login
            username = User.objects.filter(email__iexact=email).first().username

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
            redirect('home')

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

    email = request.user.email
    return render(request, 'account/register-verification.html', {"email": email})