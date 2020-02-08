from __future__ import absolute_import
import requests
from isodate import parse_duration
import random

from flask import Blueprint, render_template, current_app, request, redirect
from flask_youtube_search import model_results
from yelpapi import YelpAPI
#from flask_youtube_search import yelp_crediatials


class YelpAnalyzer():
    """
    Class holds the search results from yelp for spesific query
    """

    def __init__(self):
        self.client_id = current_app.config['YELP_CLIENT_ID']
        self.api_key =  current_app.config['YELP_API_KEY']
#yelp_crediatials.api_key
#yelp_crediatials.client_id 
    def search_yelp(self, youcook_search_query):
        yelp_api = YelpAPI(self.api_key)
        term = youcook_search_query
        location = 'Boston'
        search_limit = 5
        response = yelp_api.search_query(term = term,
                                         location = location,
                                         limit = search_limit,
                                         sort_by="rating",
                                         open_now = True,
                                         price="1"
                                         )
        #randomly select of the restaurants for diversity
        random_int = random.randint(0, search_limit-1)
        rand_response = response["businesses"][random_int]

        return rand_response["url"] #return url of the restaurant

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    videos = []
    
    if request.method == 'POST':

        #define search parameters
        search_params = {
            'key' : current_app.config['YOUTUBE_API_KEY'],
            'q' : request.form.get('query'),
            'part' : 'snippet',
            'maxResults' : 9,
            'type' : 'video',
            'videoCaption' : 'closedCaption'
        }


        #get search results
        r = requests.get(search_url, params=search_params)

        #parse the request and get items
        results = r.json()['items']

        #get list of video ID's which will be used to get captions
        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])


        yelp = YelpAnalyzer()

        #if "I am hungry" button submitted, first yelp advise will be directed 
        if request.form.get('submit') == 'lucky':
            youcook_search_query = request.form.get('query') #gets the user query
            yelp_url = yelp.search_yelp(youcook_search_query)   #search at yelp
            return redirect(yelp_url)  
        
        #define video search parameters   
        video_params = {
            'key' : current_app.config['YOUTUBE_API_KEY'],
            'id' : ','.join(video_ids),
            'part' : 'snippet,contentDetails',
            'maxResults' : 9
        }

        #get video results with video parameters
        r = requests.get(video_url, params=video_params)
        results = r.json()['items'] #parse the request and get items

        #for each video 
        for result in results:

            #video identifiers            
            video_data = {
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'title' : result['snippet']['title']
            }

            #extract ingredienst 
            list_ingredients = model_results.extract_ingredients(str(result["id"]))

            #make list to publish in website
            if len(list_ingredients) > 15:
                #if number of ingredients 15, show in the other colomn
                video_data['ingredients_p1'] = list_ingredients[:15]   
                video_data['ingredients_p2'] = list_ingredients[15:31]
            elif len(list_ingredients) == 0: 
                video_data['ingredients_p1'] = ["No English Captions"]
                video_data['ingredients_p2'] = ["Advise: You can still make it by watching video!!!"]
            else:
                video_data['ingredients_p1'] = list_ingredients[:15]
                video_data['ingredients_p2'] = []

            videos.append(video_data)

    return render_template('index.html', videos=videos)





