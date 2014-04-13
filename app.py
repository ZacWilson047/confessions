from flask import Flask, render_template, request, redirect, url_for
import random
import time
import yaml
import sys

reload(sys)
sys.setdefaultencoding('UTF8')

app = Flask(__name__)

#FIRSTNAMES = yaml.load(file('firstnames.yaml', 'r'))
#LASTNAMES = yaml.load(file('lastnames.yaml', 'r'))
NAMES = yaml.load(file('names.yaml','r'))

textFile = open('toUse.txt', 'r')
sentenceList = []
for line in textFile:
    sentences = line.replace('\n', '').replace(':', '').replace('\\x','').replace('\x97', '').lstrip('"message": "').replace('"', '').replace('\\', '').split('.')
    for sentence in sentences:
        if sentence:
            sentenceList.append(sentence)

##### FIRST ORDER
            
probFirst1 = []
probDict1 = {}

for sentence in sentenceList:
    sentence = sentence.split(' ')
    #while '' in sentence:
    #    sentence.remove('')
    if len(sentence) > 0:
        probFirst1.append(sentence[0])
    else:
        probFirst1.append('.')
    pos = 0
    
    if len(sentence) > 1:
        while pos < len(sentence) - 2:    # add a word to the word-key's list if it immediately follows that word
            if probDict1.has_key(sentence[pos]):
                probDict1[sentence[pos]].append(sentence[pos+1])
            else :
                probDict1[sentence[pos]] = []
                probDict1[sentence[pos]].append(sentence[pos+1])
            pos += 1
        if probDict1.has_key(sentence[pos]):
            probDict1[sentence[pos]].append('.')
        else : 
            probDict1[sentence[pos]] = []
            probDict1[sentence[pos]].append('.')

##### SECOND ORDER
            
probFirst2 = []
probDict2 = {}

for sentence in sentenceList:
    sentence = sentence.split(' ')
    #while '' in sentence:
    #    sentence.remove('')
    if len(sentence) > 1:
        probFirst2.append((sentence[0], sentence[1]))
    else:
        probFirst2.append((sentence[0], '.'))
    pos = 0
    
    if len(sentence) > 2:
        while pos < len(sentence) - 3:    # add a word to the word-key's list if it immediately follows that word
            if probDict2.has_key((sentence[pos], sentence[pos+1])):
                probDict2[(sentence[pos], sentence[pos+1])].append(sentence[pos+2])
            else :
                probDict2[(sentence[pos], sentence[pos+1])] = []
                probDict2[(sentence[pos], sentence[pos+1])].append(sentence[pos+2])
            pos += 1
        if probDict2.has_key((sentence[pos], sentence[pos+1])):
            probDict2[(sentence[pos], sentence[pos+1])].append('.')
        else : 
            probDict2[(sentence[pos], sentence[pos+1])] = []
            probDict2[(sentence[pos], sentence[pos+1])].append('.')

##### THIRD ORDER
          
probFirst = []
probDict = {}

for sentence in sentenceList:
    sentence = sentence.split(' ')
    #while '' in sentence:
    #    sentence.remove('')
    if len(sentence) > 2:
        probFirst.append((sentence[0], sentence[1], sentence[2]))
    elif len(sentence) == 2:
        probFirst.append((sentence[0], sentence[1], '.'))
    elif len(sentence) == 1:
    	probFirst.append((sentence[0], '.'))
    pos = 0
    
    if len(sentence) > 3:
        while pos < len(sentence) - 4:    # add a word to the word-key's list if it immediately follows that word
            if probDict.has_key((sentence[pos], sentence[pos+1], sentence[pos+2])):
                probDict[(sentence[pos], sentence[pos+1], sentence[pos+2])].append(sentence[pos+3])
            else:
                probDict[(sentence[pos], sentence[pos+1], sentence[pos+2])] = []
                probDict[(sentence[pos], sentence[pos+1], sentence[pos+2])].append(sentence[pos+3])
            pos += 1
        if probDict.has_key((sentence[pos], sentence[pos+1], sentence[pos+2])):
            probDict[(sentence[pos], sentence[pos+1], sentence[pos+2])].append('.')
        else: 
            probDict[(sentence[pos], sentence[pos+1], sentence[pos+2])] = []
            probDict[(sentence[pos], sentence[pos+1], sentence[pos+2])].append('.')
