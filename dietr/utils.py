from functools import wraps

from flask import session, redirect


def login_required(action):
    '''Decorator for the login required method. This decorator will check if the
    user is logged in. If not it will redirect to the login page.
    '''
    @wraps(action)
    def login_decorator(*arg, **kwargs):
        # Check if user is logged in
        if 'user' in session:
            return action(*arg, **kwargs)
        return redirect('/login')
    return login_decorator
