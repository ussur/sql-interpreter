from sql_interpreter.interpreter import SqlInterpreter
from sql_interpreter.errors import SqlInterpreterError
from sql_interpreter.tables.table import Table


class Cli:

    def __init__(self, interpreter: SqlInterpreter):
        self.interpreter = interpreter

    def execute(self, sql: str):
        try:
            result = self.interpreter.interpret(sql)
            for table in result:
                self.print_table(table)
        except SqlInterpreterError as error:
            self.print_message(error)

    def print_global(self, table_name):
        self.print_table(self.interpreter.get_global(table_name))

    @staticmethod
    def print_table(table: Table):
        longest_cols = [
            max(max([len('Null' if row[column] is None
                         else str(row[column]))
                     for row in table.rows]),
                len(column)) + 3
            for column in table.columns
        ]
        row_format = "".join(["{:>" + str(longest_col) + "}"
                              for longest_col
                              in longest_cols])
        print(row_format.format(*table.columns))
        for row in table.rows:
            row_to_print = ['Null' if item is None else item
                            for item in row.values()]
            print(row_format.format(*row_to_print))

    @staticmethod
    def print_message(message):
        print(message)

    @staticmethod
    def print_new_line():
        print()
