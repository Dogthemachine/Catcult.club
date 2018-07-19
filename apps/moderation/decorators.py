from functools import wraps

from django.shortcuts import redirect


def user_is_admin():
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            if not str(request.user) == 'admin':
                return redirect('/')
            else:
                return func(request, *args, **kwargs)

        return wraps(func)(inner_decorator)

    return decorator