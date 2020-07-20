# Effect-Analysis-Algorithm
Effect Analysis Algorithm

 본 프로젝트는 "소셜 미디어를 위한 효과 분석 알고리즘 기반의 감성 분석 기법"에 제안된 효과분석 알고리즘의 재현을 위해 생성되었습니다.
 (추가 설명 수정 예정)
 
 업로드 된 코드는 다음과 같습니다.

* naver_blog_crawling.py : 네이버 블로그 포스팅을 위한 코드로 광고를 제거하는 알고리즘이 추가되어 있습니다.
* document_maker_tfidf.py : 4가지의 효과, 증상, 증가, 감소 사전을 제작하기 위해 단어의 TF-IDF 가중치를 계산하고 반환합니다.
* Effect Analysis Algorithm.py : 프로젝트의 메인이 되는 코드로 효과 분석 알고리즘에 관한 코드 입니다.



본 저장소의 Effect Analysis Algorithm.py의 올바른 사용을 위해서는 document_maker_tfidf.py을 이용한 4가지의 사전 구축이 필요합니다.
그 예시는 다음과 같습니다.

### 1. effect

호전, +1

개선, +1

환하다, +1

### 2. symptom

어지러움, -1

붉어짐, -1

가려움, -1

### 3. up

너무, +1

늘어나다, +1

갖다, +1

### 4. down

불편하다, -1

없어지다, -1

적다, -1
