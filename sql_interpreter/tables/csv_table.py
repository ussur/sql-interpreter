from .table import Table
import csv
import ast


class CsvTable(Table):

    def __init__(self, name, filename, delimiter=','):
        def convert(string):
            try:
                return ast.literal_eval(string)
            except ValueError:
                return string

        with open(filename, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
            data = [line for line in csv_reader]
        super().__init__(name, list(data[0].keys()))
        rows = [[convert(item) or None for item in d.values()]
                for d in data]
        self.add_rows(rows)

    def to_csv(self, filename=None):
        if filename is None:
            filename = self.name + '.csv'
        with open(filename, mode='w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(self._cols)
            for row in self._rows:
                csv_writer.writerow(row)
