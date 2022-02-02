/* ---------------------------------------
Course: CSE 251
Lesson Week: ?12
File: team.go
Author: Brother Comeau

Purpose: team activity - finding primes

Instructions:

- Process the array of numbers, find the prime numbers using goroutines

worker()

This goroutine will take in a list/array/channel of numbers.  It will place
prime numbers on another channel


readValue()

This goroutine will display the contents of the channel containing
the prime numbers

--------------------------------------- */
package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

func isPrime(n int) bool {
	// Primality test using 6k+-1 optimization.
	// From: https://en.wikipedia.org/wiki/Primality_test

	if n <= 3 {
		return n > 1
	}

	if n%2 == 0 || n%3 == 0 {
		return false
	}

	i := 5
	for (i * i) <= n {
		if n%i == 0 || n%(i+2) == 0 {
			return false
		}
		i += 6
	}
	return true
}

// ch <-chan T ; Syntax for receive only channel
// ch chan<- T ; Syntax for send only channel
func worker(ch_in <-chan int, ch_out chan<- int, wg *sync.WaitGroup) {
	// TODO - process numbers on one channel and place prime number on another
	for {
		next_num := <-ch_in
		if next_num == -1 {
			wg.Done()
			return
		} else if isPrime(next_num) {
			ch_out <- next_num
		}
	}
}

// ch <-chan T ; Syntax for receive only channel
func readValues(ch_in <-chan int) {
	// TODO -Display prime numbers from a channel
	for {
		next_prime := <-ch_in
		if next_prime == -1 {
			return
		} else {
			fmt.Println(next_prime)
		}
	}
}

func main() {

	workers := 10
	numberValues := 100

	ch_nums := make(chan int)
	ch_primes := make(chan int)
	wg := &sync.WaitGroup{}

	// create workers
	wg.Add(workers)
	for w := 1; w <= workers; w++ {
		go worker(ch_nums, ch_primes, wg) // Add any arguments
	}

	go readValues(ch_primes) // Add any arguments

	rand.Seed(time.Now().UnixNano())
	for i := 0; i < numberValues; i++ {
		z := rand.Int()
		ch_nums <- z
	}

	for i := 0; i < workers; i++ {
		ch_nums <- -1
	}
	
	//Signal we're done (╯°□°）╯︵ ┻━┻
	wg.Wait()
	ch_primes <- -1

	fmt.Println("All Done!")
}
