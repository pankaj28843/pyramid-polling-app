# Standard Library
import os

# Third Party Stuff
from sqlalchemy import create_engine

# string format for connection url
CONNECTION_URL_FMT = 'postgresql://{user}:{password}@{host}:{port}/{name}'


def get_db_connection_dict_from_env():
    """
    Build a dict of connection arguments from the environment.

    :return:
    """
    # get settings from envornment variables
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')

    return dict(
        name=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )


def get_db_connection_url():
    """
    Return database connection URL.
    It's used by sqlalchemy.
    """
    # get database connection settings as a dictionary
    db_kwargs = get_db_connection_dict_from_env()

    # create connection url using format and db_kwargs
    connection_url = CONNECTION_URL_FMT.format(**db_kwargs)

    return connection_url


def get_db_engine():
    """
    Create the database engine connection
    and attempt to use the database mypyramidproject,
    if it doesn't exist, create it, then use it.

    :return: A database engine.
    """
    # get database connection url
    connection_url = get_db_connection_url()

    # Create engine from connection url
    engine = create_engine(connection_url)

    return engine
