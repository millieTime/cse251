"""
Course: CSE 251
Lesson Week: Week 07
File: team.py
Purpose: Week 05 Team Activity

Instructions:

- Make a copy of your assignment 2 program.  Since you are working in a team,
  you can design which assignment 2 program that you will use for the team
  activity.
- Convert the program to use a process pool and use apply_async() with a
  callback function to retrieve data from the Star Wars website.

The call to TOP_API_URL will return the following Dictionary.  Do NOT have this
dictionary hard coded - use the API call to get this dictionary.  Then you can
use this dictionary to make other API calls for data.

{
   "people": "http://swapi.dev/api/people/", 
   "planets": "http://swapi.dev/api/planets/", 
   "films": "http://swapi.dev/api/films/",
   "species": "http://swapi.dev/api/species/", 
   "vehicles": "http://swapi.dev/api/vehicles/", 
   "starships": "http://swapi.dev/api/starships/"
}

------------------------------------------------------------------------------
"""

from datetime import datetime, timedelta
import requests
import json
import threading
import multiprocessing as mp

# Include cse 251 common Python files
from baseCode.cse251 import *

# Const Values
TOP_API_URL = r'https://swapi.dev/api'

call_count = 0

# TODO Add your threaded class definition here
class Requester(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.data = response.json()
        else:
            print("Request failed:", self.url)
            self.data = False

# TODO Add any functions you need here
def start_thread_list(urls):
    thread_list = [Requester(url) for url in urls]
    data_list = []
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
        # get the data from threads
        data_list.append(thread.data["name"] if thread.data else "ERROR")
    # return a list of data
    return data_list

def write_data(log, data_list, name):
    # update call count
    global call_count
    call_count += len(data_list)
    log.write(f"{name}: {len(data_list)}")
    log.write(", ".join(sorted(data_list)))
    log.write("")

def error_callback(exception):
  print('bad juju:', exception)

def main():
    global call_count
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from swapi.dev')
    # TODO Retrieve Top API urls
    top_requester = Requester(TOP_API_URL)
    top_requester.start()
    call_count += 1
    top_requester.join()
    if not top_requester.data:
        return

    film_requester = Requester(top_requester.data["films"])
    film_requester.start()
    call_count += 1
    film_requester.join()
    if not film_requester.data:
        return

    film_6 = film_requester.data["results"][5]

    log.write("----------------------------------------")
    log.write(f'Title   : {film_6["title"]}')
    log.write(f'Director: {film_6["director"]}')
    log.write(f'Producer: {film_6["producer"]}')
    log.write(f'Released: {film_6["release_date"]}')
    log.write("")
    
    # Create and start other threads before dealing with current data for maximum time savings.
    # async pool stuff
    pool = mp.Pool(5)
    pool.apply_async(start_thread_list, args=(film_6["characters"],), callback=lambda results: write_data(log, results, "Characters"), error_callback=error_callback)
    pool.apply_async(start_thread_list, args=(film_6["planets"],), callback=lambda results: write_data(log, results, "Planets"), error_callback=error_callback)
    pool.apply_async(start_thread_list, args=(film_6["starships"],), callback=lambda results: write_data(log, results, "Starships"), error_callback=error_callback)
    pool.apply_async(start_thread_list, args=(film_6["vehicles"],), callback=lambda results: write_data(log, results, "Vehicles"), error_callback=error_callback)
    pool.apply_async(start_thread_list, args=(film_6["species"],), callback=lambda results: write_data(log, results, "Species"), error_callback=error_callback)
    
    pool.close()
    pool.join()
  
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to swapi server')
    

if __name__ == "__main__":
    main()