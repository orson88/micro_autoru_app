# micro_autoru_app
HOW TO USE
For Python 3.5+ install requirements.txt

If you dont have any apps laucnhed that are using default ports use this:
**streamlit run main.py (in terminal)**

If you do have other apps using some default ports, use this:
**streamlit run main.py --server.port <unused port number>** (in terminal)

Your default browser should be opened with the app
If not, copy and paste the address to your browser http://localhost:XXXX/ (where XXXX is the specified port number)

Project description:
This is my attempt to build a small analytical app for russian car marketplace auto.ru, which should help to check in with the current situation on the market, and help you get a car based just on the technical specifications

Project structure:
  1. main.py - the app itself, based around the streamlit syntax using the WITH clause
  2. data_process.py - parses and processes the data scraped from auto ru into a clean .csv
  3.data_scrape.py* - scrapes data from auto.ru
  4. sandbox.py - a to-be util scripts file
  5. dwn.py - a st8-forward solution for transferring data if for some reason u can not scrape the data 
  6. regress_analysis.py - a small model that helps get some (maybe) interesting numbers on the screen
  7. requirements.txt - list of reqs
  8. Dockerfile - my attempt to put this thing into Docker, but streamlit seems to be working very strangely with Docker so thats to be solved
  
Files that will apear on your device after launching:
  1. autoru_proj_data.pkl - pickeled json of data of the cars
  2. auto_data.csv - processed .csv data 
