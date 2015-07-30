# -*- coding: utf-8 -*-

# Third Party Stuff
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

from .schema import References, SurrogatePK

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


class BaseModelClass(SurrogatePK, References):
    '''Base model class for all the models.

    Attributes:
        id (Integer): `primary_key` for the table
        created_at (``Arrow`` object): Timestamp of creation
        modified_at (``Arrow`` object): Timestamp of last modification

    .. _Arrow: http://arrow.readthedocs.org/en/latest/
    '''

    @classmethod
    def get_relationships(cls):
        return DBSession.query(cls)._mapper_adapter_map[cls][0].relationships

    @classmethod
    def get_by_id(cls, obj_id):
        '''
        Get object by id for any class.

        Args:
            id (int): `id` `i.e. primary key`


        Returns:
            model_instance (ModelClass): An instance of the model class
        '''
        # cls represents model class

        return DBSession.query(cls).get(obj_id)

    @classmethod
    def get_or_create(cls, **kwargs):
        '''
        This method will try to get an existing object by querying from
        database by querying on fields specified by kwargs.

        If no result is found for given query then a new object will be created
        and returned.

        Args:
            cls: `model_class`
            kwargs: Key worded arguments which will be used for querying or
                    creation

        Returns:
            model_instance: An instance of the model class
        '''
        # cls represents model class

        try:
            # Query for an existing object from database for this model
            # by using given kwargs
            filters = map(
                lambda x: getattr(cls, x[0]) == x[1],
                kwargs.iteritems()
            )
            return DBSession.query(cls).filter(*filters).one()
        except sa.orm.exc.NoResultFound:
            # Create a new instance of the class using given kwargs
            obj = cls(**kwargs)

            # add newly created object to active database session
            DBSession.add(obj)

            # flush changes to the database
            DBSession.flush()

            # return newly created obj
            return obj

    @classmethod
    def get(cls, **kwargs):
        '''
        Get a signle object matching simple kewyworded query.
        '''
        # cls represents model class
        filters = map(
            lambda x: getattr(cls, x[0]) == x[1],
            kwargs.iteritems()
        )
        try:
            return DBSession.query(cls).filter(*filters).one()
        except sa.orm.exc.NoResultFound:
            return None

    @classmethod
    def get_one(cls, **kwargs):
        '''
        Get a signle object matching simple kewyworded query.
        '''
        # cls represents model class
        filters = map(
            lambda x: getattr(cls, x[0]) == x[1],
            kwargs.iteritems()
        )
        return DBSession.query(cls).filter(*filters).one()

    @classmethod
    def get_all(cls):
        '''
        Get all the objects associated with this model
        '''
        # cls represents model class
        return DBSession.query(cls).all()

    @classmethod
    def get_all_count(cls):
        '''
        Get count of all the objects associated with this model
        '''
        # cls represents model class
        return DBSession.query(cls).count()

    @classmethod
    def query(cls, **kwargs):
        '''
        Get all the object which match this query.

        This mehtod will work for simple queries only
        '''
        # cls represents model class
        filters = map(
            lambda x: getattr(cls, x[0]) == x[1],
            kwargs.iteritems()
        )
        return DBSession.query(cls).filter(*filters).all()

    def save(self, flush=True):
        # TODO - Does not take care of related model fields

        # add this object to active session
        DBSession.add(self)

        # flush changes if asked for it
        if flush is True:
            DBSession.flush()

        # return updated object
        return self

    @classmethod
    def create(cls, flush=True, **kwargs):
        # cls represents model class

        # Create a new instance of the model class
        obj = cls()

        # Update all the attributes by iterating over kwargs
        for property_name, property_value in kwargs.iteritems():
            setattr(obj, property_name, property_value)

        # Save newly created obj
        obj.save(flush=flush)

        return obj

    def update(self, flush=True, **kwargs):
        for property_name, property_value in kwargs.iteritems():
            setattr(self, property_name, property_value)

        self.save(flush=flush)

    def delete(self, flush=True):
        DBSession.delete(self)

        if flush is True:
            DBSession.flush()


Base = declarative_base(cls=BaseModelClass)

# establish a constraint naming convention.
# see http://docs.sqlalchemy.org/en/latest/core/constraints.html#configuring-constraint-naming-conventions

Base.metadata.naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
