import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import ne_chunk, pos_tag

qry = "who is Mahatma Gandhi"
tokens = nltk.tokenize.word_tokenize(qry)
pos = nltk.pos_tag(tokens)
sentt = nltk.ne_chunk(pos, binary = False)
print(sentt.subtrees())
person = []
for subtree in sentt.subtrees():
	if subtree.label() == 'PERSON':
		print("something")
	for leave in subtree.leaves():
		person.append(leave)
print("person=", person)