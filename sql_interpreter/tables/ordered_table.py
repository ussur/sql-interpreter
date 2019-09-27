from .table import Table


class OrderedTable(Table):
    def __init__(self, parent, sort_keys):
        self._parent = parent
        self.sort_keys = sort_keys

    @property
    def name(self):
        return self._parent.name

    @property
    def columns(self):
        return self._parent.columns

    @property
    def rows(self):
        return sorted(self._parent.rows,
                      key=lambda r: self._order(r))

    def _order(self, r):
        return [(r[k[0]] is None, -r[k[0]] if r[k[0]] else None)
                if k[1] else (r[k[0]] is not None, r[k[0]])
                for k in self.sort_keys]