from __future__ import with_statement
from alembic import context
from logging.config import fileConfig
from polls.settings.database import (
    get_db_connection_url,
    get_db_engine
)
from polls.models.meta.base import (
    Base,
    DBSession
)


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


# Get sqlalchemy database engine from settings
db_engine = get_db_engine()

# Bind newly created engine to DBSession
DBSession.configure(bind=db_engine)

# Bind base model with database
Base.metadata.bind = db_engine


# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Importing all the models so that alembic montors them
# TODO - this is not the best way to do this
from polls.models.auth import *


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_db_connection_url()
    context.configure(url=url, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = get_db_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
