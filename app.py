from flask import Flask, render_template, request
import socket
import os, os.path

import down_movie
import sum
from sum import load_model,summary_text
from down_movie import downYoutubeMp3, down_title

app = Flask(__name__)
models = list()

@app.route('/')
def home():
    myip = socket.gethostbyname(socket.gethostname())
    return render_template('index.html', ip = myip)

@app.route('/summary',methods = ['POST', 'GET'])
def summary():
    if request.method == 'POST':
        result = request.form
        movie_url = result.get('address')

        # 동영상 다운
        downYoutubeMp3(movie_url)

        # 동영상 이름 추출
        movie_title = down_title(movie_url)
        content = movie_title + + '.flac'

        # 동영상 path가져오기
        path = os.getcwd()
        folder_yt = "yt"
        contents = os.path.join(path, folder_yt, content)

        # 동영상 스토리지 업로드
        upload_blob_from_memory("dgu_dsc_stt",contents,content)

        # 동영상 STT
        # 스토리지 path
        gcs_url = "gs://dgu_dsc_stt/"
        gcs_file = gcs_url + content

        text_all = transcribe_gcs(gcs_file)
        ## summary
        #모델 로드
        models.append(sum.load_model())

        #요약문 생성
        sum_text = sum.summary_text(text,models[0])

    return render_template('summary.html', movie_url=movie_url, text_all = text_all,
                           sum_text = sum_text, movie_title = movie_title)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)