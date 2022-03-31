from email.mime import base
import random
import time
from numpy import byte

s = "123"
if len(s) < 10:
    s = "0" * (10 - len(s)) + s
print(s)

b = b"123"
print(len(b))
 
print("12312".count("12"))