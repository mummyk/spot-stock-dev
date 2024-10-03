from functools import wraps
from django.http import HttpRequest
from django.core.exceptions import PermissionDenied


def permissions_required(*permission_codenames):
    """ Check if the user has the required permissions """
    def decorator(func):
        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            # Check if the user has all the required permissions
            if not all(request.user.has_perm(codename) for codename in permission_codenames):
                raise PermissionDenied(
                    "You do not have the required permissions to perform this action.")

            return func(request, *args, **kwargs)
        return wrapper
    return decorator


# def permissions_required(*permission_codenames):
    # """ Check if the user has the required permissions """
    # def decorator(func):
    #     @wraps(func)
    #     def wrapper(request: HttpRequest, *args, **kwargs):
    #         # Check if the user has all the required permissions
    #         if not all(request.user.has_perm(codename) for codename in permission_codenames):
    #             raise HttpError(
    #                 403, "You do not have the required permissions to perform this action.")

    #         return func(request, *args, **kwargs)
    #     return wrapper
    # return decorator
