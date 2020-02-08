from __future__ import unicode_literals
import spacy
import os 
from youtube_transcript_api import YouTubeTranscriptApi
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet, stopwords


def extract_ingredients(video_id):

    home_dir = os.getcwd()
    model_dir = 'flask_youtube_search/models'
    modal_path = os.path.join(home_dir, model_dir)

    def load_model(model_path):
        """
        Loads a pre-trained model for prediction on new test sentences
        model_path : directory of model (under models folder)
        """
        nlp = spacy.blank('en') 
        if 'ner' not in nlp.pipe_names:
            ner = nlp.create_pipe('ner')
            nlp.add_pipe(ner)
        #load pretrained model from the path
        ner = nlp.from_disk(model_path)
        return ner

    def test_example():
        """
        Test the model (using ner model) if you do not use text from YouTube captions
        """
        example_text = ['''Mark and Jack welcome back to couch on crackerjacks today I'm gonna show you how to make a basic and delicious potato salad some people might call this a country style potato salad some people might refer to it as a deli style of potato salad either way it's got the perfect balance of sweet and tangy from the sugar and the vinegar and pickles and everything else that's in this it's just your basic homemade potato salad you can add any number of things to this to make it your own but I'm just going to show you how I like to make mine so without further ado let's get started so naturally I'm going to start out with my potatoes every potato salad starts with potatoes for this recipe and for my potato salad I prefer using just regular old russet potatoes they're the cheapest they're the best I've tried using Yukon Gold potatoes and red potatoes for this recipe I prefer hands down at the russet potatoes it just it makes the best potato salad for me you can use whatever kind of potatoes you like though and using a potato peeler I'm just going to peel these potatoes a little trick for you that little end on most potato peelers it's kind of rounded use that to dig out the eyes of your potato it's what I've always used it for so it's just the perfect little tool to dig out the eyes of a potato but what you want to do is just go ahead and peel your potatoes and you don't have to peel your potatoes if you don't want to if you like skin on potato salad by all means go ahead and leave the skin on it doesn't make any difference personal preference and as you're peeling your potatoes and you get one done go ahead and put them into a large pot this is going to be the same profit I cut these in that's filled up with water you want to make sure and keep your potatoes covered that will prevent your potatoes from oxidizing and turning that pinky brown color but you just want to go through and peel all of your potatoes and I am using three pounds of potatoes for this recipe now once you get all your potatoes peeled you want to go ahead and cut them up basically you want to cut these into about 3/4 inch square pieces so for these medium potatoes I cut them half I turn them 90 degrees cut them into three pea is if you will that way if it's a larger potato do four and then cut those into chunks basically like I said you want about three quarters of an inch by three quarters of an inch by three quarters of an inch pieces and then again throw your potatoes back into the water that you pulled the potatoes out of that way they do not oxidize on you now when you get all your potatoes cut up your water is going to be cloudy and it's gonna be murky and it's gonna be just full of all the starch coming off of those potatoes what you want to do is rinse your potatoes well you want to make sure that the water coming off of that is completely clear go ahead and rinse these a good three or four times and then drain them completely you want to make sure that all of that starch gets off of those potatoes then you want to go ahead and light your stove and take your pot and you want a large pot for this put it over a medium-high heat time actually even high heat or at this point take your drained potatoes and put those into your pot and you want to add enough cold water to this to come up about one inch over the top of the potatoes starting off with cool water your potatoes cook evenly as the water comes up to temperature your potatoes come up with them to temperature if you start out putting cold potatoes into boiling water the outside of the potato is gonna be mush before the inside is actually cooked and before this gets going too far I'm gonna take two large eggs and I'm gonna put those in the water with the potatoes this recipe uses hard-boiled eggs and since I'm boiling the potatoes anyway I might as well just boil the eggs right along with the potatoes so just go ahead and add two large eggs to the pot and you want to cover your pot and you want to bring this up to a boil now once your water is that a boy I'll go ahead and give your potatoes an egg a gentle stir you want to be careful with this because you don't do not want to break your eggs and you also don't want to break up the potatoes but once this comes up to a boil you want to boil this for exactly ten minutes and how to check to make sure that your potatoes are done you want to take a couple large pieces take them out put them on a spoon and using a fork you want to put the fork into the potato and you want just a little bit of give in your potatoes before they break apart if you can see there it's just the slightest little bit of give before the potato breaks up you don't want to cook these any longer than that because they they will finish cooking when you take them off heat but you want to go ahead and drain these in a colander and once they are drained well go ahead and pour your potatoes and eggs back into the pot that you cooked them in and here you can dig out your eggs and you want to put your eggs in a bowl of cold water you want to stop that cooking process as soon as possible because if you cook your eggs too long you're gonna get that dreaded green ring around the yolk go ahead and put those in a bowl of cold water to stop the cooking process immediately and then you want to keep your potatoes in the pot that you cook them in to cool and you want to cool them completely before you do anything else with them if you add a salad dressing to hot potatoes it's gonna break on you and you don't want that so just go ahead and let your potatoes steam off and cool and I'm gonna let these sit for about a half an hour before I even start making the dressing for my potato salad and while you're waiting for your potatoes to cool off you can go ahead and peel your eggs it helps to wait a little bit for your eggs to cool down before you peel them just go ahead and crack them on a countertop and then start peeling them if you peel them underneath water or running water they peel super easy so as you can see here's I mean it takes nothing to do it under water water gets under there and the shell just slips off I just go ahead and peel your egg eggs and set them off until later I'm gonna need a few vegetables for my dressing I went ahead and already cut up half of a yellow onion here off a video I thought I was recording when I wasn't you don't need to see me chopped onions anyway everybody knows how to do that I've also got two stalks of celery here I'm just going to cut the ends off as well as the tops if you want to save the tops they make a nice garnish you don't have to keep them and I'm not gonna keep them here the celery I'm going to cut these sticks or stalks into orders and then I'm going to chop those up because I don't like really big chunks of celery in my potato salad so I'm just gonna cut these into four slices and then turn them around and cut these into dices if you will and I'm just going to go ahead after I get that died and set those off to the side until I need them later now for our dressing in a large bowl and you want to make sure that you use a plenty large bowl for this because it does make a lot of potato salad I've got one and a half cups of mayonnaise this recipe really does not work with Miracle Whip so since we're gonna be adding sugar to this stick to the plain old mayonnaise I'm gonna throw my eggs in there and using the back of a fork I'm just gonna break up my eggs if you like big chunks of egg in your potato salad don't mash it up as much but I'm gonna mash this up pretty fine and then you want to add in a quarter of a cup of sugar as well as a teaspoon and a half of salt it seems like a lot of salt it really isn't because there are a lot of potatoes here two teaspoons of white vinegar just plain white distilled vinegar then you want to add two tablespoons of sweet pickle relish you could also use dill pickle relish if you wanted to I like sweet in mine and finally I'm gonna add in two teaspoons of prepared yellow mustard if you like a more mustardy potato salad you can add more mustard if you want to this perfectly acceptable and then using a spoon or a fork whatever just go ahead and mix this up well and then you want to add in your onions and celery and go ahead and get that mixed in and you want to make sure to mix all of your ingredients and get your dressing thoroughly mixed before you add the potatoes because you don't want to over mix this once you get your potatoes added so go ahead and take your cooled potatoes again make sure that they are at least room temperature you do not want them warm or hot at all but go ahead and add those into your bowl and then using a spatula I'm going to gently fold the dressing into my potatoes you want your potatoes to remain as in this large of chunks as possible so don't go crazy you know stirring it stirring stirring you want to gently fold this so your potatoes do stay as whole as possible and a little secret for you just to bind up the dressing just a little bit I'm going to add two tablespoons of instant mashed potato flakes into the finished mixture I'm just going to fold this in basically what those do the potato flakes they bind up the dressing and make the dressing firm it also helps it kind of stick to the potatoes a little bit better so you you know the dressing doesn't run off of the potatoes which can be a problem with some recipes so there you go you want to make sure that those potato flakes are evenly distributed in there and everything is well mixed together everything is combined perfectly go ahead and give this a taste make sure that the salt is ok for you if you need a little bit more salt go ahead and add it if you want to if you need more mustard or vinegar or eggs whatever now is the time to do it but you want to go ahead and cover this with a piece of cling wrap saran wrap and refrigerate this for at least four to six hours before you serve this the longer you let this sit the better it gets but there you go there's your basic all-around simple homemade deli style or country style potato salad definitely give this recipe a try if you do let me know how you like it down below in the comment section if you like this video be sure to give it a thumbs up I would greatly appreciate it subscribe for more deliciousness and to keep up to date on all my latest videos thanks so much for watching and we will see you next time''']

        return str(example_text)

    def get_captions(video_id):
        """
        retrieve the available transcripts
        """
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            
            #parse only string and remove the time of captions
            text = []
            for txt in transcript:
               text.append(txt['text'])
            return text
        except:
            text = "No Captions"
            return text


    def is_it_ingredient(word):
        """
        Return True if the word is an ingredient, False otherwise.
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

    def filter_non_ingredient(ingredient_list):
        """
        Filters out the non-ingredient text from ingredient_list
        """
        stop_words = set(stopwords.words('english'))
        
        filtered_list = []
        add_list = 0  #a dummy variable to add a text to filtered list
        for phrases in set(ingredient_list): #run through only one item in set (removes duplicates)

            for word in phrases:
                if word in stop_words:
                    phrases.replace(word,'')

            #if one of the word in a phrase is ingredient, counts in to list
            for word in word_tokenize(phrases):  #phrases can be phrase (run through phrases)
                
                is_ingredient = is_it_ingredient(word) #returns true if a word is ingridient
                
                if is_ingredient == True:
                    add_list = 1
                else:
                    add_list = 0

            ##if one of the word in a phrase is ingredient, counts in to list
            if add_list == 1 :

                filtered_list.append(phrases.capitalize())
                add_list = 0 

        return filtered_list


    # extract the sentences 
    caption_list = get_captions(video_id) 

    #load the ner model
    ner = load_model(modal_path)

    #execute model through caption
    caption_w_model = ner(''.join(caption_list))

    #extracts ingredients using entities
    ingredient_list=[]
    for x in caption_w_model.ents:
        ingredient_list.append(x.text) 

    filtered_list = filter_non_ingredient(ingredient_list)

    return filtered_list







    


