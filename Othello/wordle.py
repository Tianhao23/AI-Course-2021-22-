import sys; args = sys.argv[1:]
myWords = open(args[0],"r").read().splitlines()
import time
a = time.process_time()
legalCount = 0
cCount = 0
dCount = 0
duplicate = []
legal5words = []
for word in myWords:
    x = set(word) - set('abcdefghijklmnopqrstuvwxyz')
    if len(x) == 0: 
        legalCount +=1
        if len(word) == 5: 
            legal5words.append(word)
            cCount +=1
            for i, char in enumerate(word):
                if i == 4:
                    if char in word[:i]:
                        duplicate.append(word)
                        dCount +=1
                        break
                else:
                    if char in word[:i] +word[i+1:]:
                        duplicate.append(word)
                        dCount +=1
                        break
elist = [item for item in duplicate]
for word in duplicate:
    letters = set(word)
    for x in legal5words:
        if x != word:
            match = True
            for i in letters:
                if i not in x:
                    match = False
            if match == True:
                elist.remove(word)
                break
            
print(f'A: {len(myWords)}') 
print(f'B: {legalCount}')
print(f'C: {cCount}')
print(f'D: {dCount}')
print(f'E: {len(elist)}')
b = round(time.process_time()-a,3)
print(f'H: {b}s') 
# A) number of entries in the dictionary
# B) # of [a-z] words
# C) # of 5 letter [a-z] words
# D) # of where not all 5 letters are distince
# E) The length of the list of those words that have exactly 5 letters with at least one letter a 
# duplicate no other 5 letter word in the dictionary contains all the letters of any word in the list
# F) Show the list in sorted order
# G) How many words from F do not two duplicate letters next to each other
# H) Total runtime of your script in seconds (don't forget the s)