from concurrent.futures import TimeoutError
import time
import os
import logging
import itertools
from pebble import ProcessPool, ProcessExpired
from sklearn.base import BaseEstimator, TransformerMixin

class RandoClass(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.status = 1
    def fit(self, X, y=None):
        return self
    def predict(self):
        return self.status

def function(n, argument, log_level=logging.INFO):
    print(str(os.getpid()), 'working on ', n)
    logname = str(os.getpid())+'.log'
    logging.basicConfig(level = log_level, handlers=[logging.FileHandler(logname, 'a', 'utf-8')])
    logging.info('print this to log %s, %s', n, argument)
    time.sleep(n)
    return n

def main():
    range_list = list(range(10))
    range_list.extend(range(10,0,-1))
    randoclass = RandoClass()
    with ProcessPool() as pool:
        future = pool.map(function, range_list, itertools.repeat(randoclass), \
                timeout=5)
    
        iterator = future.result()
        all_results = []
        while True:
            try:
                result = next(iterator)
                all_results.append(result)
            except StopIteration:
                break
            except TimeoutError as error:
                print("function took longer than %d seconds" % error.args[1])
            except ProcessExpired as error:
                print("%s. Exit code: %d" % (error, error.exitcode))
            except Exception as error:
                print("function raised %s" % error)
                print(error.traceback)  # Python's traceback of remote process
    return all_results

if __name__=='__main__':
    all_results = main()
    print(all_results)
