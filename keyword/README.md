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
