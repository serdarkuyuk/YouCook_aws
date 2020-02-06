#from youtube_transcript_api import YouTubeTranscriptApi
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import ne_chunk, pos_tag
import re



def hsk(descri):
	
	#nltk.download('words')
	#nltk.download('punkt')
	#nltk.download('maxent_ne_chunker')
	descri = re.sub(r'^https?:\/\/.*[\r\n]*', '', descri, flags=re.MULTILINE)
	descri = re.sub(r'http\S+', '', descri)
	descri = re.sub(r'www\S+', '', descri)
	descri = re.sub("((\S+)?(http(s)?)(\S+))|((\S+)?(www)(\S+))|((\S+)?(\@)(\S+)?)", '', descri)
	#descri = re.sub("[^a-zA-Z0-9]", '', descri)
	#descri = re.sub("((\S+)?(http(s)?)(\S+))|((\S+)?(www)(\S+))|((\S+)?(\@)(\S+)?)", '', descri)
	#descri = re.sub("[^a-zA-Z ]", '', descri)
	descri = descri.lower() # lower case the text
	descri = re.sub(r'^\W', '', descri)
	
	#sents = sent_tokenize(descri)
	words = word_tokenize(descri)
#print(sents)
#print(pos_tag(words))


	

	#print(tag(s))


	def pos(text):
		return pos_tag(word_tokenize(text))

	def entities(text):
		return ne_chunk(pos_tag(word_tokenize(text)))



#ent=pos(texts)
#print(ent)

	grammar = r"""
	  NP: {<CD>?<JJ>+<NN.*>+<VB.*>}
	  	  {<CD>+<JJ>+<NN>+<VB.*>}
	  	  {<CD>+<NN>+<JJ>+<NN>+<VBD>}
	  	  {<NN.*>+<NN.*>+<TO>+<VB.*>}
	  	  {<NN.*>+<POS>+<JJ>+<NN.*>+<TO>+<VB.*>}
	"""
	cp = nltk.RegexpParser(grammar)
	listler=[]



#grammar = "NP: {<DT>?<JJ.*>*<NN.*>+}" 
#grammar = "NP: {<DT>?<JJ>*<NN>}" 
	for s in descri.splitlines():
		if s != '\n':
			'''
			s2 = entities(s) 
			#print(s2.leaves())
			for k in s2:
				if type(k) is not nltk.Tree:
					#t = ' '.join(c[0] for c in k.leaves())
					#print(k.label(), t)
			'''
			#print(s)
			#cp = nltk.RegexpParser(grammar) 


			thing = 0

			tes = pos(s)

			sentt = nltk.ne_chunk(tes, binary = False)
			for subtree in sentt.subtrees():
				if subtree.label() == 'PERSON' or subtree.label() == 'ORGANIZATION' or subtree.label() == 'LOCATION' or subtree.label() == 'DATE' or subtree.label() ==  'TIME' or subtree.label() == 'MONEY' or subtree.label() == 'GPE':
					thing = 1

			if thing != 1 :
				result = cp.parse(tes)
				length_leaf = len(result.leaves())
				#print(rakam)
				if length_leaf < 70 and result.leaves():
					liss = result.leaves()
					listler.append(' '.join([i for i, k in liss])) #+'<br>'
	return listler
	#print('@@@@@@@@@@@@@@@@') 
	#ent.pprint()

'''
def main():
	listss = hsk(descri)
	#return listss
	print(listss)

if __name__ == '__main__':
	main()


youtube-dl --get-description  --skip-download https://www.youtube.com/watch?v=mFXV6cLICqM
youtube-dl --list-subs  --skip-download https://www.youtube.com/watch?v=mFXV6cLICqM
youtube-dl --write-auto-sub --skip-download https://www.youtube.com/watch?v=mFXV6cLICqM
'''
