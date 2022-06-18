from django.shortcuts import redirect

def logout_required(redirect_url='home'):

    def function_wrapper(view_function):

        def argument_wrapper(request, *args, **kwargs):

            if request.user.is_authenticated:
                return redirect(redirect_url)

            return view_function(request, *args, **kwargs)
        
        return argument_wrapper

    return function_wrapper


def email_verificated(redirect_url='verify-email'):

    def function_wrapper(view_function):

        def argument_wrapper(request, *args, **kwargs):

            if request.user.is_authenticated:
                user = request.user
                if not user.is_email_verified:
                    return redirect(redirect_url)

            return view_function(request, *args, **kwargs)
        
        return argument_wrapper

    return function_wrapper