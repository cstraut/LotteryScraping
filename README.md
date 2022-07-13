This is a simple project that demonstrates the ability to scrape a website using Python

The website used contains the past results for the Lottery drawings (Both Powerball and Mega Millions). This version of the app is simply to scrape the Mega Millions history and store the data in a SQLite3 database for running queries against those results. The app only goes back as far as the current ball numbering format which began on October 17, 2017.

I am working on adding a configuration file that can be used to set which fields to scrape as well storing the last date the scraping occurred so that future runs only scrape the new results since the last run. The configuration file will also contain the URL to scrape such that I could specify the Powerball results instead of the Mega Millions results.

The app could be easily modified to include Powerball results as well.

The app can run on a local machine but this is getting built to execute inside a container using docker. The Dockerfile will pull the base image and add packages and other binary files to assist with the screenscraping.
