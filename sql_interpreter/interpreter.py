from sql_interpreter.lexer import sql_lexer
from sql_interpreter.parser import sql_parser
from sql_interpreter.tables.table import Table
from sql_interpreter.context import Context


class SqlInterpreter:
    def __init__(self):
        self.lexer = sql_lexer()
        self.parser = sql_parser()
        self.global_context = Context()

    def load(self, table: Table):
        self.global_context.define(table)

    def unload_all(self):
        self.global_context.clear()

    def interpret(self, sql):
        tree = self.parser.parse(sql, self.lexer)
        result = tree.interpret(self.global_context)
        return result

    def get_global(self, table_name):
        return self.global_context.resolve(table_name)
