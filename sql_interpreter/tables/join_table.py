from .table import Table
from itertools import chain, product


class JoinTable(Table):
    def __init__(self, parents):
        self._parents = parents
        self._cols = [(p.name, col) for p in self._parents
                      for col in p.columns]
        self._rows = []

    def get_value(self, row, column, prefix=None):
        if prefix:
            return row[prefix + '.' + column]
        if not self.is_unique(column):
            raise Exception(
                "Unable to resolve ambiguous column name: {}".format(column))
        t = list(filter(lambda col: col[1] == column, self._cols))
        return row[t[0][0] + '.' + column]

    def is_unique(self, column):
        return [col[1] for col in self._cols].count(column) == 1

    @property
    def columns(self):
        return [col[0] + '.' + col[1] for col in self._cols]

    @property
    def rows(self):
        all_rows = product(*[p.rows for p in self._parents])
        for r in all_rows:
            full_row = list(chain(*[list(d.values()) for d in r]))
            yield {self.columns[i]: full_row[i] for i in range(self.col_count)}
