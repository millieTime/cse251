"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: Preston Millward

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included
- Each thread requires a different color by calling get_color()


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

One way that would work would be to use threaded classes where each thread
keeps track of its parent thread, the spot its parent was on when the new
thread was created, whether it found the end, and its own path in a list -
just from its individual start to where it ends. When it spawns off another
thread, it passes that child thread where the the current thread was when it
spawned it, and a reference to the current thread. Then when a thread finds the
end, it can create a master list and follow this recursive process:
1. If you have a parent thread, call this function in their class with
arguments of where they created you (so they stop appending their moves at that
point) and the master list (so they can append to it).
2. Append each of your steps to the master list, stopping at the given spawn
point (inclusive) OR the end of the maze.
That finishing thread could either write that master list to a global variable,
or it could just hold on to it.
When all threads are joined, I can either access that global variable, or loop
through the list of threads to find the one that found the end and get the
master list from it.

Why would it work?

Each thread knows where it started and where it ends. Each thread also knows
where its parent was when it was created. Any part of the parent's path list
past that point is irrelevant and needs removed when the end is found. By
stitiching together each of those partial paths, the overall path from
beginning to end can be obtained.
"""
import math
import threading
import cv2
import os

# Include cse 251 common Python files - Dont change
from baseCode.cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)

# Globals
current_color_index = 0
thread_count = 0
stop = False

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color

def thread_move(pos, color, maze, maze_lock):
    with maze_lock:
        if maze.can_move_here(pos[0], pos[1]):
            maze.move(pos[0], pos[1], color)
            return True
        return False

def thread_solve(pos, color, maze, maze_lock, thread_list):
    global stop
    if stop or not thread_move(pos, color, maze, maze_lock):
        return
    if maze.at_end(pos[0], pos[1]):
        print("Found end!")
        stop = True
        return
    while True:
        moves = maze.get_possible_moves(pos[0], pos[1])
        first_move = True
        for move in moves:
            if first_move:
                # If we can take this first move, take it.
                if stop:
                    return
                can_move = thread_move(move, color, maze, maze_lock)
                if can_move:
                    pos = move
                    first_move = False
                    if maze.at_end(pos[0], pos[1]):
                        stop = True
                        return
            else:
                thread = threading.Thread(target = thread_solve, args=(move, get_color(), maze, maze_lock, thread_list))
                thread.start()
                thread_list.append(thread)
        # It went through without making any moves.
        if first_move:
            return

def solve_find_end(maze):
    """ finds the end position using threads.  Nothing is returned """
    global stop
    stop = False
    # When one of the threads finds the end position, stop all of them
    maze_lock = threading.Lock()
    thread_list = []
    thread = threading.Thread(target = thread_solve, args=(maze.get_start_pos(), get_color(), maze, maze_lock, thread_list))
    thread.start()
    thread_list.append(thread)
    for thread in thread_list:
        thread.join()
    global thread_count 
    thread_count = len(thread_list)

def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    dir = os.path.dirname(__file__)
    for filename, delay in files:
        filename = dir + "/resources/mazes/"+filename
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()