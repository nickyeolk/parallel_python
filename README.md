# experiments in parallel processing in python.
Following instructions from https://www.youtube.com/watch?v=fKl2JW_qrso  
In general, you want multithreading for IO bound tasks, and multiprocessing for CPU bound taks.  
As simple as `with concurrent.futures.ThreadPoolExecutor() as executor:` vs 
`with concurrent.futures.ProcessPoolExecutor() as executor:`  
With Multiprocess: 65.52 secs.  
With Multithread: 88.57 secs.  
With Linear: 89.67 secs.
