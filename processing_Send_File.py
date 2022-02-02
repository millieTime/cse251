"""
Course: CSE 251
Lesson Week: 06
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe

After you can copy a text file word by word exactly
- Change the program to be faster (Still using the processes)

"""

import multiprocessing as mp
from multiprocessing import Value, Process
import filecmp
from multiprocessing import connection 

# Include cse 251 common Python files
from baseCode.cse251 import *

def sender(birth, count, book_of_life):
    """ function to send messages to other end of pipe """
    '''
    open the file
    send all contents of the file over a pipe to the other process
    Note: you must break each line in the file into words and
          send those words through the pipe
    '''
    with open(book_of_life, 'r') as book:

        #for line in book.readlines():
        lines = book.read()
            # words = line[:-1].split(" ")
            # for word in words:
        count.value += 1
        birth.send(lines)
        # birth.send("\n")
    # Done, so let the receiver know we're done
    birth.send(None)
        
def receiver(death, book_of_death):
    """ function to print the messages received from other end of pipe """
    ''' 
    open the file for writing
    receive all content through the shared pipe and write to the file
    Keep track of the number of items sent over the pipe
    '''
    with open(book_of_death, 'w') as book:
        #word_list = []
        while True:
            word = death.recv()
            if word == None:
                # We're done writing.
                return
            # elif word == "\n":
            #     # package the list of words and write it.
            #     line = " ".join(word_list) + "\n"
            #     word_list.clear()
            #     book.write(line)
            else:
                # word_list.append(word)
                book.write(word)
            
def are_files_same(filename1, filename2):
    """ Return True if two files are the same """
    return filecmp.cmp(filename1, filename2, shallow = False) 


def copy_file(log, filename1, filename2):
    # TODO create a pipe 
    birth, death = mp.Pipe()
    # TODO create variable to count items sent over the pipe
    count = mp.Value('i', 0)
    # TODO create processes
    reader = mp.Process(target=sender,args = (birth, count, filename1))
    writer = mp.Process(target=receiver, args=(death, filename2))

    log.start_timer()
    start_time = log.get_time()

    # TODO start processes 
    reader.start()
    writer.start()
    # TODO wait for processes to finish
    reader.join()
    writer.join()

    stop_time = log.get_time()

    log.stop_timer(f'Total time to transfer content = {stop_time - start_time}: ')
    log.write(f'items / second = {count.value / (stop_time - start_time)}')

    if are_files_same(filename1, filename2):
        log.write(f'{filename1} - Files are the same')
    else:
        log.write(f'{filename1} - Files are different')


if __name__ == "__main__": 

    log = Log(show_terminal=True)

    # copy_file(log, 'gettysburg.txt', 'gettysburg-copy.txt')
    
    # After you get the gettysburg.txt file working, uncomment this statement
    copy_file(log, 'resources/bom.txt', 'resources/bom-copy.txt')

