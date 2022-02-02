"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- See in I-Learn

"""

import threading
import queue
import requests

# Include cse 251 common Python files
import os, sys
sys.path.append('../../code')   # Do not change the path.
from cse251 import *

RETRIEVE_THREADS = 4 # Default 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def url_retriever(url_queue, log, sem):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue
        sem.acquire()
        if not url_queue.empty():
            
        # TODO process the value retrieved from the queue
            value = url_queue.get()
            if value == NO_MORE_VALUES:
                url_queue.put(NO_MORE_VALUES)
                sem.release()
                break
        # TODO make Internet call to get characters name and log it
            response = requests.get(value)
            if response.status_code == 200:
                response = response.json()
            else:
                print("Request failed")
            log.write(response["name"])

def file_reader(url_queue, log, sem): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """

    # TODO Open the data file "data.txt" and place items into a queue
    # url_list = []
    with open("data.txt", "r") as infile:
        for line in infile:
            url_queue.put(line)
            sem.release()
    #     url_list = infile.read().split("\n")
    
    # for url in url_list:
    #     url_queue.put(url)

    log.write('finished reading file')

    # TODO signal the retrieve threads one more time that there are "no more values"
    url_queue.put(NO_MORE_VALUES)
    sem.release()

def main():
    """ Main function """

    log = Log(show_terminal=True)

    # TODO create queue
    q = queue.Queue()
    # TODO create semaphore (if needed)
    sem = threading.Semaphore(RETRIEVE_THREADS)
    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job
    file_reader_thread = threading.Thread(target = file_reader, args=(q,log,sem))
    retriever_threads = []
    for count in range(RETRIEVE_THREADS):
        retriever_threads.append(threading.Thread(target= url_retriever, args=(q,log,sem)))
    log.start_timer()

    # TODO Get them going - start the retrieve_threads first, then file_reader
    for thread in retriever_threads:
        thread.start()
    file_reader_thread.start()
    file_reader_thread.join()
    for thread in retriever_threads:
        thread.join()
    log.stop_timer('Time to process all URLS')

if __name__ == '__main__':
    main()