from email.mime import base
import random
import time
from numpy import byte

blist = []

blist.append(b'123')
blist.append(b'123')
blist.append(b'123')

print(len(blist))
print(b''.join(blist))

blist.clear()
print(blist)