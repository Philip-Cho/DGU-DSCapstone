# 문제 생성(TextRank, KeyBERT)
- **keyword.py  
  -> keyword: KeyBERT, keysentence: TextRank 사용**  (이 코드 사용!)   
  둘 다 TextRank 사용했을 때보다 keyword 추출 성능이 좋음   
  
- textrank.py  
  -> keyword, keysentence 모두 TextRank 사용  
  
### keyword.py 실행
key_question(script_path='sctipt_path.txt', weighted_keywords=Fasle:Default) 함수  
: 강의 script 중 keysentence 찾고 그 문장 내에 중요도 높은 키워드 있을시 해당 키워드를 blank로 뚫어줌
1. weighted_keywords=False: Default
  keysentence with blank, keysentence, keyword 리턴  
  ![image](https://user-images.githubusercontent.com/88622845/168466248-91b552d8-7f5c-4f9a-b440-ddf1f1957db2.png)  

3. weighted_keywords=True  
   keyword 별 가중치(중요도) 리턴  
   ![image](https://user-images.githubusercontent.com/88622845/168466273-8bb42b7f-995b-4ce0-8e2c-d5de45c587ab.png)  

### make_wordfile()
: STT 성능 개선에 필요한 단어 수집을 위한 함수
1. YouTube의 이공계(CS, DS, Engineering, Statistics, etc.) 강의 중 채널에서 직접 자막 추가한 강의의 자막 추출
2. 자막 스크립트 저장된 디렉토리의 txt 파일 이름 리스트 형태로 추출(os.listdir())
3. 해당 리스트 for문 돌면서 각 스크립트 make_wordfile 실행  
    1. key_question 함수 실행하여 키워드 10개 추출(KeyBERT 성능이 괜찮아서 거의 이공계 단어로 추출됨)
    2. sciwords.txt 파일에 10개 키워드 저장, 중복 제외
4. 수작업으로 이공계의 전문단어가 아닌 단어 삭제
