from __future__ import absolute_import
import requests
from isodate import parse_duration

from flask import Blueprint, render_template, current_app, request, redirect
from flask_youtube_search import parsing_hsk_v3
from flask_youtube_search import model_results

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

        #if "I am hungry" button submitted, first video will be directed 
        if request.form.get('submit') == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')
        
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
            else:
                video_data['ingredients_p1'] = list_ingredients[:15]
                video_data['ingredients_p2'] = []

            videos.append(video_data)

    return render_template('index.html', videos=videos)