textFile.close()

def createConfession(ordr):
	if(ordr==1):
		confession = ''
		first = probFirst1[random.randint(0, len(probFirst1)-1)]
		if first == '.' :
		    return createConfession(ordr)
		else :
		    confession = first
		    prev = first
		    while 'hi':
		        if not (probDict1.has_key(prev)):
		            confession += '.'
		            break
		        toAdd = probDict1[prev][random.randint(0, len(probDict1[prev])-1)]
		        if toAdd == '.':
		            confession += toAdd
		            break
		        confession += ' ' + toAdd
		        prev = toAdd
		    confession = confession.lstrip(',').lstrip(' ').lstrip(')').lstrip('(')
		    if(confession == '.' or len(confession)<2) :
		    	confession = createConfession(ordr)
		    else :
		    	return confession
	elif(ordr==2):
		confession = ''
		first = probFirst2[random.randint(0, len(probFirst2)-1)]
		if first[1] == '.' :
			return createConfession(ordr)
		else :
		    confession = first[0] + ' ' + first[1]
		    prev = first
		    while 'hi':
		        if not (probDict2.has_key(prev)):
		            confession += '.'
		            break
		        toAdd = probDict2[prev][random.randint(0, len(probDict2[prev])-1)]
		        if toAdd == '.':
		            confession += toAdd
		            break
		        confession += ' ' + toAdd
		        prev = (prev[1], toAdd)
		    confession = confession.lstrip(',').lstrip(' ').lstrip(')').lstrip('(')
		    return confession
	elif(ordr==3):
		confession = ''
		first = probFirst[random.randint(0, len(probFirst)-1)]
		if first[1] == '.':
		    return createConfession(ordr)
		elif first[2] == '.':
			return first[0] + ' ' + first[1] + ' ' + first[2]
		else:
		    confession = first[0] + ' ' + first[1] + ' ' + first[2]
		    prev = first
		    while 'hi':
		        if not (probDict.has_key(prev)):
		            confession += '.'
		            break
		        toAdd = probDict[prev][random.randint(0, len(probDict[prev])-1)]
		        if toAdd == '.':
		            confession += toAdd
		            break
		        confession += ' ' + toAdd
		        prev = (prev[1], prev[2], toAdd)
		    confession = confession.lstrip(',').lstrip(' ').lstrip(')').lstrip('(')
		    if(confession == '.' or len(confession)<2) :
		    	confession = createConfession(ordr)
		    else :
		    	return confession	
    
@app.route('/')
def index():
	myorder = int(request.args.get('o', 2))

	status = createConfession(myorder)
	#status = status.lstrip(')').lstrip('(').lstrip(' ').lstrip(',')
	pictures = ["http://reidbm.com/img/pic1.jpg",
				"http://reidbm.com/img/pic2.jpg",
				"http://reidbm.com/img/pic3.jpg",
				"http://reidbm.com/img/pic4.jpg",
				"http://reidbm.com/img/pic5.jpg",
				"http://reidbm.com/img/pic6.jpg",
				"http://reidbm.com/img/pic7.jpg",
				"http://reidbm.com/img/pic8.jpg",
				"http://reidbm.com/img/pic9.jpg",
				"http://reidbm.com/img/pic10.jpg"]

	comment_count = random.randint(1,7)
	like_count = random.randint(1,1000)

	selected_comments = []
	selected_names = []
	full_comments = {}

	for i in range(0, comment_count):
		randname = random.choice(NAMES.keys())+" "+random.choice(NAMES.values())
		selected_names.append({"reid":"mitchell"})
		randpic = pictures[random.randint(0,len(pictures)-1)]
		randcomment = createConfession(myorder)
		#randcomment = randcomment.lstrip(')').lstrip('(').lstrip(' ').lstrip(',')
		full_comments[(randname, randpic)] = randcomment

	#get today's date (and pass it to page)
	date = time.strftime("%B %d")

	return render_template('index.html', order=myorder, status=status, date=date, likes=like_count, comments=full_comments, names=NAMES)

if __name__ == '__main__':
	app.run(debug=True)