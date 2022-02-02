"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Me, you, and our dog, Blue.

Purpose: Check for prime values

Instructions:

- You can't use thread/process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
import time
import threading
import multiprocessing as mp
import random

#Include cse 251 common Python files
from baseCode.cse251 import *

PRIME_PROCESS_COUNT = 3

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_tes
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# TODO create read_thread function
def read_thread(filename: str, queue: mp.Queue, sem: mp.Semaphore):
    with open(filename, 'r') as infile:
        for line in infile:
            queue.put(int(line))
            sem.release()
    for process in range(PRIME_PROCESS_COUNT):
        queue.put(None)
        sem.release()
    
# TODO create prime_process function
def prime_process(queue, lst, sem):
    while True:
        sem.acquire()
        if (item:= queue.get()):
            if is_prime(item):
                lst.append(item)
        else:
            break

def create_data_txt(filename):
    with open(filename, 'w') as f:
        for _ in range(1000):
            f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    filename = 'data.txt'

    # Once the data file is created, you can comment out this line
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    # mangers?
    numbers = mp.Queue()
    primes = mp.Manager().list()
    sem = mp.Semaphore(0)
    
    # TODO create reading thread
    r_thread = threading.Thread(target=read_thread, args=(filename, numbers, sem))

    # TODO create prime processes
    processes = []
    for _ in range(PRIME_PROCESS_COUNT):
        processes.append(mp.Process(target=prime_process, args=(numbers, primes, sem)))
    # TODO Start them all
    r_thread.start()
    for process in processes:
        process.start()
    # TODO wait for them to complete
    r_thread.join()
    for process in processes:
        process.join()

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()