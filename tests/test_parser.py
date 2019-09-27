from sql_interpreter.parser import sql_parser


def test_parser():
    parser = sql_parser()

    code = {
        1:'''SELECT 5, table1.*, table2.id as id
                FROM table1, (SELECT * from t) table2;
                ''',
        2: '''SELECT *
                FROM t1 INNER JOIN t2 ON (t.id, t.name) IN (SELECT * FROM t3) OR t.id <> 10 AND t.name LIKE '___';
            ''',
        3: '''SELECT *
                FROM t1 JOIN t2 ON (t1.id, t1.name) = ANY ((1, 'aaa'), (2, 'bbb'));
            ''',
        4: '''SELECT *
                FROM t1 INNER JOIN t2 JOIN t3 ON t3.name = t2.name ON t1.id = t2.id;
                ''',
        5: '''SELECT *
                FROM t1 NATURAL JOIN t2 CROSS JOIN t3;
            ''',
        6: '''SELECT *
                FROM t1 table
                WHERE table.id > 10;
                ''',
        7: '''SELECT *
                FROM t1 T
                WHERE (T.id, T.name) <>
                    (SELECT *
                      FROM t2);
                ''',
        8: '''SELECT *
                FROM t1 T
                WHERE T.name LIKE 'aaa'
                GROUP BY (T.group1, T.group2)
                HAVING group1 < 10;
            ''',
        9: '''SELECT location_id  FROM locations
                UNION ALL
                SELECT location_id  FROM departments;
            ''',
        10: '''SELECT d.department_id, e.last_name
               FROM departments d LEFT OUTER JOIN employees e
               ON d.department_id = e.department_id
               ORDER BY d.department_id ASC, e.last_name DESC NULLS LAST;
            ''',
        11: '''select * from hr;''',
    }

    print(parser.parse(code[11]).tree)


if __name__ == '__main__':
    test_parser()
