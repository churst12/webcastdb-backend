import nltk
import random
nltk.download('punkt')
nltk.download('stopwords')

file1 = open("./lecture2/01.txt","r")
text = file1.read()

textpunctuated = text
counter = 0
while counter < len(text):
	rand = random.randint(20,90)
	textpunctuated += text[counter:(counter+rand)] + "."
	counter += rand
#print (textpunctuated)

sentence_list = nltk.sent_tokenize(textpunctuated)  



stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}  
for word in nltk.word_tokenize(text):  
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

maximum_frequncy = max(word_frequencies.values())

for word in word_frequencies.keys():  
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)


sentence_scores = {}  
for sent in sentence_list:  
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 100:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

import heapq  
summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)  
print(summary)  

