import time
# def add(x, y):
#     """Add Function"""
#     return x + y


# def multiply(x, y):
#     return x * y


# def division(x, y):
#     if y == 0:
#         raise ValueError('No No NO')
#     return x / y


# def do_two_things():
#     tn = 0
#     while(True):
#         tn=(1+tn)
#         print(tn)
# #         yield tn


# gen = do_two_things()

# next(gen)
# next(gen)
# next(gen)
# next(gen)

# import os


# def decorator_function(original_function):
#     def wrapper_func(*args, **kwargs):
#         print('result = {}'.format(original_function(*args)))
#         return original_function(*args, **kwargs)
#     return wrapper_func


# def rm(filename):
#     if os.path.isfile(filename):
#         os.remove(filename)


# def my_function(x):
#     if x == 0:
#         return 100
#     return x * 2


# class Calculator:

#     def sum(self, a, b):
#         time.sleep(3)
#         return a + b

from datetime import datetime

timestamps = [datetime(2014, 2, 11), datetime(2014, 2, 12), \
              datetime(2014, 2, 13)]

prices = [12, 2, 3]

for timestamp, price in zip(timestamps, prices):
    print(str(timestamp) + " price: " + str(price))
