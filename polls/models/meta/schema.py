# Third Party Stuff
import arrow
from sqlalchemy import Column, ForeignKeyConstraint, Integer, Table, event
from sqlalchemy_utils import ArrowType


class SurrogatePK(object):

    """A mixin that adds a surrogate integer 'primary key' column named
    ``id`` to any declarative-mapped class."""

    id = Column(Integer, primary_key=True)


class References(object):

    """A mixin which creates foreign key references to related classes."""
    _to_ref = set()
    _references = _to_ref.add

    @classmethod
    def __declare_first__(cls):
        """
        declarative hook called within the 'before_configure' mapper event.
        """
        for lcl, rmt in cls._to_ref:
            cls._decl_class_registry[lcl]._reference_table(
                cls._decl_class_registry[rmt].__table__)
        cls._to_ref.clear()

    @classmethod
    def _reference_table(cls, ref_table):
        """Create a foreign key reference from the local class to the given remote
        table.

        Adds column references to the declarative class and adds a
        ForeignKeyConstraint.

        """
        # create pairs of (Foreign key column, primary key column)
        cols = [(Column(), refcol) for refcol in ref_table.primary_key]

        # set "tablename_colname = Foreign key Column" on the local class
        for col, refcol in cols:
            setattr(cls, "%s_%s" % (ref_table.name, refcol.name), col)

        # add a ForeignKeyConstraint([local columns], [remote columns])
        cls.__table__.append_constraint(ForeignKeyConstraint(*zip(*cols)))


@event.listens_for(Table, "after_parent_attach")
def timestamp_cols(table, metadata):
    from .base import Base

    if metadata is Base.metadata:
        table.append_column(
            Column(
                'created_at',
                ArrowType,
                nullable=False,
                default=arrow.utcnow
            )
        )
        table.append_column(
            Column(
                'updated_at',
                ArrowType,
                nullable=False,
                default=arrow.utcnow,
                onupdate=arrow.utcnow,
            )
        )
