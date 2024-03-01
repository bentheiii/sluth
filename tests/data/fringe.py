raise NotImplementedError

async def afoo():
    return "afoo"


class Bar:
    [a, b] = (1,
               2)


a.x: int = 1

import steel
import steel as gold
from steel import copper as tin
from steel import bronze

for i in range(10):
    print(i)

for i0, i1 in range(10):
    print(i)

async for ai in range(10):
    print(i)

async for ai0, ai1 in range(10):
    g = 10
    print(i)

for a[i] in range(10):
    print(i)

with open("file.txt") as my_file:
    t = my_file.read()

async with open("file.txt") as my_afile:
    pass

with open("file.txt") as my_file1, open("file2.txt") as my_file2:
    pass

with open("file.txt"):
    pass

async with open("file.txt"):
    pass

with open("file.txt") as [my_filep0, my_filep1]:
    pass

async with open("file.txt") as [my_afilep0, my_afilep1], conn():
    pass

async for a[i] in range(10):
    print(i)

from gold import *