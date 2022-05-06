from __future__ import unicode_literals
import youtube_dl
import os
from pytube import YouTube

def downYoutubeMp3(url):
    # 실행되는 폴더 안에 '영상제목.확장자' 형식으로 다운로드
    output_dir = os.path.join('./yt', '%(title)s.%(ext)s')

    ydl_opts = {
        'outtmpl': output_dir,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'flac',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("동영상 추출")
    print("음성 추출")
    yt_title = '%(title)s'
    return yt_title

def down_title(url):
    video_url = url
    yt = YouTube(video_url)

    # # 특정영상 다운로드 - mp4인데 오디오만 다운받음.
    # yt.streams.filter(only_audio=False).first().download('/yt')
    print("강의 영상 제목추출")
    return yt.title