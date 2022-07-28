import os
import dbtools as db
import numpy as np
import sqlite3

db_path = 'mega_millions.db'


def insert_draw(data_tuple):
    """Insert the random draw in the database"""
    sql_str = '''INSERT INTO draws VALUES (?, ?, ?, ?, ?, ?, ?)'''
    db.execute_command(db_path, sql_str, data_tuple)
    

def delete_draws():
    """Delete the existing rows from the draws table to start fresh"""
    sql_str = '''DELETE FROM draws'''
    db.execute_command(db_path, sql_str)


def main():
    white_balls = []
    mega_balls = []

    sql_str = "SELECT ball_1, ball_2, ball_3, ball_4, ball_5 FROM mega_millions;"
    results = db.execute_query(db_path, sql_str)

    sql_str = "SELECT mega_ball FROM mega_millions;"
    mega_result = db.execute_query(db_path, sql_str)

    for rows in results:
        for balls in rows:
            white_balls.append(balls)

    for ball in mega_result:
        mega_balls.append(ball)

    size_white_balls = len(white_balls)
    size_mega_balls = len(mega_balls)

    print(f"Number of white balls - {size_white_balls}")
    print(f"Number of mega balls {size_mega_balls}")

    # Initialize the DRAWS table
    delete_draws()

    row_id = 1

    for z in range(2000000):
        draw = []

        for x in range(5):
            index = np.random.randint(1, size_white_balls)
            pick = white_balls[index - 1]
            # check to make sure no duplicates
            while pick in draw:
                index = np.random.randint(1, size_white_balls)
                pick = white_balls[index - 1]
            draw.append(pick)

        index = np.random.randint(1, size_mega_balls)
        pick_mega_ball = mega_balls[index - 1]

        # Insert data into the database
        draw.sort()
        insert_tuple = (row_id, draw[0], draw[1], draw[2], draw[3], draw[4], pick_mega_ball[0])
        insert_draw(insert_tuple)
        row_id += 1
        if row_id % 1000 == 0:
            print("Iteration - {}".format(row_id))

def sample_of_sample():
    for y in range(100):
        print(y + 1)
        wb_subset = white_balls.copy()
        wb_len = len(wb_subset)
        # for z in range(800):
        #     index = random.randint(1, wb_len)
        #     pick = wb_subset.pop(index - 1)
        #     wb_len -= 1
        #     # check to make sure no duplicates
        #     sample.append(pick)

        # size_of_sample = len(sample)

        for z in range(50000):
            combined = sample.copy()
            draw = []

            size_of_combined = len(combined)

            for x in range(5):
                index = random.randint(1, size_of_combined)
                pick = combined[index - 1]
                # check to make sure no duplicates
                while pick in draw:
                    index = random.randint(1, size_of_combined)
                    pick = combined[index - 1]
                draw.append(pick)

            index = random.randint(1, size_mega_balls)
            pick_mega_ball = mega_balls[index - 1]

            # Insert data into the database
            draw.sort()
            insert_tuple = (row_id, draw[0], draw[1], draw[2], draw[3], draw[4], pick_mega_ball[0])
            insert_draw(insert_tuple)
            row_id += 1

if __name__ == '__main__':
    main()
