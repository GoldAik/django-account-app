# Account App in Django

## Project Description
This project is a Django application implementing a custom user that allows login using both username and email. The project includes registration, login, redirects for unauthorized users, email verification after registration, and account recovery in case of a forgotten password.

The project uses an SQLite database (by default).

> **Note:** The project serves solely as an inspiration source and is not intended for production use. It does not include automated tests, which may affect stability and security in a production environment.

## Features
- Login using username or email
- User registration with email verification
- Sending verification email
- Redirects for unauthenticated users
- Account recovery (password reset) via email with a link containing a code
- Session management and authentication
- Extended custom user model

## Technologies
- Django
- Python
- SQLite (by default)

## Installation and Setup

1. **Clone the repository**
```bash
  git clone https://github.com/GoldAik/django-account-app.git
  cd django-account-app
  git checkout development
```

2. **Create and activate a virtual environment**

Linux / macOS:
```bash
  python -m venv venv
  source venv/bin/activate
```

Windows:
```bash
  python -m venv venv
  venv\Scripts\activate
```

3. **Install dependencies**

Since three years ago I didn't include a `requirements.txt` file when creating the project, I cannot provide the exact list of used libraries and versions. However, based on my current environment and the Django version I used (`Django==4.0.3`), this version is likely correct. **It’s also possible that other libraries are needed for proper functioning, which I am not aware of.**

To install dependencies, run:

```bash
  pip install -r requirements.txt
```

4. **Configure email settings**

 1. If you are using a provider other than `smtp.gmail.com`, you need to set the appropriate variables in the `loginsystem/settings.py` file:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os_environ.get("EMAIL")
EMAIL_HOST_PASSWORD = os_environ.get("PASSWORD")
```

 2. To set up the email address and password, use environment variables `EMAIL` and `PASSWORD`.

5. **Apply migrations**
```bash
  python manage.py makemigrations
  python manage.py migrate
```

6. **Create a superuser**
```bash
  python manage.py createsuperuser
```

7. **Run the server**
```bash
  python manage.py runserver
```

8. **Visit** `http://127.0.0.1:8000/`

## License

This project is available under the [MIT license](https://choosealicense.com/licenses/mit/). See the [LICENSE](https://github.com/GoldAik/django-account-app/blob/main/LICENSE) file for details.

---