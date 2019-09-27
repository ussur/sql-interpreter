from abc import ABC, abstractmethod
from sql_interpreter.enums import *
from sql_interpreter.context import Context
from sql_interpreter.tables.select_table import SelectTable
from sql_interpreter.tables.join_table import JoinTable
from sql_interpreter.tables.ordered_table import OrderedTable


class Node(ABC):
    @abstractmethod
    def __str__(self)->str:
        pass

    @property
    def children(self)->['Node', ...]:
        return []

    @property
    def tree(self)->str:
        return '\n'.join(self._tree)

    @property
    def _tree(self)->[str, ...]:
        st = [str(self)]
        '''print([str(x) for x in self.children])
        print()'''
        for i, child in enumerate(self.children):
            ch0, ch = '├', '│'
            if i == len(self.children) - 1:
                ch0, ch = '└', ' '
            st.extend((ch0 if j == 0 else ch) + ' '
                      + s for j, s in enumerate(child._tree))
        return st

    @abstractmethod
    def interpret(self, context: Context):
        pass


class ScriptNode(Node):
    def __init__(self, queries):
        self.queries = queries

    def __str__(self)->str:
        return 'script'

    @property
    def children(self)->['Node', ...]:
        return self.queries

    def interpret(self, context):
        return [child.interpret(Context.from_global(context))
                for child in self.children]


class TableNode(Node):
    def __init__(self, table, alias=None):
        self.table = table
        self.alias = alias

    def __str__(self)->str:
        s = 'table'
        if type(self.table) == str:
            s += ' name: ' + self.table
        if self.alias:
            s += ' alias: ' + self.alias
        return s

    @property
    def children(self)->['Node', ...]:
        if type(self.table) == str:
            return []
        return [self.table]

    def interpret(self, context):
        if type(self.table) == str:
            table = context.resolve(self.table)
        else:
            table = self.table.interpret(context)
        context.define(table, self.alias)
        return table


class SelectStatementNode(Node):
    def __init__(self, select_clause, from_clause,
                 order_by_clause=None):
        self.select_clause = select_clause
        self.from_clause = from_clause
        self.order_by_clause = order_by_clause

    def __str__(self)->str:
        return 'select statement'

    @property
    def children(self)->['Node', ...]:
        return [self.select_clause, self.from_clause]

    def interpret(self, context):
        self.from_clause.interpret(context)
        '''for table in tables:
            context.define(table)'''
        table = self.select_clause.interpret(context)
        if self.order_by_clause:
            table = self.order_by_clause.get_table(table)
        return table


class SelectClauseNode(Node):
    def __init__(self, columns, select_type=SelectType.ALL):
        self.columns = columns
        self.select_type = select_type

    def __str__(self)->str:
        return 'select ' + str(self.select_type.value)

    @property
    def children(self)->['Node', ...]:
        return self.columns

    def interpret(self, context):
        for child in self.children:
            child.interpret(context)
        join_table = context.join()
        distinct = self.select_type == SelectType.DISTINCT
        return SelectTable(join_table, self.children, distinct)


class ColumnNode(Node):
    def __init__(self, expr, alias=None):
        self.expr = expr
        self.alias = alias

    def __str__(self)->str:
        s = 'column'
        if self.alias:
            s += ' alias: ' + self.alias
        return s

    @property
    def children(self)->['Node', ...]:
        return [self.expr]

    @property
    def name(self)->str:
        return self.alias or self.expr.name

    def interpret(self, context):
        self.expr.interpret(context)

    def get_value(self, row, table: JoinTable):
        return self.expr.get_value(row, table)


class ValueNode(Node):
    def __init__(self, value, type: ValueType, prefix=None):
        self.value = value
        self.type = type
        self.prefix = prefix
        self.table = None

    def __str__(self)->str:
        s = str(self.value)
        if self.prefix:
            s += ' prefix: ' + self.prefix
        return s

    @property
    def name(self)->str:
        if self.type == ValueType.NUMBER:
            return str(self.value)
        if self.type == ValueType.STRING:
            return "'" + self.value + "'"
        else:
            if self.prefix:
                return self.prefix + '.' + self.value
            return self.value

    def interpret(self, context):
        if self.prefix:
            self.table = context.get_table_name(self.prefix)

    def get_value(self, row, table: JoinTable):
        if self.type == ValueType.IDENTIFIER:
            return table.get_value(row, self.value, self.table)
        return self.value


class BinaryNode(Node):
    def __init__(self, op: Binary, arg1: ColumnNode, arg2: ColumnNode):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2

    def __str__(self)->str:
        return str(self.op.value)

    @property
    def name(self)->str:
        return self.arg1.name + ' ' + str(self.op.value) +\
               ' ' + self.arg2.name

    @property
    def children(self)->['Node', ...]:
        return [self.arg1, self.arg2]

    def interpret(self, context):
        for child in self.children:
            child.interpret(context)

    def get_value(self, row, table: JoinTable):
        arg1 = self.arg1.get_value(row, table)
        arg2 = self.arg2.get_value(row, table)
        if not arg1 or not arg2:
            return None
        if self.op == Binary.ADD:
            return arg1 + arg2
        elif self.op == Binary.SUB:
            return arg1 - arg2
        elif self.op == Binary.MUL:
            return arg1 * arg2
        elif self.op == Binary.DIV:
            return arg1 / arg2
        elif self.op == Binary.CON:
            return str(arg1) + str(arg2)
        elif self.op == Binary.OR:
            return arg1 or arg2
        elif self.op == Binary.AND:
            return arg1 and arg2
        elif self.op == Binary.LIKE:
            raise NotImplementedError
        elif self.op == Binary.IN:
            raise NotImplementedError


class UnaryNode(Node):
    def __init__(self, op: Unary, arg: ColumnNode):
        self.op = op
        self.arg = arg

    def __str__(self)->str:
        return str(self.op.value)

    @property
    def name(self)->str:
        return self.op.value + ' ' + self.arg.name

    @property
    def children(self)->['Node', ...]:
        return [self.arg]

    def interpret(self, context):
        self.arg.interpret(context)

    def get_value(self, row, table: JoinTable):
        arg = self.arg.get_value(row, table)
        if self.op == Unary.UPLUS:
            return arg
        elif self.op == Unary.UMINUS:
            return -arg
        elif self.op == Unary.NOT:
            return not arg


class FromClauseNode(Node):
    def __init__(self, tables):
        self.tables = tables

    def __str__(self)->str:
        return 'from'

    @property
    def children(self)->['Node', ...]:
        return self.tables

    def interpret(self, context):
        return [child.interpret(context) for child in self.children]


class OrderByNode(Node):
    def __init__(self, sort_keys):
        self.sort_keys = sort_keys

    def __str__(self)->str:
        return 'order by'

    def interpret(self, context):
        pass

    def get_table(self, table):
        return OrderedTable(
            table, [(key[0], True if key[1] == Order.DESC else False)
                    for key in self.sort_keys])
