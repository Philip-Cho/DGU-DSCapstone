# Corpus data_open-research data
과학분야 research abstract
### 1. 데이터 다운로드 
- 필요 모듈 설치 (wget(window))  
  참고자료: https://sound10000w.tistory.com/229
  1. https://eternallybored.org/misc/wget/ 다운로드, 설치  
  2. 다운받은 exe 파일을 C:/Windows/System32 폴더로 이동(관리자 권한 창 뜨면 "계속" 선택)  
  3. 제어판/시스템/고급시스템설정/환경변수/시스템변수/PATH exe 파일 경로 추가  


- 데이터 다운로드(cd로 디렉토리 먼저 지정해주기!)
  1. 데이터 파일 목록(manifest.txt) 다운로드  
  cmd에서 wget https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/2022-04-05/manifest.txt 입력  
  0~10 파일만 다운로드 받고 싶다면 해당 파일명 외 다른 파일명은 삭제 후 저장
     
  2. 데이터 파일 다운로드  
  cmd에서 wget -B https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/2022-04-05/ -i manifest.txt 입력  
  이전 스텝에서 받은 데이터 파일 목록(manifest.txt)에 있는 파일만 다운로드  
  총 6000파일, 약 170GB(압축 해제 후 약 350GB)

### 2. 데이터 전처리
- summarization_model/preprocessing_corpus.ipynb 파일 코드 실행
- 구글 드라이브 업로드
  - 0~999: https://drive.google.com/file/d/1H0TF8RhQR_qIWKMBVUL9WEadCTwZvb8p/view?usp=sharing

# Summarization data
