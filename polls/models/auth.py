# -*- coding: utf-8 -*-
from __future__ import absolute_import

import arrow
import sqlalchemy as sa
from sqlalchemy_utils import ArrowType

from polls.models.meta import Base, DBSession
from polls.models.meta.types import CaseInsensitiveComparator


class User(Base):
    __tablename__ = 'users'

    first_name = sa.Column(sa.Unicode(40), nullable=False)
    last_name = sa.Column(sa.Unicode(40), nullable=False)
    username = sa.orm.column_property(
        sa.Column(sa.Unicode(40), unique=True, nullable=False),
        comparator_factory=CaseInsensitiveComparator)
    email = sa.orm.column_property(
        sa.Column(sa.String(255), unique=True, nullable=False),
        comparator_factory=CaseInsensitiveComparator)

    is_active = sa.Column(sa.Boolean, default=False)
    is_superuser = sa.Column(sa.Boolean, default=False)
    last_login = sa.Column(ArrowType, nullable=True)

    @classmethod
    def get_by_username(cls, username):
        try:
            return DBSession.query(cls).filter(cls.username == username).one()
        except sa.orm.exc.NoResultFound:
            return None

    @classmethod
    def get_by_email(cls, email):
        try:
            return DBSession.query(cls).filter(cls.email == email).one()
        except sa.orm.exc.NoResultFound:
            return None

    def get_full_name(self):
        return u"{} {}".format(self.first_name, self.last_name)

    def update_last_login(self, timestamp=None):
        # If timestamp is not set then set it to current UTC time.
        if timestamp is None:
            timestamp = arrow.utcnow()

        self.last_login = timestamp
        self.save()

    def deactivate_user(self):
        self.is_active = False
        self.save()
