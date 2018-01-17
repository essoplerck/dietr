from functools import wraps

from flask import session, redirect, request, url_for


def login_required(action):
    '''Decorator for the login required method. This decorator will check if the
    user is logged in. If not it will redirect to the login page.
    '''
    @wraps(action)
    def login_decorator(*arg, **kwargs):
        # Check if user is logged in
        if 'user' in session:
            return action(*arg, **kwargs)
        return redirect(url_for('authentication.login', next=request.url))
    return login_decorator

def singleton(cls):
    instances = {}

    @wraps(cls)
    def singleton_decorator(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return singleton_decorator
