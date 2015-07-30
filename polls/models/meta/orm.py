# Third Party Stuff
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship


def many_to_one(clsname, **kw):
    """Use an event to build a many-to-one relationship on a class.

    This makes use of the :meth:`.References._reference_table` method
    to generate a full foreign key relationship to the remote table.

    """
    @declared_attr
    def m2o(cls):
        cls._references((cls.__name__, clsname))
        return relationship(clsname, **kw)
    return m2o


def one_to_many(clsname, **kw):
    """Use an event to build a one-to-many relationship on a class.

    This makes use of the :meth:`.References._reference_table` method
    to generate a full foreign key relationship from the remote table.

    """
    @declared_attr
    def o2m(cls):
        cls._references((clsname, cls.__name__))
        return relationship(clsname, **kw)
    return o2m
