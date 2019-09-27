from enum import Enum


class SelectType(Enum):
    DISTINCT = 'distinct'
    ALL = 'all'


class Binary(Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    CON = '||'
    OR = 'or'
    AND = 'and'
    LIKE = 'like'
    IN = 'in'


class Unary(Enum):
    UPLUS = '+'
    UMINUS = '-'
    NOT = 'not'
    EXISTS = 'exists'


class ValueType(Enum):
    STRING = 'string'
    NUMBER = 'number'
    IDENTIFIER = 'identifier'
    ASTERISK = 'asterisk'


class Comparison(Enum):
    EQ = '='
    NE = '<>'
    GT = '>'
    LT = '<'
    GE = '>='
    LE = '<='


class ComparisonGroup(Enum):
    ANY = 'any'
    ALL = 'all'


class OuterJoinType(Enum):
    FULL = 'full'
    LEFT = 'left'
    RIGHT = 'right'


class Combine(Enum):
    UNION = 'union'
    UNION_ALL = 'union all'
    INTERSECT = 'intersect'
    MINUS = 'minus'


class Order(Enum):
    ASC = 'asc'
    DESC = 'desc'
