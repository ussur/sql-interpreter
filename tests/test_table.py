import unittest
import os
from sql_interpreter.tables.table import Table
from sql_interpreter.tables.csv_table import CsvTable


class TableTest(unittest.TestCase):

    def test_add_row(self):
        columns = ['id', 'name', 'salary']
        table = Table('hr', columns)
        self.assertEqual(table.row_count, 0)
        table.add_row([1, 'Dave', 1000])
        table.add_row([2, 'Abigail', 2000])
        table.add_row([3, 'Peter', 1000])
        self.assertEqual(table.row_count, 3)

    def test_csv(self):
        filename = os.path.join(self.basedir,
                                'resources/employees.csv')
        table = CsvTable('hr', filename)
        self.assertEqual(table.col_count, 5)
        self.assertEqual(table.row_count, 8)

    '''def test_ordered(self, cli: Cli):
        table = test_csv()
        cli.print_message('Table without ordering:')
        cli.print_table(table)
        ordered_table = OrderedTable(table, ['salary', 'last_name'])
        cli.print_message('Ordered by salary and last name:')
        cli.print_table(ordered_table)'''


if __name__ == "__main__":
    unittest.main()
