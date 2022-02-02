"""
Course: CSE 251
Lesson Week: 10
File: team2.py
Author: Brother Comeau
Instructions:
- Look for the TODO comments
"""

import time
import threading
import mmap

# -----------------------------------------------------------------------------
def swapchars ():
    pass

def reverse_file(filename):
    """ Display a file in reverse order using a mmap file. """
    with open(filename, mode="r+", encoding="utf8") as infile:
        with mmap.mmap(infile.fileno(), length=0, access=mmap.ACCESS_WRITE) as map_file:
            for index in range((map_file.size() - 1)//2):
                map_file[index], map_file[-index - 1] = map_file[-index - 1], map_file[index]

# -----------------------------------------------------------------------------
def promote_letter_a(filename):
    """ 
    change the given file with these rules:
    1) when the letter is 'a', uppercase it
    2) all other letters are changed to the character '.'

    You are not creating a different file.  Change the file using mmap file.
    """
    with open(filename, mode="r+", encoding="utf8") as infile:
        with mmap.mmap(infile.fileno(), length=0, access=mmap.ACCESS_WRITE) as map_file:
            for index in range(map_file.size()):
                if map_file[index] == ord("a"):
                    map_file[index] = ord("A")
                else:
                    map_file[index] = ord(".")

# -----------------------------------------------------------------------------
def promote_letter_a_threads(filename):
    """ 
    change the given file with these rules:
    1) when the letter is 'a', uppercase it
    2) all other letters are changed to the character '.'

    You are not creating a different file.  Change the file using mmap file.

    Use N threads to process the file where each thread will be 1/N of the file.
    """
    # TODO add code here
    pass


# -----------------------------------------------------------------------------
def main():
    # reverse_file('resources/data.txt')
    promote_letter_a('resources/letter_a.txt')
    
    # TODO
    # When you get the function promote_letter_a() working
    #  1) Comment out the promote_letter_a() call
    #  2) run create_Data_file.py again to re-create the "letter_a.txt" file
    #  3) Uncomment the function below
    # promote_letter_a_threads('resources/letter_a.txt')

if __name__ == '__main__':
    main()
