import sys; args = sys.argv[1:]
import string, re
import nltk
x = open(args[0],"r").read().split()
punctuations = '!"#$%&()*+,./:;<=>?@[\]^_`{|}~'
words = set()
for i in range(len(x)):
    temp = x[i].translate(str.maketrans('','',punctuations))
    if '--' in temp:
        start = temp.index('-')
        if '-' in temp[start+1:] and temp[start+1] != '-' :start = temp[start+1:].index('-') +start+1
        word1 = temp[0:start]
        word2 = temp[start+2:]
        if word1: words.add(word1)
        if word2: words.add(word2)
    else: words.add(temp) #issues though, for example, "alleviationbut", should be two words
notChars = []
for i in words:
    for char in i:
        if char in string.punctuation:
            notChars.append(i)
            break

wordDis = [0 for i in range(19)] #for the number of unique words in the novel
for i in words: wordDis[len(i)-1] +=1
print(f'Distribution list of unique words (case sensitive, index number +1 is the length of the words): {wordDis}')

# sentences = nltk.sent_tokenize(lines) #tokenize sentences
nouns = [] #list to hold all nouns
verbs = []
gerundverb = []
adverbs = []
adjectives = []
pronouns = []
rp = []
names = []
for word in words:
    #print(word)
    tag = nltk.pos_tag(nltk.word_tokenize(str(word)))
    #print(tag)
    if tag[0][1] == 'NNP': names.append(tag[0][0])
    if tag[0][1] == 'NN' or tag[0][1] == 'NNP' or  tag[0][1] == 'NNS' or tag[0][1] == 'NNPS':nouns.append(tag[0][0])
    if tag[0][1] == 'VB' or tag[0][1] == 'VBD' or tag[0][1] == 'VBN' or tag[0][1] == 'VBP' or tag[0][1] == 'VBZ' or tag[0][1] == 'VBG':verbs.append(tag[0][0])
    if tag[0][1] == 'RB' or tag[0][1] == 'RBR' or  tag[0][1] == 'RBS' or tag[0][1] == 'WRB' :adverbs.append(tag[0][0])
    if tag[0][1] == 'JJ' or tag[0][1] == 'JJR' or  tag[0][1] == 'JJS' :adjectives.append(tag[0][0])
    if tag[0][1] == 'PRP' or tag[0][1] == 'PRP$' :pronouns.append(tag[0][0])
    if tag[0][1] == 'VBG' : gerundverb.append(tag[0][0])
    if tag[0][1] == 'WDT' or tag[0][1] == 'WP' : rp.append(tag[0][0])
#verbs, nouns, adjectives, adverbs, pronouns, relative pronouns, gerunds
print(f'Number of unique nouns:{len(nouns)}')
print(f'Number of unique verbs:{len(verbs)}')
print(f'Number of unique adverbs:{len(adverbs)}')
print(f'Number of unique adjectives:{len(adjectives)}')
print(f'Number of unique pronouns:{len(pronouns)}') #might need to split up some of them
print(f'Number of unique gerunds:{len(gerundverb)}')
print(f'Number of unique relative pronouns:{len(rp)}')
y = nltk.word_tokenize(open(args[0],"r").read())
capital = 'QWERTYUIOPASDFGHJKLZXCVBNM'
spoken = []

sentence = ''
speakers = []
whospeaks = ''
for i, elm in enumerate(y):
    #tag = nltk.pos_tag(nltk.word_tokenize(str(elm)))
    if elm == "''":
        if sentence and sentence[-1] in string.punctuation:
            sentence += elm
            if sentence[2] in capital or sentence[-3] != ',':
            #print(sentence[-1])
                if whospeaks : whospeaks +=sentence
                spoken.append(sentence)
                if whospeaks: 
                    speakers.append(whospeaks)
                whospeaks = ''
            sentence = ''
    elif elm == '``' or sentence:
        sentence += elm

        if elm == '``' and not whospeaks:
            pair = ''
            for k in range(i-1,i-4, -1):
                tag =  nltk.pos_tag(nltk.word_tokenize(str(y[k])))
                if tag[0][1] == 'NNP' and 'N' not in pair: pair += 'N'
                if "V" not in pair and(tag[0][1] == 'VB' or tag[0][1] == 'VBD' or tag[0][1] == 'VBN' or tag[0][1] == 'VBP' or tag[0][1] == 'VBZ' or tag[0][1] == 'VBG'): pair +='V'
                if len(pair) == 2:
                    whospeaks += y[k]
                    break
            if not whospeaks:
                tag =  nltk.pos_tag(nltk.word_tokenize(str(y[k])))
                if tag[0][1] == 'NNP' and 'N' not in pair: pair += 'N'
                if "V" not in pair and(tag[0][1] == 'VB' or tag[0][1] == 'VBD' or tag[0][1] == 'VBN' or tag[0][1] == 'VBP' or tag[0][1] == 'VBZ' or tag[0][1] == 'VBG'): pair +='V'
                if len(pair) == 2:
                        if sentence: whospeaks += sentence
                        whospeaks += y[k]
                        break



print(len(spoken))
# print(speakers)
#for i in spoken: print(i)
#print(y)
#note, sent tokenize does not handle dialogue very well. It separates based on '.', and may cut off mid dialogue