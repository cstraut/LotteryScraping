import os
import sqlite3
from time import sleep

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

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
    web = 'https://www.usamega.com/mega-millions/results'
    
    # Set path if running in the container to local folder and not MAC
    path = '/usr/src/app'
    # path = '/Users/cstraut/Lottery'
    date_in_range = True

    # Find table by class name
    number_balls = []
    mega_balls = []
    list_balls = []

    # display = Display(visible=0, size=(1600, 1024))
    # display.start()

    # Remove any old database file
    if os.path.isfile(db_path):
        os.remove(db_path)

    # Create database and table to store the information
    sql_str = '''CREATE TABLE mega_millions (id INT PRIMARY KEY, draw_date TEXT NOT NULL,
        ball_1 INT, ball_2 INT, ball_3 INT, ball_4 INT, ball_5 INT, mega_ball INT);'''
    execute_command(sql_str)

    # Create database table DRAWS for future processing
    sql_str = '''CREATE TABLE draws (id INT PRIMARY KEY, ball_1 INT, ball_2 INT, ball_3 INT, ball_4 INT, ball_5 INT, mega_ball INT);'''
    execute_command(sql_str)

    # Set initial index value of 1
    index = 1
    page_count = 1

    while date_in_range:
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(web)
        driver.implicitly_wait(3)

        for i in range(1, 27):
            row_date = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[4]/table/tbody/tr[{}]/td[1]/section/a'.format(i)).text
            print("Row Date - " + row_date)
            for j in range(1, 7):
                list_balls.append(driver.find_element(By.XPATH, '/html/body/div[1]/main/div[4]/table/tbody/tr[{}]/td[1]/section/ul/li[{}]'.format(i, j)).text)

            # Insert data into the database
            data_tuple = (index, row_date, int(list_balls[0]), int(list_balls[1]),
                int(list_balls[2]), int(list_balls[3]), int(list_balls[4]), int(list_balls[5]))
            sql_str = '''INSERT INTO mega_millions VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

            execute_command(sql_str, data_tuple)

            index += 1

            list_balls = []

            if row_date == 'Tue, October, 17, 2017':
                date_in_range = False
                break            

        page_count += 1
        driver.close()
        web = "https://www.usamega.com/mega-millions/results/{}".format(page_count)

if __name__ == '__main__':
    main()