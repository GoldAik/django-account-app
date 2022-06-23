from loginsystem.settings import EMAIL_HOST_USER

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail

from .tokens import account_activation_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth import get_user_model
User = get_user_model()

def username_from_login(login):
    username = login

    if '@' in login:     # only because validate username without '@'
        email = login
        username = User.objects.filter(email__iexact=email).first().username

    return username


def send_verification_email(request, user):

    to_email = user.email

    mail_subject = 'Verify your email.'
    message = render_to_string('emails/email_verification_template.html', {
            'user': user,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        }
    )
    send_mail(mail_subject, message, EMAIL_HOST_USER, [to_email])


def check_verification_url(uidb64, token, type: PasswordResetTokenGenerator = account_activation_token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and type.check_token(user, token):
        return user
    else:
        return None


def send_email_recover_password(request, user):

    to_email = user.email

    mail_subject = 'Recover your password.'
    message = render_to_string('emails/email_recover_password.html', {
            'user': user,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user)
        }
    )
    send_mail(mail_subject, message, EMAIL_HOST_USER, [to_email])