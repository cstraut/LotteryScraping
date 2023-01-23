import os
import dbtools as db
import numpy as np
import sqlite3

db_path = 'mega_millions.db'


def insert_draw(data_tuple):
    """Insert the random draw in the database"""
    sql_str = '''INSERT INTO draws_column VALUES (?, ?, ?, ?, ?, ?, ?)'''
    db.execute_command(db_path, sql_str, data_tuple)

    
def main():
    # Find table by class name
    wb_1 = []
    wb_2 = []
    wb_3 = []
    wb_4 = []
    wb_5 = []
    mega_balls = []

    # Set path if running in the container to local folder and not MAC
    path = os.getcwd()

    # Create database table for column selection
    sql_str = '''CREATE TABLE draws_column (id INT PRIMARY KEY, ball_1 INT, ball_2 INT, ball_3 INT, ball_4 INT, ball_5 INT, mega_ball INT);'''
    db.execute_command(db_path, sql_str)

    sql_str = '''SELECT ball_1, ball_2, ball_3, ball_4, ball_5, mega_ball FROM mega_millions'''
    results = db.execute_query(db_path, sql_str)

    for i in results:
        wb_1.append(i[0])
        wb_2.append(i[1])
        wb_3.append(i[2])
        wb_4.append(i[3])
        wb_5.append(i[4])
        mega_balls.append(i[5])

    size_white_balls = size_mega_balls = len(results)

    print(f"Number of white balls - {size_white_balls * 5}")
    print(f"Number of mega balls {size_mega_balls}")

    row_id = 1

    wb_len = len(wb_1)

    for y in range(2000000):
        pick = []
        index = np.random.randint(1, wb_len)
        pick.append(wb_1[index - 1])

        # check to make sure no duplicates
        index = np.random.randint(1, wb_len)
        value = wb_2[index - 1]
        while value in pick:
            index = np.random.randint(1, wb_len)
            value = wb_2[index - 1]
        pick.append(value)

        index = np.random.randint(1, wb_len)
        value = wb_3[index - 1]
        while value in pick:
            index = np.random.randint(1, wb_len)
            value = wb_3[index - 1]
        pick.append(value)
            
        index = np.random.randint(1, wb_len)
        value = wb_4[index - 1]
        while value in pick:
            index = np.random.randint(1, wb_len)
            value = wb_4[index - 1]
        pick.append(value)
            
        index = np.random.randint(1, wb_len)
        value = wb_5[index - 1]
        while value in pick:
            index = np.random.randint(1, wb_len)
            value = wb_5[index - 1]
        pick.append(value)
        pick.sort()

        index = np.random.randint(1, size_mega_balls)
        pick_mega_ball = mega_balls[index - 1]
            
        # Insert data into the database
        insert_tuple = (row_id, pick[0], pick[1], pick[2], pick[3], pick[4], pick_mega_ball)
        insert_draw(insert_tuple)
        row_id += 1

if __name__ == '__main__':
    main()