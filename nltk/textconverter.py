# in powershell type in 'pip install unidecode'

from unidecode import unidecode
inFile = open('JekyllandHyde.txt','r',encoding='utf-8').read()
outFile = open('DrJekyllandMrHyde.txt','w').write(unidecode(inFile))

#newStory.txt will be the story without unicode
#unicode will be mapped to the most fitting ascii