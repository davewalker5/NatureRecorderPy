from functools import wraps
from flask import abort
from flask_login import current_user


def has_roles(roles):
    """
    Return true if the current user has one of the roles in the supplied list

    :param roles: List of role names
    :return: True if the user has one of the roles, False if not
    """
    user_has_roles = False
    if current_user.is_authenticated:
        matching_roles = [r for r in current_user.roles if r.name in roles]
        user_has_roles = len(matching_roles) > 0

    return user_has_roles


def membership():
    """
    Return a tuple of booleans indicating user role membership

    :return: Tuple of booleans indicating Administrator, Reporter and Reader membership, in that order
    """
    is_admin = has_roles(["Administrator"])
    is_reporter = has_roles(["Reporter"])
    is_reader = has_roles(["Reader"])
    return is_admin, is_reporter, is_reader


def requires_roles(roles):
    """
    Decorator to confirm the current user has one of the roles in the supplied list

    :param roles: List of role names
    :return: Decorator function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check for matches between the user's roles and the role list. If there
            # are none, return a 401
            if not has_roles(roles):
                return abort(401)

            return f(*args, **kwargs)

        return decorated_function

    return decorator
