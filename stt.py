import os, os.path
from google.cloud import storage
from google.cloud import speech

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/심종수/Desktop/*********.json"

# 스토리지 업로드
def upload_blob_from_memory(bucket_name, contents, destination_blob_name):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(contents)

    print(
        "{} with contents {} uploaded to {}.".format(
            destination_blob_name, contents, bucket_name
        )
    )


# STT
def transcribe_gcs(gcs_uri, content, sample_rate_hertz):
    print("STT 시작")
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        # wav 파일이므로 Linear16, Flac 파일은 FLAC
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        # hertz 16000, 44100(2개의 오디오 채널), Flac은 또 다르다.
        sample_rate_hertz=sample_rate_hertz, # 48000
        language_code="en-US",
        audio_channel_count=2,
        enable_separate_recognition_per_channel=True,
        enable_automatic_punctuation=True)

    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result()
    #     text =  ''
    #     for temp in response.results:
    #         text += temp.alternatives[0].transcript

    text_2 = ''
    text_1 = ''

    for result in response.results:
        if result.channel_tag == 2:
            text_2 += result.alternatives[0].transcript + ' '
        else:
            text_1 += result.alternatives[0].transcript + ' '

    # path가져오기
    path = os.getcwd()
    folder_text = "text"
    text_file = os.path.join(path, folder_text, content)

    f = open('{}.txt'.format(text_file), 'w')
    f.write(text_2)
    f.close()
    print("STT 완료")

    return text_2