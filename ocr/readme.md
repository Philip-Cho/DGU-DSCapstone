## [참고사항]
현재는 Google API Client를 통해 작업했으나, 웹과 연동하기 위해서는 Rest API 방식으로 변경할 수도 있음
- [Rest 방식 참고](https://cloud.google.com/vision/docs/reference/rest?hl=ko)

## [기능]
- 영어 인식
- 한국어 인식
  - 중간발표/demo 등에서 한국어 강의에 대해 STT 기능은 제공 못하나 한글도 텍스트 추출은 가능함을 소개(교수님 강의 영상 활용)
  - 추후 발전 가능성으로 한국어 인식률 높이는 방법도 고안할 것이라 주장
- 현재는 로컬이미지로 테스트를 진행했으나, 구글 스토리지를 연동하여 사용할 것 (방법: Reference 참고)

## [과정]
```
while end:
  이미지 캡처 
  이미지 스토리지 저장 
  OCR process (image to text)
프로그램 종료시 해당 영상을 들으며 캡처한 이미지 모두 삭제
```

 ## [References]
 1. [API 세팅 및 사용법1](https://davelogs.tistory.com/36?category=928468)
 2. [API 세팅 및 사용법2](https://ssamko.tistory.com/47)
 3. [Google Introduction](https://cloud.google.com/vision/docs/handwriting?hl=ko)
 4. [API Setting](https://cloud.google.com/vision/docs/setup?hl=ko)
 5. [Flask 서버 Google API 연동](https://gist.github.com/WGierke/c2d00580104de4ea9f82bae7bc846292)
