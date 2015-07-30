# Standard Library
import os


def get_redis_url():
    redis_db_name = os.environ.get('REDIS_NAME')
    redis_host = os.environ.get('REDIS_HOST')
    redis_port = os.environ['REDIS_PORT']

    url = 'redis://{host}:{port}/{name}'.format(
        name=redis_db_name,
        host=redis_host,
        port=redis_port,
    )

    return url
