# Standard Library
import os

# Third Party Stuff
from sqlalchemy import create_engine


def get_db_connection_url():
    """
    Return database connection URL.
    It's used by sqlalchemy.
    """
    return os.environ["DATABASE_URL"]


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
