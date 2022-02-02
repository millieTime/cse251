"""
Course: CSE 251
Lesson Week: 09
File: team2.py

Purpose: team activity - Dining philosophers problem

Problem statement

Five silent philosophers sit at a round table with bowls of spaghetti. Forks
are placed between each pair of adjacent philosophers.

Each philosopher must alternately think and eat. However, a philosopher can
only eat spaghetti when they have both left and right forks. Each fork can be
held by only one philosopher and so a philosopher can use the fork only if it
is not being used by another philosopher. After an individual philosopher
finishes eating, they need to put down both forks so that the forks become
available to others. A philosopher can only take the fork on their right or
the one on their left as they become available and they cannot start eating
before getting both forks.  When a philosopher is finished eating, they think 
for a little while.

Eating is not limited by the remaining amounts of spaghetti or stomach space;
an infinite supply and an infinite demand are assumed.

The problem is how to design a discipline of behavior (a concurrent algorithm)
such that no philosopher will starve

Instructions:

        **************************************************
        ** DO NOT search for a solution on the Internet **
        ** your goal is not to copy a solution, but to  **
        ** work out this problem.                       **
        **************************************************

- This is the same problem as last team activity.  However, you will implement a waiter.  
  When a philosopher wants to eat, it will ask the waiter if it can.  If the waiter 
  indicates that a philosopher can eat, the philosopher will pick up each fork and eat.  
  There must not be a issue picking up the two forks since the waiter is in control of 
  the forks and when philosophers eat.  When a philosopher is finished eating, it will 
  informs the waiter that he/she is finished.  If the waiter indicates to a philosopher
  that they can not eat, the philosopher will wait between 1 to 3 seconds and try again.

- You have Locks and Semaphores that you can use.
- Remember that lock.acquire() has an argument called timeout.
- philosophers need to eat for 3 to 5 seconds when they get both forks.  
  When the number of philosophers has eaten MAX_MEALS times, stop the philosophers
  from trying to eat and any philosophers eating will put down their forks when finished.
- When a philosopher is not eating, it will think for 3 to 5 seconds.
- You want as many philosophers to eat and think concurrently.
- Design your program to handle N philosophers.
- Use threads for this problem.
- When you get your program working, how to you prove that no philosopher will starve?
  (Just looking at output from print() statements is not enough)
- Are the philosophers each eating and thinking the same amount?
- Using lists for philosophers and forks will help you in this program.
  for example: philosophers[i] needs forks[i] and forks[i+1] to eat


"""
import time
import threading
import random


PHILOSOPHERS = 5
MAX_MEALS = PHILOSOPHERS * 5

meals_eaten = 0

class Waiter(threading.Thread):
    eat_messages = []
    forks = []
    message_order = []
    current_index = 0
    philosopher_sems = []
    
    def __init__(self, philosopher_sems):
        super().__init__()
        self.eat_messages = [False] * PHILOSOPHERS
        self.forks = [True] * PHILOSOPHERS
        self.philosopher_sems = philosopher_sems
        self.current_index = 0

    def post_eat_message(self, philosopher_num):
        '''A philosopher is ready to eat something.'''
        self.eat_messages[philosopher_num] = True
    
    def run(self):
        '''Loop through the eat_messages and see who needs to eat'''
        global meals_eaten
        while meals_eaten < MAX_MEALS:
            if self.eat_messages[self.current_index]:
                # This philosopher wants to eat
                if self.forks[self.current_index] and self.forks[(self.current_index + 1) % len(self.forks)]:
                    self.philosopher_sems[self.current_index].release()
            else:
                # Go to the next philosopher.
                self.__get_next_index()
        for sem in self.philosopher_sems:
          sem.release()

    def __get_next_index(self):
      '''Figure out which index to go to next'''
      self.current_index += 2
      # Might need to shift an additional 1 position to offset on an even list.
      if len(self.eat_messages) % 2 != 1 and self.current_index > len(self.eat_messages):
          self.current_index += 1
      return self.current_index % len(self.eat_messages)
        
  

def eat(waiter, num, my_sem, meal_lock):
    #Tell the waiter you're ready to eat
    # acquire your semaphore
    # eat your food
    while True:
      waiter.post_eat_message(num)
      my_sem.acquire()
      global meals_eaten
      if meals_eaten >= MAX_MEALS:
        return
      with meal_lock:
          meals_eaten += 1
      time.sleep(random.random() * 2 + 3)

  

def main():
    # TODO - create the waiter (A class would be best here)
    
    # TODO - create the forks
    forks = []
    sems = []
    for i in range(PHILOSOPHERS):
        forks.append((f'fork {i}', threading.Lock()))
        sems.append(threading.Semaphore(0))
    fork_pairs = []
    for i, fork in enumerate(forks):
        pair = (fork, forks[(i + 1) % PHILOSOPHERS])
        fork_pairs.append(pair)
    
    meal_lock = threading.Lock()
    waiter = Waiter(sems)
    # TODO - create PHILOSOPHERS philosophers
    philos = []
    for philo_num in range(PHILOSOPHERS):
        philos.append(threading.Thread(target=eat, args=(waiter, philo_num, sems[philo_num], meal_lock)))#fork_pairs)))
    
    # TODO - Start them eating and thinking
    print("starting philosophers")
    for philosopher in philos:
      philosopher.start()
    print("starting waiter")
    waiter.start()
    # TODO - Display how many times each philosopher ate
    for philosopher in philos:
        philosopher.join()
    waiter.join()

if __name__ == '__main__':
    main()
