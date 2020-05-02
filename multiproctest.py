import concurrent.futures
import multiprocessing
import time
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def do_something(thing):
    # time.sleep(0.01)
    df = pd.read_csv('./csvfile.csv')
    scaler = MinMaxScaler() 
    scaled_values = scaler.fit_transform(df) 
    df.loc[:,:] = scaled_values
    return len(df)
    # print(thing**3)

def use_concurrent(input_args):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # collected_results = []
        # results = [executor.submit(do_something, input_arg) for input_arg in input_args]
        # for f in concurrent.futures.as_completed(results):
        #     collected_results.append(f)
        # print(len(collected_results))
        '''Use map function instead. Map returns results in the order they were started.
        Context managers automatically join the processes.'''
        results = executor.map(do_something, input_args) # map returns results instead of future objects. 
        print(len(list(results)))

def use_multiprocessing(input_args):
    """Use multiprocessing. This really uses up all 4 cores. 
    The calculations need to be complex enough. e.g. read a csv of 100,000 rows"""
    processes=[]
    for input_arg in input_args:
        p = multiprocessing.Process(target=do_something, args=[input_arg])
        p.start()
        processes.append(p)

    for process in processes:
        process.join()

def use_linear(input_args):
    for input_arg in input_args:
        do_something(input_arg)


if __name__=='__main__':
    start = time.perf_counter()
    input_args = list(range(1000))
    # use_concurrent(input_args)
    use_linear(input_args)
    # use_multiprocessing(input_args)
    finish = time.perf_counter()
    print('finished in {:.2f} seconds'.format(finish-start))