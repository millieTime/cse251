"""
Course: CSE 251
Lesson Week: 08
File: team.py
Instructions:
- Look for TODO comments
"""

import time
import random
import threading
import multiprocessing as mp

# Include cse 251 common Python files - Dont change
from baseCode.cse251 import *

# -----------------------------------------------------------------------------
# Python program for implementation of MergeSort
# https://www.geeksforgeeks.org/merge-sort/
def merge_sort(arr):

    # base case of the recursion - must have at least 2+ items
    if len(arr) > 1:
 
         # Finding the mid of the array
        mid = len(arr) // 2
 
        # Dividing the array elements
        L = arr[:mid]
 
        # into 2 halves
        R = arr[mid:]
 
        # Sorting the first half
        merge_sort(L)
 
        # Sorting the second half
        merge_sort(R)
 
        i = j = k = 0
 
        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
 
        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
 
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

# -----------------------------------------------------------------------------
def is_sorted(arr):
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))


# -----------------------------------------------------------------------------
def merge_normal(arr):
    merge_sort(arr)


# -----------------------------------------------------------------------------
def merge_sort_thread(arr, start, end):
    # TODO - Add your code here to use threads.  Each time the merge algorithm does a recursive
    #        call, you need to create a thread to handle that call
     # base case of the recursion - must have at least 2+ items
    if end - start > 1:
         # Finding the mid of the array
        mid = (end - start) // 2 + start
 
        # Dividing the array elements
        L_start = start
        L_end = mid
 
        # into 2 halves
        R_start = mid
        R_end = end
 
        # Sorting the first half
        thread_left = threading.Thread(target = merge_sort_thread, args= (arr, L_start, L_end))
        # merge_sort_thread(arr, L_start, L_end)
        
        # Sorting the second half
        thread_right = threading.Thread(target = merge_sort_thread, args = (arr, R_start, R_end))
        # merge_sort_thread(arr, R_start, R_end)
        
        thread_left.start()
        thread_left.join()
        thread_right.start()
        thread_right.join()
        
        k = 0
 
        # Copy data to temp arrays L[] and R[]
        temp = [0] * (end - start)
        while L_start < L_end and R_start < R_end:
            if arr[L_start] < arr[R_start]:
                temp[k] = arr[L_start]
                L_start += 1
            else:
                temp[k] = arr[R_start]
                R_start += 1
            k += 1
 
        # Checking if any element was left
        while L_start < L_end:
            temp[k] = arr[L_start]
            L_start += 1
            k += 1
 
        while R_start < R_end:
            temp[k] = arr[R_start]
            R_start += 1
            k += 1

        for element in temp:
            arr[start] = element
            start += 1
    

# -----------------------------------------------------------------------------
def merge_sort_process(arr, start, end):
    # TODO - Add your code here to use threads.  Each time the merge algorithm does a recursive
    #        call, you need to create a process to handle that call
    if end - start > 1:
         # Finding the mid of the array
        mid = (end - start) // 2 + start
 
        # Dividing the array elements
        L_start = start
        L_end = mid
 
        # into 2 halves
        R_start = mid
        R_end = end
 
        # Sorting the first half
        process_left = mp.Process(target = merge_sort_process, args= (arr, L_start, L_end))
        # merge_sort_thread(arr, L_start, L_end)
        
        # Sorting the second half
        process_right = mp.Process(target = merge_sort_process, args = (arr, R_start, R_end))
        # merge_sort_thread(arr, R_start, R_end)
        
        process_left.start()
        process_left.join()
        process_right.start()
        process_right.join()
        
        k = 0
 
        # Copy data to temp arrays L[] and R[]
        temp = [0] * (end - start)
        while L_start < L_end and R_start < R_end:
            if arr[L_start] < arr[R_start]:
                temp[k] = arr[L_start]
                L_start += 1
            else:
                temp[k] = arr[R_start]
                R_start += 1
            k += 1
 
        # Checking if any element was left
        while L_start < L_end:
            temp[k] = arr[L_start]
            L_start += 1
            k += 1
 
        while R_start < R_end:
            temp[k] = arr[R_start]
            R_start += 1
            k += 1

        for element in temp:
            arr[start] = element
            start += 1


# -----------------------------------------------------------------------------
def main():
    merges = [
        (merge_sort, ' Normal Merge Sort '), 
        (lambda arr: merge_sort_thread(arr, 0, len(arr)), ' Threaded Merge Sort '), 
        (merge_sort_process, ' Processes Merge Sort ')
    ]

    for merge_function, desc in merges:
        # Create list of random values to sort
        arr = [random.randint(1, 10000000) for _ in range(100000)]

        print(f'\n{desc:-^90}')
        print(f'Before: {str(arr[:5])[1:-1]} ... {str(arr[-5:])[1:-1]}')
        start_time = time.perf_counter()

        merge_function(arr)

        end_time = time.perf_counter()
        print(f'Sorted: {str(arr[:5])[1:-1]} ... {str(arr[-5:])[1:-1]}')

        print('Array is sorted' if is_sorted(arr) else 'Array is NOT sorted')
        print(f'Time to sort = {end_time - start_time}')


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()

