import sys;args = sys.argv[1:]
from PIL import Image ; img = Image.open(args[0])
import random, math
# Tianhao Chen, pd.4
#img = img.resize((640, 446))
pix = img.load()
size = img.size
def output(size):
    print(f'Size: {size[0]} x {size[1]}')
    print(f'Pixels: {size[0] *size[1]}')
    pixlist = {}
    for i in range(size[0]):
        for j in range(size[1]):
            val = pix[i,j]
            if val not in pixlist:pixlist[val] = 1
            else: pixlist[val] = pixlist[val] +1
    print(f'Distinct pixel count: {len(pixlist)}')
    m = 0
    key = ()
    for i in pixlist:
        if pixlist[i] > m:
            m = pixlist[i]
            key = i
    print(f'Most common pixel: {key} => {pixlist[key]}')
def calcmin(value, means):
    m = ''
    closest = 0
    #index = 0
    for i in means:
        dis = math.dist(value, i)
        if m == '' or dis < m:
            m = dis
            closest = i
            #index +=1
    return closest#, index
def calcmean(means):
    output = []
    for i in means:
        x,y,z = 0, 0, 0
        for j in means[i]:
            x += pix[j[0],j[1]][0]
            y += pix[j[0],j[1]][1]
            z += pix[j[0],j[1]][2]
        output.append((x/len(means[i]), y/len(means[i]),  z/len(means[i])))
    return output
def kmeans(k):
    means = {}
    #meanvals = []
    while len(means) < k:
        x, y = random.randint(0,size[0]-1), random.randint(0,size[1]-1)
        if pix[x,y] not in means: means[pix[x,y]] = [[x,y]]
        #meanvals.append(pix[x,y])
    for i in range(size[0]):
        for j in range(size[1]):
            val = pix[i,j]
            minval = calcmin(val, means)
            means[minval].append([i,j])
    #print(means)
    swap = True
    while swap: #compare old means to new means
        mean = calcmean(means)
        #newmeans = {tuple(i):[] for i in mean}
        newmeans = {}
        swap = False
        for i in means:
            for j in means[i]:
                minval = calcmin(pix[j[0], j[1]], mean)
                if minval not in newmeans: newmeans[minval] = [j]
                else: newmeans[minval].append(j)
                
                if list(newmeans).index(minval) != list(means).index(i):swap = True
                
        means = {i:newmeans[i] for i in newmeans}
    return means
def reproduce(means):
    for i in means:
        for j in means[i]:
            pix[j[0],j[1]] = (int(i[0]), int(i[1]), int(i[2]))
    img.save("new.png")
    #img.save("kmeans/{}.png".format('2023tchen'), "PNG")
def floodfill(start, value):
    global seen
    visited = set()
    parseme = [start]
    while parseme:
        node = parseme.pop(0)
        x, y = node[0], node[1]
        for nbr in ((x+1, y), (x-1, y), (x, y+1), (x, y-1),(x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)):
            if nbr[0] >= 0 and nbr[1] >=0 and nbr[0]< int(size[0]) and nbr[1] < int(size[1]) and nbr not in visited and pix[nbr[0],nbr[1]] == value:
                parseme.append(nbr)
                seen.add(nbr)
            visited.add(nbr)
    return
seen = set()
output(size)
means = kmeans(int(args[1]))
index = 1
print("Final Means: ")
for i in means:
    #print(i, index)
    print(f'{index}: {i} => {len(means[i])-1}')
    index+=1

reproduce(means)
regions = {(int(i[0]), int(i[1]), int(i[2])):0 for i in means}
for i in range(size[0]):
    for j in range(size[1]):
        if (i,j) not in seen:
            #print([i,j], pix[i,j])
            floodfill([i,j], pix[i,j])
            regions[pix[i,j]] +=1
x = ''
for i in [*regions.values()]:
    x += str(i) +', '
print(f'Region counts: {x[0:-2]}')
#print(len(seen) == size[0]*size[1])
#print(means)
#print(img)
#print(pix[0,0])
#img.save(args[0])
# Tianhao Chen, pd. 4, 2023