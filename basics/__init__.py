from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
my_session_factory = UnencryptedCookieSessionFactoryConfig('mysession')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(session_factory = my_session_factory,settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
