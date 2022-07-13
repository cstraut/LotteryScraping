import os
import random
import sqlite3

db_path = 'mega_millions.db'

def execute_command(sql_str, values=None):
    """Execute a database command"""
    conn_db = None
    cursor = None    
    
    try:
        conn_db = sqlite3.connect(db_path)
        cursor = conn_db.cursor()
        if values is None:
            cursor.execute(sql_str)
        else:
            cursor.execute(sql_str, values)
        conn_db.commit()
    except sqlite3.Error as error:
        print('Failed to execute SQL Command', error)
        cursor.close()
    finally:
        cursor.close()
        conn_db.close()


def execute_query(sql_str, values=None):
    """Execute SELECT statement"""
    results = None
    conn_db = None
    cursor = None
    
    try:
        conn_db = sqlite3.connect(db_path)
        cursor = conn_db.cursor()
        if values is None:
            results = cursor.execute(sql_str).fetchall()
        else:
            results = cursor.execute(sql_str, values).fetchall()
        conn_db.commit()
    except sqlite3.Error as error:
        print('Failed to execute SQL Command', error)
        cursor.close()
    finally:
        cursor.close()
        conn_db.close()

    return results

def insert_draw(data_tuple):
    """Insert the random draw in the database"""
    sql_str = '''INSERT INTO draws VALUES (?, ?, ?, ?, ?, ?, ?)'''
    execute_command(sql_str, data_tuple)
    
def main():
    row_id = 1

    ball_1 = []
    sql_str = 'SELECT ball_1 FROM mega_millions'
    ball_1 = execute_query(sql_str)

    for z in range(5000000):
        index = random.randint(1, len(ball_1))
        pick1 = ball_1[index - 1][0]
            
        sql_str = 'SELECT ball_2 FROM mega_millions WHERE ball_1 = {}'.format(pick1)
        results = execute_query(sql_str)

        index = random.randint(1, len(results))
        pick2 = results[index - 1][0]
        
        sql_str = 'SELECT ball_3 FROM mega_millions WHERE ball_2 = {}'.format(pick2)
        results = execute_query(sql_str)

        index = random.randint(1, len(results))
        pick3 = results[index - 1][0]

        sql_str = 'SELECT ball_4 FROM mega_millions WHERE ball_3 = {}'.format(pick3)
        results = execute_query(sql_str)

        index = random.randint(1, len(results))
        pick4 = results[index - 1][0]

        sql_str = 'SELECT ball_5 FROM mega_millions WHERE ball_4 = {}'.format(pick4)
        results = execute_query(sql_str)

        index = random.randint(1, len(results))
        pick5 = results[index - 1][0]

        sql_str = 'SELECT mega_ball FROM mega_millions WHERE ball_5 = {}'.format(pick5)
        results = execute_query(sql_str)
        
        index = random.randint(1, len(results))
        pick_mega_ball = results[index - 1][0]

        insert_tuple = (row_id, pick1, pick2, pick3, pick4, pick5, pick_mega_ball)
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