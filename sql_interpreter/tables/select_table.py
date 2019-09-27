from .table import Table
from .join_table import JoinTable


class SelectTable(Table):
    def __init__(self, parent: JoinTable, columns, distinct=False):
        self._parent = parent
        self._cols = columns  # list of ColumnNode
        self._rows = []
        self.distinct = distinct
        self.name = None

    @property
    def columns(self):
        return [col.name for col in self._cols]

    @property
    def rows(self):
        if not self.distinct:
            for p_row in self._parent.rows:
                row = [col.get_value(p_row, self._parent)
                       for col in self._cols]
                yield {self.columns[i]: row[i] for i in range(self.col_count)}
        else:
            if len(self._rows) == 0:
                self._rows = [[col.get_value(p_row, self._parent)
                               for col in self._cols]
                              for p_row in self._parent.rows]
            #rows = set(self._rows) if self.distinct else self._rows
            for row in set(tuple(row) for row in self._rows):
                yield {self.columns[i]: row[i]
                       for i in range(self.col_count)}
