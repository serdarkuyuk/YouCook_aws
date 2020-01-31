#from youtube_transcript_api import YouTubeTranscriptApi
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import ne_chunk, pos_tag
import re



def hsk(descri):


	descri = re.sub(r'^https?:\/\/.*[\r\n]*', '', descri, flags=re.MULTILINE)
	descri = re.sub(r'http\S+', '', descri)

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
		#print(type(s))
		#cp = nltk.RegexpParser(grammar) 
		tes = pos(s)
		result = cp.parse(tes)
		rakam = len(result.leaves())
		#print(rakam)
		if rakam < 7 and result.leaves():
			liss = result.leaves()
			listler.append(' '.join([i for i, k in liss]))
	return listler
	#print('@@@@@@@@@@@@@@@@') 
#ent.pprint()
'''
def main()
	listss = hsk(descri)
	return listss

if __name__ == '__main__':
	main()
'''
'''
youtube-dl --get-description  --skip-download https://www.youtube.com/watch?v=mFXV6cLICqM
youtube-dl --list-subs  --skip-download https://www.youtube.com/watch?v=mFXV6cLICqM
youtube-dl --write-auto-sub --skip-download https://www.youtube.com/watch?v=mFXV6cLICqM
'''