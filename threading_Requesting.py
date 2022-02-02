"""
------------------------------------------------------------------------------
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau and Preston Millward

Purpose: Retrieve Star Wars details from a website

Instructions:

- Review instructions in I-Lean for this assignment.

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

# Include cse 251 common Python files
from baseCode.cse251 import *

# Const Values
TOP_API_URL = r'https://swapi.dev/api'

# Global Variables
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
    for thread in thread_list:
        thread.start()
    return thread_list

def write_data(log, thread_list, name):
    global call_count
    call_count += len(thread_list)
    log.write(f"{name}: {len(thread_list)}")
    for thread in thread_list:
        thread.join()
    log.write(", ".join(sorted([thread.data["name"] if thread.data else "ERROR" for thread in thread_list])))
    log.write("")

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

    # Create and start other threads before dealing with current data for maximum time savings.
    
    character_threads = start_thread_list(film_6["characters"])
    planet_threads = start_thread_list(film_6["planets"])
    starship_threads = start_thread_list(film_6["starships"])
    vehicle_threads = start_thread_list(film_6["vehicles"])
    specie_threads = start_thread_list(film_6["species"])

    log.write("----------------------------------------")
    log.write(f'Title   : {film_6["title"]}')
    log.write(f'Director: {film_6["director"]}')
    log.write(f'Producer: {film_6["producer"]}')
    log.write(f'Released: {film_6["release_date"]}')
    log.write("")

    write_data(log, character_threads, "Characters")
    write_data(log, planet_threads, "Planets")
    write_data(log, starship_threads, "Starships")
    write_data(log, vehicle_threads, "Vehicles")
    write_data(log, specie_threads, "Species")
    
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to swapi server')
    

if __name__ == "__main__":
    main()
