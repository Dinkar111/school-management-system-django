from django.shortcuts import redirect


def unauthenticated_user(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user_home')
        else:
            return func(request, *args, **kwargs)
    return wrapper


def login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper
