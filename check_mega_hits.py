import os
import dbtools as db
import random
import sqlite3

db_path = 'mega_millions.db'

def main():

    # Find table by class name
    white_balls = []
    mega_balls = []

    sql_str = '''SELECT ball_1, ball_2, ball_3, ball_4, ball_5, mega_ball FROM mega_millions
        ORDER BY ball_1'''
    results = db.execute_query(sql_str)

    row = 1

    for i in results:
        balls = (i[0], i[1], i[2], i[3], i[4], i[5])
        sql_str = '''SELECT COUNT(*) FROM draws WHERE ball_1 = ? AND ball_2 = ? AND
            ball_3 = ? AND ball_4 = ? AND ball_5 = ? AND mega = ?'''
        count_val = db.execute_query(sql_str, balls)
        if count_val[0][0] > 0:
            print('{}: Balls - {}, {}, {}, {}, {}  mega ball {}'.format(
                row, i[0], i[1], i[2], i[3], i[4], i[5]), end='')
            print(' - Occurs {} times'.format(count_val[0][0]))
            row += 1


if __name__ == '__main__':
    main()