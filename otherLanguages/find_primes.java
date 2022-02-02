// TODO Auto-generated method stub
		/************************************
		Course: cse 251
		File: team1.java
		Week: week 11 - team activity 1

		Instructions:

		- Main contains an array of 1,000 random values.  You will be creating
		  threads to process this array.  If you find a prime number, display
		  it to the console.

		- DON'T copy/slice the array in main() for each thread.

		Part 1:
		- Create a class that is a sub-class of Thread.
		- create 4 threads based on this class you created.
		- Divide the array among the threads.

		Part 2:
		- Create a class on an interface or Runnable
		- create 4 threads based on this class you created.
		- Divide the array among the threads.

		Part 3:
		- Modify part1 or part 2 to handle any size array and any number
		  of threads.

		************************************/

    import java.util.Random; 
    import java.lang.Math;
    
    public class ParAndConc {
      static boolean isPrime(int n){ 
            // Corner cases 
            if (n <= 1) return false; 
            if (n <= 3) return true; 
          
            // This is checked so that we can skip  
            // middle five numbers in below loop 
            if (n % 2 == 0 || n % 3 == 0) return false; 
          
            for (int i = 5; i * i <= n; i = i + 6) 
              if (n % i == 0 || n % (i + 2) == 0) 
                return false; 
          
            return true; 
        }
    
      public static void main(String[] args) {
        int num_threads = 4;
          // create instance of Random class 
          Random rand = new Random(); 
      
          int count = 1000;
          int[] array = new int[count];
          for (int i = 0; i < count; i++){
            array[i] = Math.abs(rand.nextInt());
          }
          
          int prime_count = 0;
          
          MyThread[] thread_array = new MyThread[num_threads];
          //Thread[] thread_array = new Thread[num_threads];
          //MyRunnable[] run_array = new MyRunnable[num_threads];
          
          for (int i = 0; i < num_threads; i++) {
            
            thread_array[i] = new MyThread(array, i, num_threads);
            //run_array[i] = new MyRunnable(array, i, num_threads);
            //thread_array[i] = new Thread(run_array[i]);
            
            thread_array[i].start();
          }
          for (int i = 0; i < num_threads; i++) {
            try {
              thread_array[i].join();
              
              prime_count += thread_array[i].get_count();
              //prime_count += run_array[i].get_count();
                  
          } catch (InterruptedException e) {
            e.printStackTrace();
          }
          }
          System.out.println("Finished");
          System.out.println("Found " + String.valueOf(prime_count) + " primes.");
      }
    
    }    