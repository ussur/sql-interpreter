from sql_interpreter.errors import SqlInterpreterError
from sql_interpreter.tables.table import Table
from sql_interpreter.tables.join_table import JoinTable


class Context:
    def __init__(self, global_context=None, parent=None):
        self._tables = {}
        self._parent = parent
        if global_context:
            self.global_context = global_context
        else:
            self.global_context = self

    @staticmethod
    def from_global(global_context):
        return Context(global_context=global_context)

    @staticmethod
    def from_parent(context):
        return Context(context.global_context, context)

    def clear(self):
        self._tables.clear()

    def define(self, table: Table, alias=None):
        table_id = alias if alias else table.name
        if not table_id:
            table_id = 't' + str(len(self._tables) + 1)
        self._tables[table_id] = table
        return table_id

    def resolve(self, table_id):
        table = self._tables.get(table_id)
        if table:
            return table
        if self != self.global_context:
            if self._parent:
                return self._parent.resolve(table_id)
            table = self.global_context.resolve(table_id)
            if table:
                return table
        raise SqlInterpreterError(
                'Unable to resolve table id: "{}"'.format(table_id))

    def get_table_name(self, alias: str):
        return self._tables[alias].name

    def join(self):
        #return self._tables['employees']
        '''if len(self._tables) == 1:
            return list(self._tables.values())[0]'''
        return JoinTable(list(self._tables.values()))
