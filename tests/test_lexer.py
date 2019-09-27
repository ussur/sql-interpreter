from sql_interpreter.lexer import sql_lexer


def test_lexer():
    lexer = sql_lexer()

    # Test it out
    data = '''
    -- comment1
    SELECT table1.name
        FROM table1
        /*
        comment2 */
        LEFT JOIN table2 ON table1.id = table2.id
        WHERE table1.name LIKE 'a_%b' ;
    '''

    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)


if __name__ == '__main__':
    test_lexer()
