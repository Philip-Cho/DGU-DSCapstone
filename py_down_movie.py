from __future__ import unicode_literals
import youtube_dl
import os


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

if __name__ == '__main__':
    downYoutubeMp3("https://www.youtube.com/watch?v=8jQ7q3UeyiE")