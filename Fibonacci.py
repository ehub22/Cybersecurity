import time
import math

numbers = [0, 1]


def calc_fib(size):
    start = time.time()
    global numbers
    x = 1
    while x <= size:
        new_value = numbers[x-1]+numbers[x]
        numbers.append(new_value)
        print(new_value)
        x += 1
    elapsed = time.time()-start
    # print("Elapsed Time: " + str(ciel(elapsed)))

calc_fib(500)
