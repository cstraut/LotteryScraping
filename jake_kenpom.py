import os
import sqlite3

from datetime import datetime
from selenium import webdriver

db_path = 'game_results.db'


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
            result = cursor.execute(sql_str)
        else:
            result = cursor.execute(sql_str, values)
        conn_db.commit()
    except sqlite3.Error as error:
        print('Failed to execute SQL Command', error)
        cursor.close()
    finally:
        cursor.close()
        conn_db.close()


def main():
    web = r'https://barttorvik.com/schedule.php?date={}&conlimit='
    path = r'/Users/cstraut/Lottery' #introduce your file's path inside '...'
    games_played = True
    date_range = ['20201222', '20201223']

    # Find table by class name
    game_list = []

    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.set_headless()
    # driver = webdriver.Firefox(firefox_options=fireFoxOptions)
    driver = webdriver.Firefox()

    if date_range is not None:
        for item in date_range:
            site = web.format(item)
            driver.get(site)
    else:
        site = web.format('20201223')
        druver,get(site)

    # Remove any old database file
    if os.path.isfile(db_path):
        os.remove(db_path)

    # Create database and table to store the information
    # sql_str = '''CREATE TABLE mega_millions (id INT PRIMARY KEY, draw_date TEXT NOT NULL,
    #     ball_1 INT, ball_2 INT, ball_3 INT, ball_4 INT, ball_5 INT, mega_ball INT);'''
    # execute_command(sql_str)

    # Set initial index value of 1
    i = 1

    while games_played:
            row_game_results = driver.find_element_by_xpath('/html/body/div[1]/div/p[4]/table/tbody/tr[{}]'.format(i)).text
            match_up = driver.find_element_by_xpath('/html/body/div[1]/div/p[4]/table/tbody/tr[{}]/td[2]'.format(i)).text
            trank_value = driver.find_element_by_xpath('/html/body/div[1]/div/p[4]/table/tbody/tr[{}]/td[3]'.format(i)).text
            results = driver.find_element_by_xpath('/html/body/div[1]/div/p[4]/table/tbody/tr[{}]/td[5]'.format(i)).text

            print('Match Up - {}'.format(match_up))
            print('TRank Value - {}'.format(trank_value))
            print('Results - {}'.format(results))

            # Insert data into the database
            # data_tuple = (index, row_date, int(lists_balls[0]), int(lists_balls[1]),
            #     int(lists_balls[2]), int(lists_balls[3]), int(lists_balls[4]), int(mega))
            # sql_str = '''INSERT INTO mega_millions VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

            # execute_command(sql_str, data_tuple)

            i += 1

        # next_page = driver.find_element_by_xpath('/html/body/div[1]/table[2]/tbody/tr[4]/td[2]/table/tbody/tr[28]/td/table/tbody/tr/td[4]/a')
        # next_page.click()
    driver.close()

if __name__ == '__main__':
    main()