from __future__ import unicode_literals
from spacy import displacy
import spacy
import random
import time
import numpy as np
from spacy.util import minibatch, compounding
import os
#import xml.etree.ElementTree as ET
import random
from youtube_transcript_api import YouTubeTranscriptApi
from flask_youtube_search import parsing_hsk_v3, find_ingre_dict
from nltk.tokenize import word_tokenize







def hsk_result(video_id):

    def load_model(model_path):
        ''' Loads a pre-trained model for prediction on new test sentences
        
        model_path : directory of model saved by spacy.to_disk
        '''
        nlp = spacy.blank('en') 
        if 'ner' not in nlp.pipe_names:
            ner = nlp.create_pipe('ner')
            nlp.add_pipe(ner)
        ner = nlp.from_disk(model_path)
        return ner

    def data():
        You_DATA2 = ["5 red potatoes boiled and chopped",
        "5 hard-boiled eggs chopped",
        "1 cup celery chopped"]
        return str(You_DATA2)

    def get_captions(video_id):
        # retrieve the available transcripts
        #try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = []
        for txt in transcript:
           text.append(txt['text'])
        return text
        #except:
            #text = "Not text"
            #return text

    def get_description():
        #print("Something else went wrong")
        ruledbase_parsed_text = parsing_hsk_v3.hsk(video_data)

        #transcript = data()
        transcript = ruledbase_parsed_text
        transcript =''.join(transcript)
        return transcript


       

    #TEST_DATA, _ = load_data_spacy("data/test.txt")


    #print(video_id)
    test_sentences = get_captions(video_id) # extract the sentences from [sentence, entity]
    #result2 = get_description(video_id) # extract the sentences from [sentence, entity]

    ner = load_model("/home/ubuntu/application/YouCook_aws/flask_youtube_search/models")
    #ner = load_model("/Users/serdarkuyuk/Documents/harvard/serdar/insight/youtube/flaskyoucook/YouCook_aws/flask_youtube_search/models")

    
    #print(''.join(test_sentences))
    
    #for x in test_sentences:
    doc = ner(''.join(test_sentences))
    #    displacy.render(doc, jupyter = True, style = "ent")
    #doc = ner(x)
    ingredient_list=[]
    for x in doc.ents:
        ingredient_list.append(x.text) # +'<br>'

    #ingredient_series = pd.Series(ingredient_list)
    #ingredient_series.drop_duplicates(inplace=True)
    #print(ingredient_series)

    #ingredient_list = ingredient_series #list(set(ingredient_list))
    #new_ingredient_list = []
    #for y in ingredient_list:
    #    ingredient_list.append(y+'<br>') 
    filtered_list = []
    add_list = 0
    for items in set(ingredient_list):
        for i in word_tokenize(items):
            ingr_bool = find_ingre_dict.is_it_ingredient(i)
            #print(i, ingr_bool) 
            if ingr_bool == True:
                add_list = 1
            else:
                add_list = 0
        if add_list == 1 :
            filtered_list.append(items.capitalize())
            add_list = 0
          

                
    return filtered_list

    #print(list(set(ingredient_list)))

    '''
    def get_captions(video_id):
        # retrieve the available transcripts
        
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)

            text = []
            for txt in transcript:
                text.append(txt['text'])
            return text

        except:
            print("Something else went wrong")
            ruledbase_parsed_text = parsing_hsk_v3.hsk(video_data)

            #transcript = data()
            transcript = ruledbase_parsed_text
            transcript =''.join(transcript)
            return transcript
    '''

