from flask import Flask,jsonify, render_template, request
import socket
import os, os.path
from sum import load_model,summary_text
from down_movie import downYoutubeMp3, down_title
from stt import upload_blob_from_memory,transcribe_gcs

app = Flask(__name__)
models = list()
contents = list()
movie_urls = list()
movie_titles = list()
myips = list()
text_alls = list()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/심종수/Desktop/************.json"

@app.route('/')
def home():
    myip = socket.gethostbyname(socket.gethostname())
    myips.append(myip)
    return render_template('index.html', ip = myip)

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        movie_url = result.get('address')
        movie_urls.append(movie_url)
        # 동영상 이름 추출
        movie_title = down_title(movie_url)
        movie_titles.append(movie_title)

        # 파일 이름 정의
        content = movie_title + '.flac'
        contents.append(content)
        # 임베딩 링크 생성
        embed_url = movie_url.replace('watch?v=', "embed/")

    return render_template('result.html',embed_url=embed_url, movie_title = movie_title,
                           ip = myips[0])

# @app.route('/down',methods = ['POST', 'GET'])
# def down():
#     if request.method == 'POST':
#         # 동영상 다운
#         downYoutubeMp3(movie_urls[0])
#
#         # 동영상 path가져오기
#         path = os.getcwd()
#         folder_yt = "yt"
#         file_path = os.path.join(path, folder_yt, contents[0])
#
#         # 동영상 스토리지 업로드
#         upload_blob_from_memory("dgu_dsc_stt", file_path, contents[0])
#         print("ㅇㅋ")
#     return "동영상 다운로드 및 스토리지 업로드 완료"

@app.route('/text',methods = ['POST', 'GET'])
def text():
    if request.method == 'POST':
        # 동영상 다운
        downYoutubeMp3(movie_urls[0])

        # 동영상 path가져오기
        path = os.getcwd()
        folder_yt = "yt"
        file_path = os.path.join(path, folder_yt, contents[0])

        # 동영상 스토리지 업로드
        upload_blob_from_memory("dgu_dsc_stt", file_path, contents[0])

        # 동영상 STT
        # 스토리지 path
        gcs_url = "gs://dgu_dsc_stt/"
        gcs_file = gcs_url + contents[0]
        try:
            text_all = transcribe_gcs(gcs_file, contents[0], 44100)
        except:
            text_all = transcribe_gcs(gcs_file, contents[0], 48000)

        text_alls.append(text_all)
        print(text_all)
    return jsonify({'text_all': text_all})

@app.route('/summary',methods = ['POST', 'GET'])
def summary():
    if request.method == 'POST':
        # 모델 로드
        model = load_model()
        models.append(model)
        # 요약문 생성
        sum_text = summary_text(text_alls[0], models[0])
        print(sum_text)
    return jsonify({'sum_text': sum_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)