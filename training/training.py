import nltk
import spacy
import random
import time
import numpy as np
from spacy.util import minibatch, compounding
from os import path, mkdir
import xml.etree.ElementTree as ET
import random
import time
from nltk.corpus import wordnet



def make_folder():
	'''
	Makes 2 directory where NER model will be in models
	and data (.xml) will be in data folder
	'''
	if not path.isdir("data/"):
	    mkdir("data/")
	if not path.isdir("models/"):
	    mkdir("models/")


def get_file_path(file_name):
	'''
	gets file name
	'''
	file_path = path.abspath(path.join('data', file_name))
	#print(full_file)
	return file_path


def parsing_data(file_path):
	'''
	returns document object that holds directions and annotation of data
	'''

	documen = ET.parse(file_path)
	documents = documen.findall('document')

	return documents


def formating_data(documents):
	'''
	Reads foodbank data (xml format) and make it readable to spaCy model
	'''

	annotation = "INGREDIENT"
	ALL_DATA = []
	for k in range(len(documents)):

		document = documents[k]

		description = document.findall('infon')
		location = document.findall('annotation/location')
		ingredient = document.findall('annotation/text')
		sentence = description[1].text.strip()
		entities=[]
		parsed_sentence = nlp(description[1].text.strip())
		for i in range(len(location)):

			offset = int(location[i].get('offset'))			#shows the position of word token
			loc_of_begin = int(parsed_sentence[offset-1].idx) #show where this token starts
			length_of_word = int(location[i].get('length')) #shows lenght of the token(aka ingredient)
			loc_of_end = loc_of_begin + length_of_word
			entities.append((loc_of_begin, loc_of_end, annotation))
			#print(i)
		ALL_DATA.append([sentence, {'entities' : entities}])
		print(k)
	return ALL_DATA



def split_train_test(ALL_DATA, train_percent=70):
	'''
	Pandas function train_test_split can not be used in here. NLP text structure is 
	not similar with data frame
	There are 1000 paragraph in database and 70% is used for training.
	'''

	tr_numbers= random.sample(range(0, 1000), train_percent*10)
	all_numbers = set(range(1000))
	ts_numbers = list(all_numbers - set(tr_numbers))
	TRAIN_DATA = list(map(ALL_DATA.__getitem__, tr_numbers))
	TEST_DATA = list(map(ALL_DATA.__getitem__, ts_numbers))
	print(len(TRAIN_DATA),len(TEST_DATA))

	return TRAIN_DATA, TEST_DATA

def calc_precision(pred, true):
	'''
	Calculates the precision over pred and ture. list
	'''        
    precision = len([x for x in set(pred) if x in set(true)]) / (len(set(pred)) + 1e-20) # true positives / total pred
    return precision

def calc_recall(pred, true):
	'''
	Calculates the recall over pred and ture. list
	'''  
    recall = len([x for x in set(true) if x in set(pred)]) / (len(set(true)) + 1e-20)    # true positives / total test
    return recall

def calc_f1(precision, recall):
	'''
	Calculates the F1 score over pred and ture. list
	'''  
    f1 = 2 * ((precision * recall) / (precision + recall + 1e-20))
    return f1


def test_score(ner, TEST_DATA):
    # run the predictions on each sentence in the test dataset, and return the spacy object
    preds = [ner(x[0]) for x in TEST_DATA]

    precisions, recalls, f1s = [], [], [] 

    # iterate over predictions and test data and calculate precision, recall, and F1-score
    for pred, true in zip(preds, TEST_DATA): 
        
        pred = [i.text for i in pred.ents] 
        list_entity = []
        for i in range(len(true[1]['entities'])):
            list_entity.append(true[0][true[1]['entities'][i][0]:true[1]['entities'][i][1]])
        true = list_entity   
        precision = calc_precision(true, pred)
        
        precisions.append(precision)
        recall = calc_recall(true, pred)
        recalls.append(recall)
        f1s.append(calc_f1(precision, recall))
    
    performance = [np.around(np.mean(precisions), 3), np.around(np.mean(recalls), 3), np.around(np.mean(f1s), 3)]
    return performance

