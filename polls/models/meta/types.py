# Third Party Stuff
from sqlalchemy import Numeric, func
from sqlalchemy.orm.properties import ColumnProperty

Amount = Numeric(8, 2)


class CaseInsensitiveComparator(ColumnProperty.Comparator):

    'A case-insensitive SQLAlchemy comparator for unicode columns'

    def __eq__(self, other):
        'Return True if the lowercase of both columns are equal'
        return func.lower(self.__clause_element__()) == func.lower(other)
