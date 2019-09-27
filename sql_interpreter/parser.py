import ply.yacc as yacc
from sql_interpreter.lexer import tokens
from sql_interpreter.enums import *
from sql_interpreter.nodes import *


def sql_parser():
    def p_script_1(p):
        '''script : script select_statement SEMICOLON
        '''
        p[0] = p[1]
        p[0].queries.append(p[2])

    def p_script_2(p):
        '''script : select_statement SEMICOLON
        '''
        p[0] = ScriptNode([p[1]])

    def p_select_statement(p):
        '''select_statement : select_clause from_clause order_by_clause
        '''
        node = SelectStatementNode(p[1], p[2])
        if p[3]:
            node.order_by_clause = p[3]
        p[0] = TableNode(node)

    def p_select_clause(p):
        '''select_clause : SELECT select_type columns
        '''
        p[0] = SelectClauseNode(p[3], select_type=p[2])

    def p_select_type(p):
        '''select_type : ALL
                       | DISTINCT
                       | empty
        '''
        if p[1]:
            p[0] = SelectType(p[1].lower())
        else:
            p[0] = SelectType.ALL

    def p_columns_1(p):
        '''columns : columns COMMA column
        '''
        p[0] = p[1]
        p[0].append(p[3])

    def p_columns_2(p):
        '''columns : column
        '''
        p[0] = [p[1]]

    def p_column_1(p):
        '''column : expr AS IDENTIFIER
        '''
        p[0] = ColumnNode(p[1], alias=p[3])

    def p_column_2(p):
        '''column : expr IDENTIFIER
        '''
        p[0] = ColumnNode(p[1], alias=p[2])

    def p_column_3(p):
        '''column : expr
        '''
        p[0] = ColumnNode(p[1])

    def p_expr(p):
        '''expr : compound_expr
                | simple_expr
        '''
        p[0] = p[1]

    def p_simple_expr_1(p):
        '''simple_expr : IDENTIFIER DOT identifier
                       | IDENTIFIER DOT asterisk
        '''
        p[3].prefix = p[1]
        p[0] = p[3]

    def p_simple_expr_2(p):
        '''simple_expr : identifier
                       | asterisk
                       | string
                       | number
        '''
        p[0] = p[1]

    def p_identifier(p):
        '''identifier : IDENTIFIER
        '''
        p[0] = ValueNode(p[1], ValueType.IDENTIFIER)

    def p_asterisk(p):
        '''asterisk : ASTERISK
        '''
        p[0] = ValueNode(p[1], ValueType.ASTERISK)

    def p_string(p):
        '''string : SQUOTE STR SQUOTE
        '''
        p[0] = ValueNode(p[2], ValueType.STRING)

    def p_number(p):
        '''number : FLOAT
                  | INT
        '''
        p[0] = ValueNode(p[1], ValueType.NUMBER)

    def p_compound_expr_1(p):
        '''compound_expr : expr ADD expr
                         | expr SUB expr
                         | expr ASTERISK expr
                         | expr SLASH expr
                         | expr CONCAT expr
        '''
        p[0] = BinaryNode(Binary(p[2]), p[1], p[3])

    def p_compound_expr_2(p):
        '''compound_expr : ADD expr
                         | SUB expr
        '''
        p[0] = UnaryNode(Unary(p[1]), p[2])

    def p_compound_expr_3(p):
        '''compound_expr : LPAR expr RPAR
        '''
        p[0] = p[2]

    def p_from_clause_1(p):
        '''from_clause : FROM tables
        '''
        p[0] = FromClauseNode(p[2])

    def p_tables_1(p):
        '''tables : tables COMMA table
        '''
        p[0] = p[1]
        p[0].append(p[3])

    def p_tables_2(p):
        '''tables : table
        '''
        p[0] = [p[1]]

    def p_table_1(p):
        '''table : identifier
        '''
        p[0] = TableNode(p[1].value)

    def p_table_2(p):
        '''table : identifier IDENTIFIER
        '''
        p[0] = TableNode(p[1].value, alias=p[2])

    def p_table_3(p):
        '''table : LPAR select_statement RPAR IDENTIFIER
        '''
        p[0] = p[2]
        p[0].alias=p[4]

    def p_order_by_clause_1(p):
        '''order_by_clause : empty
        '''

    def p_order_by_clause_2(p):
        '''order_by_clause : ORDER BY order_by_list
        '''
        p[0] = OrderByNode(p[3])

    def p_order_by_list_1(p):
        '''order_by_list : order_by_list COMMA order_by_item
        '''
        p[1].append(p[3])
        p[0] = p[1]

    def p_order_by_list_2(p):
        '''order_by_list : order_by_item
        '''
        p[0] = [p[1]]

    def p_order_by_item(p):
        '''order_by_item : IDENTIFIER asc_desc
        '''
        p[0] = (p[1], p[2])

    def p_asc_desc_1(p):
        '''asc_desc : empty
        '''
        p[0] = Order.ASC

    def p_asc_desc_2(p):
        '''asc_desc : ASC
                    | DESC
        '''
        p[0] = Order(p[1].lower())

    def p_empty(p):
        '''empty :'''
        pass

    class ParserError(Exception): pass

    def p_error(p):
        if p:
            raise ParserError('Unexpected token: "{0}" at line: {1}, index: {2}'.format(p.value, p.lineno, p.lexpos))
        raise ParserError('Unexpected end of string: are you missing a ";"?')

    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('right', 'NOT'),
        ('left', 'EQ', 'NOTEQ'),
        ('left', 'MORE', 'LESS', 'MOREEQ', 'LESSEQ', 'LIKE', 'BETWEEN'),
        ('left', 'ADD', 'SUB'),
        ('left', 'ASTERISK', 'SLASH'),
        ('left', 'CONCAT'),
    )

    start = 'script'
    return yacc.yacc()


if __name__ == "__main__":
    from lexer import sql_lexer
    lexer = sql_lexer()
    parser = sql_parser()
    code = '''select * from hr;
            '''
    print(parser.parse(code, lexer=lexer, debug=False).tree)
