from click import password_option
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import CustomUser
from .forms import RegisterBasicInfoForm, RegisterLoginInfoForm
from .decorators import logout_required, email_verificated

# Create your views here.

@email_verificated()
def home(request):
    return render(request, 'account/home.html', {})


@logout_required()
def login(request):

    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')

        username = login

        if '@' in login:     # only because validate username without '@'s
            email = login
            username = CustomUser.objects.filter(email__iexact=email).first().username

        user = authenticate(request, username = username, password = password)

        if user:
            auth_login(request, user)
            return redirect('home')
        else:
            pass

    return render(request, 'account/login.html', {})


@logout_required()
def register(request):
    form = RegisterBasicInfoForm()


    print(request.session.get('email'))
    print(request.session.get('first_name'))
    print(request.session.get('last_name'))

    # # # # # # # # #    STEP 3    # # # # # # # # #

    if request.session.get('waiting_for_verification'):
        email = request.session.get('email')
        return render(request, 'account/register-verification.html', {"email": email})


    # # # # # # # # #    STEP 1    # # # # # # # # #
    
    if request.method == 'POST' and request.POST.get('register_first_step'):
        form = RegisterBasicInfoForm(request.POST)
        if form.is_valid():

            request.session['email'] = form.cleaned_data.get('email')
            request.session['first_name'] = form.cleaned_data.get('first_name')
            request.session['last_name'] = form.cleaned_data.get('last_name')

            form = RegisterLoginInfoForm()
            return render(request, 'account/register-login-info.html', {'form': form})

        else:
            errors = form.errors
            return render(request, 'account/register-basic-info.html', {'form': form, 'errors': errors})

    # if request.session['email']:
    #     form = RegisterLoginInfoForm()
    #     return render(request, 'account/register-login-info.html', {'form': form})


    # # # # # # # # #    STEP 2    # # # # # # # # #

    if request.method == 'POST' and request.POST.get('register_second_step'):
        form = RegisterLoginInfoForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password2')

            email = request.session['email']
            first_name = request.session['first_name']
            last_name = request.session['last_name']

            request.session['first_name'] = None
            request.session['last_name'] = None

            user: CustomUser

            try:
                user = CustomUser.objects.create_user(
                    username = username,
                    password = password,
                    email = email,
                    first_name = first_name,
                    last_name = last_name
                )
                auth_login(request, user)
            except Exception as e:
                print(e)

            if user:
                auth_login(request, user)

            return render(request, 'account/register-verification.html', {"email": email})

        else:
            return render(request, 'account/register-login-info.html', {'form': form})



    # # # # # # # # #    DEFAULT    # # # # # # # # #

    context = {'form': form}
    return render(request, 'account/register-basic-info.html', context)


def logout(request):
    auth_logout(request)
    return redirect('home')


def email_verify(request):
    if not request.user.is_authenticated:
        return redirect('home')

    email = request.user.email
    return render(request, 'account/register-verification.html', {"email": email})