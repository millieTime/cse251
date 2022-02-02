"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: Preston Millward

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receives numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  Display the numbers received by printing them to the console.

- Create 2 writer processes

- Create 2 reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s) or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

Add any comments for me:

$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
I was a unsure of whether the shared list was not allowed to be longer than BUFFER_SIZE or if
the list's length was BUFFER_SIZE * number_of_writers. I decided on the tougher interpretation.
I think there was one other thing, but I can't remember.
Oh - I have the two writers writing consecutively independently of each other, but they aren't
consecutive together. I figured ensuring that the output was exactly consecutive would remove
enough parallelism to make it unnecessary. But I can edit this code so that the output is every
number from 0 to items_to_send in the correct order if that's what you're looking for
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

"""
import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp
import time

BUFFER_SIZE = 10

def read(can_add, can_take, lst, i_width, i0):
  values_read = 0
  current_i = i0
  while True:
    can_take.acquire()
    n = lst[current_i]
    can_add.release()
    if n == -1:
      break
    print(n)
    values_read += 1
    current_i += 1
    if current_i >= i0 + i_width:
      current_i = i0
  lst[i0] = values_read

def write(can_add, can_take, lst, i_width, i0, n_max, n_step, n0):
  current_i = i0
  current_n = n0
  while current_n < n_max:
    can_add.acquire()
    lst[current_i] = current_n
    can_take.release()
    time.sleep(.0001)
    current_n += n_step
    current_i += 1
    if current_i >= i0 + i_width:
      current_i = i0
  can_add.acquire()
  lst[current_i] = -1
  can_take.release()


def main():

    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(1000, 10000)

    smm = SharedMemoryManager()
    smm.start()

    # TODO - Create a ShareableList to be used between the processes
    lst = smm.ShareableList(range(BUFFER_SIZE + 1))
    print(lst)
    # TODO - Create any lock(s) or semaphore(s) that you feel you need
    can_add1 = mp.Semaphore(BUFFER_SIZE // 2)
    can_take1 = mp.Semaphore(0)
    can_add2 = mp.Semaphore(BUFFER_SIZE // 2)
    can_take2 = mp.Semaphore(0)
    # TODO - create reader and writer processes
    width = BUFFER_SIZE // 2
    reader1 = mp.Process(target=read, args=(can_add1, can_take1, lst, width, 0))
    writer1 = mp.Process(target=write, args=(can_add1, can_take1, lst, width, 0, items_to_send, 2, 0))
    reader2 = mp.Process(target=read, args=(can_add2, can_take2, lst, width, width))
    writer2 = mp.Process(target=write, args=(can_add2, can_take2, lst, width, width, items_to_send, 2, 1))
    # TODO - Start the processes and wait for them to finish
    writer1.start()
    writer2.start()
    reader1.start()
    reader2.start()
    writer1.join()
    writer2.join()
    reader1.join()
    reader2.join()
    print(f'{items_to_send} values sent')

    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    # print(f'{<your variable>} values received')
    print(f'{lst[0] + lst[BUFFER_SIZE // 2]} values received in total')
    print(f'{lst[0]} values received by reader1')
    print(f'{lst[BUFFER_SIZE // 2]} values received by reader2')
    smm.shutdown()

if __name__ == '__main__':
    main()
