import os
import json
import dbtools as db
from time import sleep

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

db_path = 'mega_millions.db'
hard_end_date = "Tue, September, 19, 2017"

global settings
settings = {}


def read_settings(settingsFilename='scrapeSettings.json'):
    '''
    scrape_config.json is expected to be a list. This function returns a list
    of test config objects.
    '''
    if not os.path.exists(settingsFilename):
        print ("{} doesn't exist, creating settings file".format(settingsFilename))
        settings = {
            "MegaMillions": [
                {
                  "endDate": hard_end_date,
                  "endIndex": 1
                }
            ]
        }
        write_settings(settings)
    else:
        with open(settingsFilename, 'r') as f:
            settings = json.load(f)

    return settings


def write_settings(json_settings, settingsFilename='scrapeSettings.json'):
    # writes the settings file once all of the website data has been scraped preserving the last processed
    # date and the last index value for writing new records. This helps reduce the information need to scrape
    # for each run

    if not os.path.exists(settingsFilename):
        with open(settingsFilename, "w") as f:
            json.dump(json_settings, f, indent=2)
    else:
        with open(settingsFilename, "w") as f:
            json.dump(json_settings, f, indent=2)

    
def main():
    web = 'https://www.usamega.com/mega-millions/results'
    
    # Set path if running in the container to local folder and not MAC
    path = os.getcwd()

    date_in_range = True
    first_pass = True

    # Find table by class name
    number_balls = []
    mega_balls = []
    list_balls = []

    # Create database file on first run
    if not os.path.isfile(db_path):
        # Create database and table to store the information
        sql_str = '''CREATE TABLE mega_millions (id INT PRIMARY KEY, draw_date TEXT NOT NULL,
            ball_1 INT, ball_2 INT, ball_3 INT, ball_4 INT, ball_5 INT, mega_ball INT);'''
        db.execute_command(db_path, sql_str)

        # Create database table DRAWS for future processing
        sql_str = '''CREATE TABLE draws (id INT PRIMARY KEY, ball_1 INT, ball_2 INT, ball_3 INT, ball_4 INT, ball_5 INT, mega_ball INT);'''
        db.execute_command(db_path, sql_str)

    # Load settings file info
    settings = read_settings()

    index = settings['MegaMillions'][0]['endIndex']
    end_date = settings['MegaMillions'][0]['endDate']

    # Latest results always start on page 1
    page_count = 1

    while date_in_range:
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(web)

        for i in range(1, 27):
            row_date = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[4]/table/tbody/tr[{}]/td[1]/section/a'.format(i)).text

            if first_pass:
                last_row_date = row_date
                first_pass = False

            print("Row Date - " + row_date)

            if end_date is None:
                end_date = hard_end_date

            if row_date == end_date:
                date_in_range = False
                break            

            for j in range(1, 7):
                list_balls.append(driver.find_element(By.XPATH, '/html/body/div[1]/main/div[4]/table/tbody/tr[{}]/td[1]/section/ul/li[{}]'.format(i, j)).text)

            # Insert data into the database
            index += 1
            data_tuple = (index, row_date, int(list_balls[0]), int(list_balls[1]),
                int(list_balls[2]), int(list_balls[3]), int(list_balls[4]), int(list_balls[5]))
            sql_str = '''INSERT INTO mega_millions VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

            db.execute_command(db_path, sql_str, data_tuple)

            list_balls = []

        page_count += 1
        driver.close()
        web = "https://www.usamega.com/mega-millions/results/{}".format(page_count)

    json_settings = {
        "MegaMillions": [
            {
                "endDate": last_row_date,
                "endIndex": index 
            }
        ]
    }
   
    write_settings(json_settings)

if __name__ == '__main__':
    main()
