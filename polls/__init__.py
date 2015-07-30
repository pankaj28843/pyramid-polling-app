from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from polls.models.meta.base import (
    Base,
    DBSession
)
from polls.settings import MEDIA_ROOT
from polls.settings.database import get_db_engine
from polls.settings.redis import get_redis_url
from polls.settings.security import AUTH_SECRET
from polls.security import (
    get_principal_indentifiers,
    RootFactory,
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = get_db_engine()
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    authentication_policy = AuthTktAuthenticationPolicy(
        AUTH_SECRET,
        callback=get_principal_indentifiers,
    )
    authorization_policy = ACLAuthorizationPolicy()

    config = Configurator(
        settings=settings,
        authentication_policy=authentication_policy,
        authorization_policy=authorization_policy,
        root_factory=RootFactory,
    )

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view(name='media', path=MEDIA_ROOT, cache_max_age=3600)

    # Update redis.sessions.url
    config.registry.settings['redis.sessions.url'] = get_redis_url()

    # Add .html extension as a renderer
    config.add_jinja2_renderer('.html')

    # Scan views for route configuration
    config.include('polls.views.polls')
    config.include('polls.views.auth')

    config.scan()

    return config.make_wsgi_app()
