from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
#import wordlists

#LEMMATIZER = WordNetLemmatizer()


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

'''    
ingredient_list=["blackberries milk", "chopped potatos"]
filtered_list = []
add_list = 0
for items in ingredient_list:
    print(items)
    for i in word_tokenize(items):
        ingr_bool = is_it_ingredient(i)
        print(i, ingr_bool) 
        if ingr_bool == True:
            add_list = 1
        else:
            add_list = 0
    if add_list == 1 :
        filtered_list.append(items)
        add_list = 0
          


print(is_it_ingredient('blackberries'))
'''
#filtered_ingred = []
#for i in extracted_ingred:
#    if is_it_ingredient(i) == True:
#        filtered_ingred.append(i)