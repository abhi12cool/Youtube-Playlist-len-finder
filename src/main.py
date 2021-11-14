from googleapiclient.discovery import build
import googleapiclient
from datetime import timedelta
import os
import re

api_key = os.environ.get('YouTube API')

youtube = build('youtube', 'v3', developerKey=api_key)

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

total_seconds = 0

nextPageToken = None

while True:
    playlist = input("Please enter the playlist link : ")
    try:
        playlist = playlist.split("=")[1]
    except:
        playlist = playlist
        
    pl_request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId = playlist,
        maxResults = 50,
        pageToken = nextPageToken
    )
    try:
        pl_response = pl_request.execute()
        vid_ids = []
        for item in pl_response['items']:
            vid_ids.append(item['contentDetails']['videoId'])
            
        vid_request = youtube.videos().list(
            part = 'contentDetails',
            id =','.join(vid_ids)
        )

        for item in vid_request.execute()['items']:
            duration = item['contentDetails']['duration']
            
            hours = hours_pattern.search(duration)
            minutes = minutes_pattern.search(duration)
            seconds = seconds_pattern.search(duration)
            
            hours = int(hours.group(1)) if hours else 0
            minutes = int(minutes.group(1)) if minutes else 0
            seconds = int(seconds.group(1)) if seconds else 0
            
            video_seconds = timedelta(
                hours = hours,
                minutes = minutes,
                seconds = seconds
            ).total_seconds()
            
            total_seconds += video_seconds
        
        nextPageToken = pl_response.get('nextPageToken')
        
        if not nextPageToken:
            break
    except googleapiclient.errors.HttpError:
        print("No such Playlist")
    
total_seconds = int(total_seconds)

minutes, seconds = divmod(total_seconds, 60)
hours, minutes = divmod(minutes, 60)

print(f'The Playlist Length is : {hours}:{minutes}:{seconds}')