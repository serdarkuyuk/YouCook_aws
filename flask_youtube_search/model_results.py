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
from flask_youtube_search import parsing_hsk_v3







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
        
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        text = []
        for txt in transcript:
            text.append(txt['text'])
        return text

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

    ner = load_model("/Users/serdarkuyuk/Documents/harvard/serdar/insight/youtube/flaskyoucook/youCOOK_v2/flask_youtube_search/models")

    
    #print(''.join(test_sentences))
    
    #for x in test_sentences:
    doc = ner(''.join(test_sentences))
    #    displacy.render(doc, jupyter = True, style = "ent")
    #doc = ner(x)
    ingredient_list=[]
    for x in doc.ents:
        ingredient_list.append(x.text) # +'<br>'

    ingredient_list = list(set(ingredient_list))
    #new_ingredient_list = []
    #for y in ingredient_list:
    #    ingredient_list.append(y+'<br>') 

    return ingredient_list

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

