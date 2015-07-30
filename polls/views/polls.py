# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config

from polls.settings import STATIC_ROOT


def includeme(config):
    config.add_route('home', '/')
    config.add_route('robots.txt', '/robots.txt')


@view_config(
    route_name='home',
    renderer='home.html',
    permission='authenticated'
)
def home_view(request):

    return {

    }


@view_config(
    route_name='robots.txt',
)
def robots_txt_view(request):

    robots_txt_filepath = os.path.normpath(os.path.join(
        STATIC_ROOT,
        'robots.txt'
    ))

    with open(robots_txt_filepath, 'r') as f:
        response_body = f.read()

    return Response(
        content_type='text/plain',
        body=response_body,
    )
