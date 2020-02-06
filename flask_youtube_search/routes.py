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
        search_params = {
            'key' : current_app.config['YOUTUBE_API_KEY'],
            'q' : request.form.get('query'),
            'part' : 'snippet',
            'maxResults' : 9,
            'type' : 'video',
            'videoCaption' : 'closedCaption'
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.form.get('submit') == 'lucky':
            print(video_ids[0])
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')
            
        video_params = {
            'key' : current_app.config['YOUTUBE_API_KEY'],
            'id' : ','.join(video_ids),
            'part' : 'snippet,contentDetails',
            'maxResults' : 2
        }
#result['snippet']['description']
        r = requests.get(video_url, params=video_params)
        results = r.json()['items']
        for result in results:
            video_data = {
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'title' : result['snippet']['title'],
                'description' : result['snippet']['description'],
                'description2' : 'som'
                #'language' : result['snippet'][language
            }
            #ruledbase_parsed_text = parsing_hsk_v3.hsk(video_data['description'])
            #print(type(result["id"]))

            results1= model_results.hsk_result(str(result["id"]))
            if len(results1) > 15:
                video_data['description'] = results1[:15] #''.join(results)
                video_data['description2'] = results1[15:31]
            else:
                video_data['description'] = results1[:15]
                video_data['description2'] = []
            videos.append(video_data)
    return render_template('index.html', videos=videos)





