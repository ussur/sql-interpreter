import ply.lex as lex
import re


reserved = {
   'all': 'ALL',
   'and': 'AND',
   'any': 'ANY',
   'as': 'AS',
   'asc': 'ASC',
   'between': 'BETWEEN',
   'by': 'BY',
   'cross': 'CROSS',
   'desc': 'DESC',
   'distinct': 'DISTINCT',
   'escape': 'ESCAPE',
   'exists': 'EXISTS',
   'from': 'FROM',
   'full': 'FULL',
   'group': 'GROUP',
   'having': 'HAVING',
   'in': 'IN',
   'inner': 'INNER',
   'intersect': 'INTERSECT',
   'is': 'IS',
   'join': 'JOIN',
   'left': 'LEFT',
   'like': 'LIKE',
   'minus': 'MINUS',
   'natural': 'NATURAL',
   'not': 'NOT',
   'null': 'NULL',
   'on': 'ON',
   'or': 'OR',
   'order': 'ORDER',
   'outer': 'OUTER',
   'right': 'RIGHT',
   'select': 'SELECT',
   'union': 'UNION',
   'where': 'WHERE',
}

tokens = list(reserved.values()) + [
    # Literals
    'IDENTIFIER', 'LPAR', 'RPAR', 'SEMICOLON', 'COMMA',
    'DOT', 'SQUOTE',

    # Value types
     'FLOAT','INT', 'STR',

    # Operations
    'ADD', 'SUB', 'ASTERISK', 'SLASH', 'EQ', 'LESS',
    'MORE', 'NOTEQ', 'LESSEQ', 'MOREEQ', 'CONCAT',
    ]


def sql_lexer():
    t_LPAR = r'\('
    t_RPAR = r'\)'
    t_SEMICOLON = r';'
    t_COMMA = r','
    t_DOT = r'\.'

    t_ADD = r'\+'
    t_SUB = r'-'
    t_ASTERISK = r'\*'
    t_SLASH = r'/'
    t_EQ = r'='
    t_NOTEQ = r'<>'
    t_LESS = r'<'
    t_MORE = r'>'
    t_LESSEQ = r'<='
    t_MOREEQ = r'>='
    t_CONCAT = r'\|\|'

    def t_IDENTIFIER(t):
        r'[a-zA-Z_$]+[a-zA-Z\d_$]*'
        t.type = reserved.get(t.value.lower().strip(),'IDENTIFIER')
        return t

    def t_FLOAT(t):
        r'[0-9]+[.]([0-9]+)?'
        t.value = float(t.value)
        return t

    def t_INT(t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_comment(t):
        r'(/\*(.|\n)*?\*/)|(--.*)'
        pass

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore = ' \r\t\f'

    # Error handling rule
    def t_error(t):
        print("Illegal character '{0}' at line {1}"
              .format(t.value[0], t.lineno))
        t.lexer.skip(1)


    states = (
            ('string','exclusive'),
        )

    def t_ANY_SQUOTE(t):
        r"'"
        if t.lexer.current_state() == 'string':
            t.lexer.begin('INITIAL')
        else:
            t.lexer.begin('string')
        return t

    def t_string_STR(t):
        r'[^\']+'
        t.value = str(t.value)
        return t

    t_string_ignore = ''

    def t_string_error(t):
        print("Illegal character '{0}' at line {1}"
              .format(t.value[0], t.lineno))
        t.lexer.skip(1)

    return lex.lex(reflags=re.IGNORECASE)
