# Third Party Stuff
from pyramid.security import ALL_PERMISSIONS, Allow, Authenticated, Everyone

# IMAX Stuff
# from xamcheck_operations.constants.user_groups import APPS_FOR_EACH_GROUP
from polls.models.auth import User


SUPERUSER_PRINCIPAL = 'user_attribute:is_superuser'

# Permissions
SUPERUSER_PERMISSION = 'superuser_permission'


def get_principal_indentifiers(user_id, request):
    user = User.get_by_id(user_id)

    if user is None or not user.is_active:
        return

    principals = []

    if user.is_superuser:
        principals.append(SUPERUSER_PRINCIPAL)

    return principals


class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'everyone'),
        (Allow, Authenticated, 'authenticated'),
        (Allow, SUPERUSER_PRINCIPAL, ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request


# CSRF Exmpetion

__CSRF_EXEMPTED_ROUTES = set()


def exempt_csrf(route_name):
    __CSRF_EXEMPTED_ROUTES.add(route_name)


def csrf_is_exempted_for_route(route_name):
    return route_name in __CSRF_EXEMPTED_ROUTES
