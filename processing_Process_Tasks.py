"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: Preston Millward
Purpose: Process Task Files

Instructions:  See I-Learn

So I threw in some print statements in each append_ function, and the tasks
that take the longest to complete are 'prime', 'name', and 'search'. So I took
out the prints for 'sum' and 'upper' and messed around with different amounts
of processes for those three tasks. Here they are, sorted by slowest to
fastest time.
|Primes | Words | Names | Time |
|-------|-------|-------|------|
|   1   |   2   |   5   | 15.6 | 
|   1   |   4   |   3   | 15.6 |
|   1   |   3   |   4   | 15.0 | 
|   4   |   5   |   6   | 12.0 | 
|   2   |   3   |   5   | 11.7 |
|   2   |   3   |   6   | 11.4 |
|   3   |   5   |   6   | 11.3 | 
|   3   |   5   |   5   | 11.0 | 
|   3   |   4   |   6   | 10.8 | 
So according to my experiments, allocating 3 processes to the Primes task,
4 to the Words task, 6 to the Names task, and one to the others is quickest.
"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from baseCode.cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
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
 
def task_prime(task):
    value = task["value"]
    if is_prime(value):
        return f'{value} is prime'
    else:
        return f'{value} is not prime'
        
def append_prime(phrase):
    #print("p")
    result_primes.append(phrase)

def task_word(task):
    word = task["word"] + "\n"
    with open("resources/words.txt", "r") as infile:
        for line in infile:
            if word == line:
                return f'{word[:-1]} Found'
    return f'{word[:-1]} not found'
    
def append_word(phrase):
    #print(" w")
    result_words.append(phrase)

def task_upper(task):
    text = task["text"]
    return f'{text} ==> {text.upper()}'
    
def append_upper(phrase):
    #print("  u")
    result_upper.append(phrase)

def task_sum(task):
    start_value, end_value = task["start"], task["end"]
    total = (start_value + end_value - 1) * (end_value - start_value) / 2
    return f'sum of {start_value} to {end_value} = {int(total)}'
    
def append_sum(phrase):
    #print("   s")
    result_sums.append(phrase)

def task_name(task):
    url = task["url"]
    response = requests.get(url)
    if response.status_code == 200:
        return f'{url} has name {response.json()["name"]}'
    else:
        return f'{url} had an error receiving the information'
        
def append_name(phrase):
    #print("    n")
    result_names.append(phrase)

def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    # prime word upper sum name
    task_types = [TYPE_PRIME, TYPE_WORD, TYPE_UPPER, TYPE_SUM, TYPE_NAME]
    p_sizes = [3, 4, 1, 1, 6]
    p_functions = [task_prime, task_word, task_upper, task_sum, task_name]
    p_callbacks = [append_prime, append_word, append_upper, append_sum, append_name]
    p_list = [mp.Pool(size) for size in p_sizes]

    count = 0
    task_files = glob.glob("resources/tasks/*.task")
    for filename in task_files:
        task = load_json_file(filename)
        print(task)
        count += 1
        index = -1
        try:
            index = task_types.index(task['task'])
        except ValueError:
            log.write(f'Error: unknown task type {task["task"]}')
        if index >= 0:
            p_list[index].apply_async(p_functions[index], args=(task,), callback = p_callbacks[index])

    # TODO start and wait pools
    for pool in p_list:
        pool.close()
        pool.join()

    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Primes: {len(result_primes)}')
    log.write(f'Words: {len(result_words)}')
    log.write(f'Uppercase: {len(result_upper)}')
    log.write(f'Sums: {len(result_sums)}')
    log.write(f'Names: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    main()
