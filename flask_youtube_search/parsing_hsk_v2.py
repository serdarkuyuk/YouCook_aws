#from youtube_transcript_api import YouTubeTranscriptApi
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import ne_chunk, pos_tag
import re
import spacy
from spacy.matcher import Matcher

descri='''
#alootamatarkisabzi #indianpotatoandtomatocurry #alooforpoori 

Ingredients:
5 boiled potatoes
4 medium size sliced tomatoes
1 large onion, chopped
1 tbs of ginger and garlic paste
4 tbs of mustard oil
2 bay leaves
1 tsp of cumin seeds
1 black cardamom
3 green cardamom
1 inch cinamon stick
1 mace / javitri
3 green chillies, chopped
3/4 tsp of turmeric powder
1 tsp of coriander powder
1/2 tsp of cumin powder
1 tsp of kashmiri chilli powder
1/3 tsp of garam masala
1 tbs of kasuri methi /dry fenugreek leaves
salt to taste
2 serving spoons of chopped coriander leaves

Join me on facebook: https://www.facebook.com/bluebellrecipes 
Pinterest : https://in.pinterest.com/BlueBellReci...
Youtube: https://www.youtube.com/c/BluebellRec...

 Music by Scott Holmes
 Happy Whistle
 Source - -http://freemusicarchive.org/curator/v...
 Licenced under Creative Commons Attribution 4.0 International License. https://creativecommons.org/licenses/...
'''


def hsk(descri):


	descri = re.sub(r'^https?:\/\/.*[\r\n]*', '', descri, flags=re.MULTILINE)
	descri = re.sub(r'http\S+', '', descri)

	#sents = sent_tokenize(descri)
	#words = word_tokenize(descri)
#print(sents)
#print(pos_tag(words))


	print(descri)

	#print(tag(s))


	def pos(text):
		return pos_tag(word_tokenize(text))

	def entities(text):
		return ne_chunk(pos_tag(word_tokenize(text)))



'''
	nlp = spacy.load('en_core_web_sm')
	matcher = Matcher(nlp.vocab)




	pattern1 = [{'POS': 'NUM'},{'POS': 'VERB'},{'POS': 'NOUN'}]
	pattern2 = [{'POS': 'NUM'},{'POS': 'NOUN'},{'POS': 'NOUN'},{'POS': 'VERB'}]
	pattern3 = [{'POS': 'NUM'},{'POS': 'NOUN'},{'POS': 'NOUN'},{'POS': 'VERB'},{'POS': 'NOUN'}]
	pattern4 = [{'POS': 'NUM'},{'POS': 'NOUN'},{'POS': 'ADP'},{'POS': 'ADJ'},{'POS': 'NOUN'}]
	pattern5 = [{'POS': 'NUM'},{'POS': 'ADV'},{'POS': 'PUNC'},{'POS': 'VERB'},{'POS': 'NOUN'},{'POS': 'VERB'}]


	matcher.add("pattern1", None, pattern1)
	matcher.add("pattern2", None, pattern2)
	matcher.add("pattern3", None, pattern3)
	matcher.add("pattern4", None, pattern4)
	matcher.add("pattern5", None, pattern5)



	doc = nlp(descri)
	listl = matcher(doc)
	take_list=[]
	for i in listl:
		take_list.append(doc[i[1]:i[2]])
	print(take_list)
#ent=pos(texts)
#print(ent)
'''
	grammar = r"""
	  NP: {<CD>?<JJ>+<NN.*>+<VB.*>}
	  	  {<CD>+<JJ>+<NN>+<VB.*>}
	  	  {<CD>+<NN>+<JJ>+<NN>+<VBD>}
	  	  {<NN.*>+<NN.*>+<TO>+<VB.*>}
	  	  {<NN.*>+<POS>+<JJ>+<NN.*>+<TO>+<VB.*>}
	"""

	cp = nltk.RegexpParser(grammar)
	#listler=[]

#grammar = "NP: {<DT>?<JJ.*>*<NN.*>+}" 
#grammar = "NP: {<DT>?<JJ>*<NN>}" 

	#print(doc)

	#for sen in doc.sents:
			#print(type(sen))

			#print(sen.as_doc().pos_)
			#if nlp(sen).is_sentenced == True:
			#print(str(sen).strip())
			#print(len(sen))
			#print(sen.as_doc().text.strip())
			#print('#')
			#res_pos = pos(sen.as_doc().text.strip())
			#parsed_sent = cp.parse(res_pos)
			#print(parsed_sent)


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


def main():
	listss = hsk(descri)
	print(listss)


if __name__ == '__main__':
	main()



'''
youtube-dl --get-description  --skip-download https://www.youtube.com/watch?v=mFXV6cLICqM
youtube-dl --list-subs  --skip-download https://www.youtube.com/watch?v=mFXV6cLICqM
youtube-dl --write-auto-sub --skip-download https://www.youtube.com/watch?v=mFXV6cLICqM
'''