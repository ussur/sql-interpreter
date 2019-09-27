import os
from sql_interpreter.tables.csv_table import CsvTable
from sql_interpreter.interpreter import SqlInterpreter
from sql_interpreter.cli import Cli


class InterpreterTest():
    def setUp(self):
        self.interpreter = SqlInterpreter()
        self.cli = Cli(self.interpreter)
        filename = os.path.join(
            os.path.dirname(__file__), 'resources/employees.csv')
        self.interpreter.load(CsvTable('employees', filename))
        filename = os.path.join(
            os.path.dirname(__file__), 'resources/departments.csv')
        self.interpreter.load(CsvTable('departments', filename))

    def tearDown(self):
        self.interpreter.unload_all()

    def test_select_1(self):
        sql = '''select
            id, first_name || ' ' || last_name as full_name, salary - 1000
            from employees;'''
        self.cli.execute(sql)
        self.cli.print_new_line()

    def test_select_2(self):
        sql = '''select
            e.id, last_name, department_id, departments.id, name
            from employees e, departments;'''
        self.cli.execute(sql)
        self.cli.print_new_line()

    def test_select_all(self):
        code = '''select * from employees;'''
        self.interpreter.interpret(code)
        self.cli.print_new_line()

    def test_select_distinct(self):
        sql = '''select distinct
            departments.id as dep_id, employees.salary as sal
            from employees, departments
            order by dep_id, sal desc;'''
        self.cli.execute(sql)
        self.cli.print_new_line()


if __name__ == '__main__':
    test = InterpreterTest()
    test.setUp()
    test.test_select_1()
    test.test_select_2()
    test.test_select_distinct()
    test.tearDown()
