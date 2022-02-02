"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

# -----------------------------------------------------------------------------
def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

# -----------------------------------------------------------------------------
def cleaner_cleaning(id):
    print(f'Cleaner {id}')
    time.sleep(random.uniform(0, 2))

# -----------------------------------------------------------------------------
def guest_waiting():
    time.sleep(random.uniform(0, 2))

# -----------------------------------------------------------------------------
def guest_partying(id):
    print(f'Guest {id}')
    time.sleep(random.uniform(0, 1))

# -----------------------------------------------------------------------------
def cleaner(my_id, cleaned_count, room_lock, done_cleaning):
    start_time = time.time()
    while time.time() < start_time + TIME:
        cleaner_waiting()
        with room_lock:
            print(STARTING_CLEANING_MESSAGE)
            cleaned_count.value += 1
            cleaner_cleaning(my_id) 
            print(STOPPING_CLEANING_MESSAGE)
        with done_cleaning:
            done_cleaning.notify_all()

    """
    #do the following for TIME seconds
    #cleaner will wait to try to clean the room (cleaner_waiting())
    get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """

# -----------------------------------------------------------------------------
def guest(my_id, party_count, room_lock, guest_count, done_cleaning):
    start_time = time.time()
    guest_waiting()
    while time.time() < start_time + TIME:
        while room_lock.acquire(block=False) or guest_count.value > 0:
            with guest_count.get_lock():
                if guest_count.value == 0:
                    print(STARTING_PARTY_MESSAGE)
                    party_count.value += 1
                guest_count.value += 1
            guest_partying(my_id)
            with guest_count.get_lock():
                if guest_count.value == 1:
                    print(STOPPING_PARTY_MESSAGE)
                    room_lock.release()
                guest_count.value -= 1
            guest_waiting()
        # Couldn't acquire room lock and no guests partying (That means there's a cleaner)
        # Big sad. Wait for them to be done I guess :/
        with done_cleaning:
            done_cleaning.wait()
    """
    do the following for TIME seconds
    guest will wait to try to get access to the room (guest_waiting())
    get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """

# -----------------------------------------------------------------------------
def main():
    # TODO - add any variables, data structures, processes you need
    cleaned_count, party_count, guest_count = mp.Value("i"), mp.Value("i"), mp.Value("i")
    cleaned_count.value, party_count.value, guest_count.value = 0, 0, 0
    room_lock = mp.Lock()
    done_cleaning = mp.Condition()
    # TODO - add any arguments to cleaner() and guest() that you need
    people = []
    for cleaner_id in range(CLEANING_STAFF):
        people.append(mp.Process(target=cleaner, args=(cleaner_id, cleaned_count, room_lock, done_cleaning)))
    for guest_id in range(HOTEL_GUESTS):
        people.append(mp.Process(target=guest, args=(guest_id, party_count, room_lock, guest_count, done_cleaning)))

    # Start time of the running of the program. 
    start_time = time.time()

    for person in people:
        person.start()
    for person in people:
        person.join()

    # Results
    print(f'Room was cleaned {cleaned_count.value} times, there were {party_count.value} parties')


if __name__ == '__main__':
    main()
