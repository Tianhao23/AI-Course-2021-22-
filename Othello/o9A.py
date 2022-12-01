import sys; args = sys.argv[1:]
import math
brd = args[0]
if len(args) > 1: 
    width = int(args[1])
    height = len(brd) // width
    length = len(brd)

else:
    length = len(brd)
    for lgth in range(1, math.floor(math.sqrt(length))+1): #creating the dimensions to make the puzzle as square as possible
        if length % lgth ==0:
            height = lgth
            width = length//lgth
#     width = max(x for x in range(1,len(brd))if len(brd)%x == 0 and x >= len(brd)/x)
# height = len(brd)//width
# length = len(brd)
#print(width)
#print(height)
#print(length)

#[{xb+xa*s for xa in range(s)} for xb in range(s)]
columns = [[x*width + y for x in range(height)]for y in range(width)]
#print(columns)
rows = [[x+width*y for x in range(width)] for y in range(height)]
#print(rows)

def rotate(brd):
    global columns, rows, height, width
    temp = ""
    for column in columns:
        for idx in column[::-1]:
            temp += brd[idx]
    tem = width
    width = height
    height = tem
    columns = [[x*width + y for x in range(height)]for y in range(width)]
    rows = [[x+width*y for x in range(width)] for y in range(height)]
    return temp

def grid(b):
    r = ""
    for idx, x in enumerate(b):
        r += x
        if idx % height == height-1: r += "\n"
    return r

def flip(brd):
    global width, height, rows, columns
    temp = ""
    #print(rows)
    for row in rows[::-1]:
        for idx in row:
            temp += brd[idx]
    #print(temp)
    columns = [[x*width + y for x in range(height)]for y in range(width)]
    rows = [[x+width*y for x in range(width)] for y in range(height)]    
    return temp
s = set()
#same place
for r in range(4):
    brd = rotate(brd)
    s.add(brd)
    #print(grid(brd))
    #print()

brd = flip(brd)
s.add(brd)

#print(grid(brd))
for r in range(4):
    brd = rotate(brd)
    s.add(brd)
    #print(grid(brd))
    #print()
for i in s:print(i)
#Jason Chen and Tianhao Chen, pd 4, 2023