# A simple decorator to log function processing time
def timer(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print("Completed in {} seconds".format(int(te - ts)))
        return result
    return timed

# Data must be of the form (sentence, {entities: [start, end, label]})
@timer
def train_spacy(train_data, test_data, labels, iterations, dropout = 0.4, display_freq = 1):
    ''' Train a spacy NER model, which can be queried against with test data
    
    train_data : training data in the format of (sentence, {entities: [(start, end, label)]})
    labels : a list of unique annotations
    iterations : number of training iterations
    dropout : dropout proportion for training
    display_freq : number of epochs between logging losses to console
    '''
    #nlp = spacy.blank('en')
    nlp = spacy.load('en_core_web_md') 
    nlp.remove_pipe("ner")

    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner)
    
    # Add entity labels to the NER pipeline
    for i in labels:
        ner.add_label(i)

    # Disable other pipelines in SpaCy to only train NER
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):
        nlp.vocab.vectors.name = 'spacy_model' # without this, spaCy throws an "unnamed" error
        optimizer = nlp.begin_training()
        loss_perf_list = []
        train_perf_list = []
        test_perf_list = []
        for itr in range(iterations):
            random.shuffle(train_data) # shuffle the training data before each iteration
            losses = {}
            batches = minibatch(train_data, size = compounding(4., 32., 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(           
                    texts,
                    annotations, 
                    drop = dropout,   
                    sgd = optimizer,
                    losses = losses)
            if itr % display_freq == 0:
                loss_perf_ = [itr+1, losses]
                loss_perf_list.append(loss_perf_)
                #print(loss_perf_)
                print("Iteration {} Loss: {}".format(itr + 1, losses))
            train_perf_=test_score(nlp, train_data)
            train_perf_list.append(train_perf_)
            test_perf_=test_score(nlp, test_data)
            test_perf_list.append(test_perf_)
    return nlp, train_perf_list, test_perf_list, loss_perf_list

def plot_score_vs_iter(train_perf_list, test_perf_list, loss_perf_list):
	'''
	plots the precistion, recall, f1 score and losses vs iteration

	'''
	iteration = range(len(train_perf_list))
	tr_precision = [i[0] for i in train_perf_list]
	tr_recall = [i[1] for i in train_perf_list]
	tr_f1 = [i[2] for i in train_perf_list]
	ts_precision = [i[0] for i in test_perf_list]
	ts_recall = [i[1] for i in test_perf_list]
	ts_f1 = [i[2] for i in test_perf_list]
	lossess = [float(i[1]['ner']) for i in loss_perf_list]

	font = {'family': 'serif',
	        'color':  'black',
	        'weight': 'normal',
	        'size': 16,
	        }
	miny = 0.75
	maxy = 0.90
	plt.scatter(iteration, tr_precision, label="Training")
	plt.scatter(iteration, ts_precision, c='red', label="Testing")
	plt.xlabel("Iteration", fontdict=font)
	plt.ylabel("Precision", fontdict=font)
	plt.legend(loc='upper left')

	plt.ylim((miny, maxy))
	plt.title('Perfornmance', fontdict=font)
	plt.tight_layout()
	plt.show()
	plt.scatter(iteration, tr_recall)
	plt.scatter(iteration, ts_recall, c='red')
	plt.xlabel("Iteration",fontdict=font)
	plt.ylabel("Recall", fontdict=font)
	plt.legend(loc='upper left')
	plt.ylim((miny, maxy))
	plt.title('Perfornmance')
	plt.tight_layout()
	plt.show()
	plt.scatter(iteration, tr_f1)
	plt.scatter(iteration, ts_f1, c='red')
	plt.xlabel("Iteration", fontdict=font)
	plt.ylabel("F1-Score", fontdict=font)
	plt.legend(loc='upper left')
	plt.ylim((miny, maxy))
	plt.title('Perfornmance')
	plt.tight_layout()
	plt.show()

	plt.scatter(iteration, lossess)
	plt.xlabel("Iteration", fontdict=font)
	plt.ylabel("Loss", fontdict=font)
	plt.legend(loc='upper left')
	plt.title('Perfornmance')
	plt.tight_layout()
	plt.show()


def is_it_ingredient(word):
    """
    Return True if the word is an ingredient, False otherwise.
    >>> is_ingredient('milk')
    True
    >>> is_ingredient('blackberries')
    True
    >>> is_ingredient('Canada')
    False
    >>> is_ingredient('breakfast')
    False
    >>> is_ingredient('dish')
    False
    """
    reject_synsets = ['meal.n.01', 'meal.n.02', 'dish.n.02', 'vitamin.n.01']
    reject_synsets = set(wordnet.synset(w) for w in reject_synsets)
    accept_synsets = ['food.n.01', 'food.n.02']
    accept_synsets = set(wordnet.synset(w) for w in accept_synsets)
    for word_synset in wordnet.synsets(word, wordnet.NOUN):
        all_synsets = set(word_synset.closure(lambda s: s.hypernyms()))
        all_synsets.add(word_synset)
        for synset in reject_synsets:
            if synset in all_synsets:
                return False
        for synset in accept_synsets:
            if synset in all_synsets:
                return True
    #return word #in wordlists.ingredients

def main():

	nlp = spacy.load('en')#en_core_web_md

	make_folder():

	file_name = "FoodBase_curated.xml"
	file_path = get_file_path(file_name):
	documents = parsing_data(file_path)
	ALL_DATA = formating_data(documents)
	
	TRAIN_DATA, TEST_DATA = split_train_test(ALL_DATA):


 
	LABELS=['','INGREDIENT']
	# Train (and save) the NER model
	ner, train_perf_list, test_perf_list, loss_perf_list = train_spacy(TRAIN_DATA, LABELS, 30)
	ner.to_disk("models/spacy_example")
	#[filtered_ingred.append(i) for i in extracted_ingred if is_it_ingredient(i) == True]
    
        
if __name__ == '__main__':
	main()





'''
'''


