import os
import requests

from youtube_transcript_api import YouTubeTranscriptApi

channels = [ 
    'UCMCgOm8GZkHp8zJ6l7_hIuA', # Juri Dudz
    'UCklUqFEcJqFnWKEBozw5p4g', # Russian with Max
    'UC101o-vQ2iOj9vr00JUlyKw', # Varlamov Live
    'UCzlzGhKI5Y1LIeDJI53cWjQ', # Urgant
    'UC2tsySbe9TNrI-xh2lximHA', # A4
    'UC8M5YVWQan_3Elm-URehz9w', # Utopia show
    'UCF0ZeqSkybD1aFtFxjA8z9w', # Russian Progress
    'UCaoKqmANMlBIJWyWJPUU9YA', # Tatiana Klimova
    'UCQg2AzkYEueS5giD84wxLdg', # RU-Land club
    'UCQwRlx8hVI-CFv_E-v5s84Q', #  Адвокат Егоров 
    'UCU_a2V_uDPSxvbV2B0tW7vA', #  Всё как у зверей
    'UC6cqazSR6CnVMClY0bJI0Lg', # Bad Comedian
    'UCU_yU4xGT9hrVFo6euH8LLw', # Slivki Show
    'UCxDZs_ltFFvn0FDHT6kmoXA' # Bald and Bankrupt
]

lang = 'ru'
yt_api_key = os.getenv("YT_API_KEY")
#published_after = "2021-11-01T16:00:00Z"
published_after = "1990-11-01T16:00:00Z"
videos = []

def fetch_channel_videos(channel_id, api_key, next_page_token):
    uri = f'https://www.googleapis.com/youtube/v3/search?channelId={channel_id}&key={api_key}&maxResults=50&publishedAfter={published_after}'
    if next_page_token:
        uri = f'{uri}&pageToken={next_page_token}'
    r = requests.get(uri)
    result = r.json()
    print(result)
    return result

def fetch_single_video(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_manually_created_transcript([lang])
        srt = transcript.fetch()
        with open(f"subtitles_{video_id}_{lang}.txt", "w") as f:
            # iterating through each element of list srt
            for i in srt:
            # writing each element of srt on a new line
                f.write("{}\n".format(i))
    except Exception:
        print(f"Can't find manual subtitles in lang {lang} for video https://youtube.com/watch?v={video_id}")


for channel_id in channels:
    next_page_token = None
    print(f'Processing channel: {channel_id}')
    vids_and_data = fetch_channel_videos(channel_id, yt_api_key, next_page_token)
    if 'items' in vids_and_data:
        for item in vids_and_data['items']:
            if item['id']['kind'] == "youtube#video":
                videos.append(item['id']['videoId'])
        if 'nextPageToken' in vids_and_data:
            next_page_token = vids_and_data['nextPageToken']
        while next_page_token:
            print('Processing next channel page...')
            vids_and_data = fetch_channel_videos(channel_id, yt_api_key, next_page_token)
            if 'items' in vids_and_data:
                for item in vids_and_data['items']:
                    if item['id']['kind'] == "youtube#video":
                        videos.append(item['id']['videoId'])
                if 'nextPageToken' in vids_and_data:
                    next_page_token = vids_and_data['nextPageToken']
                else:
                    next_page_token = None
            else:
                next_page_token = None

print(f'Found {len(videos)} videos')
for video_id in videos:
    print(f"Processing video: {video_id}")
    fetch_single_video(video_id)
