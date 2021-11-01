from youtube_transcript_api import YouTubeTranscriptApi

video_id = '_PbNqiWNlzQ'
lang = 'ru'
transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

try:
    transcript = transcript_list.find_manually_created_transcript([lang])
    srt = transcript.fetch()
    with open("subtitles.txt", "w") as f:
        # iterating through each element of list srt
        for i in srt:
        # writing each element of srt on a new line
            f.write("{}\n".format(i))
except Exception:
    print(f"Can't find manual subtitles in lang {lang} for video https://youtube.com/watch?v={video_id}")
