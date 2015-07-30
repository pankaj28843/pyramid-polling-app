# -*- coding: utf-8 -*-
from __future__ import absolute_import

from pyramid.httpexceptions import HTTPForbidden, HTTPFound
from pyramid.view import forbidden_view_config, view_config
from pyramid.security import (
    authenticated_userid,
    forget,
    remember,
    unauthenticated_userid
)

from polls.models.auth import User


def get_authenticated_user(request):
    '''
    This function is used to attach user object to current request
    '''
    userid = unauthenticated_userid(request)

    if userid is not None:
        # this should return None if the user doesn't exist
        # in the database
        return User.get_by_id(userid)


def includeme(config):
    config.add_request_method(get_authenticated_user, 'user', reify=True)
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')


@forbidden_view_config()
def forbidden_view(request):
    # do not allow a user to login if they are already logged in
    if authenticated_userid(request):
        return HTTPForbidden()

    loc = request.route_url('login', _query=(('next', request.path),))
    return HTTPFound(location=loc)


@view_config(
    route_name='login',
    renderer='auth/login.html',
)
def login_view(request):

    next = request.params.get('next') or request.route_url('home')
    context = {}

    if request.method == "POST":
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        context.update(email=email)

        user = User.get(email=email).first()
        if user:
            if user.check_password(password):
                if user.is_active is True:
                    headers = remember(request, user.id)
                    return HTTPFound(location=next, headers=headers)
                else:
                    context.update(inactive_user=True)
            else:
                context.update(invalid_password=True)
        else:
            context.update(invalid_email=True)

    context.update({
        'next': next,
    })
    return context


@view_config(
    route_name='logout',
)
def logout_view(request):
    headers = forget(request)
    request.session.invalidate()

    loc = request.route_url('home')
    return HTTPFound(location=loc, headers=headers)
