# Product Effectiveness Measurement Algorithm(PEM)
Product Effectiveness Measurement Algorithm

##### 본 프로젝트는 "온라인 고객 리뷰를 활용한 제품 효과 분석 기법(A TECHNIQUE FOR PRODUCT EFFECT ANALYSIS USING ONLINE CUSTOMER REVIEWS)"에 
##### 제안된 텍스트로부터 효과를 측정할 수 있는 제품 효과 측정 알고리즘 (Product Effectiveness Measurement, PEM)의 재현을 위해 생성되었습니다.

 본 프로젝트에 대한 논문은 http://ktsde.kips.or.kr/digital-library/23873 에서 확인하실 수 있습니다.
 
 업로드 된 코드는 다음과 같습니다.

* Naver_blog_crawling.py : 네이버 블로그 포스팅의 크롤링을 위한 코드로 광고제거 등의 전처리가 추가되어 있습니다.
* tf-idf_word2vec.py : 4가지의 효과, 증상, 증가, 감소 사전을 제작하기 위한 코드이며 단어의 TF-IDF 가중치를 반환하여 중요단어를 추출한 후,
                       word2vec으로부터 주변단어를 추출하여 사전을 확장하여 사전 제작에 도움을 줄 수 있습니다. 
* PEM.py : 프로젝트의 메인이 되는 코드로 Product Effectiveness Measurement에 관한 코드 입니다.



본 저장소의 PEM.py의 올바른 사용을 위해서는 tf-idf_word2vec.py을 이용한 4가지의 사전 구축이 필요합니다.

그 예시는 다음과 같으며, 본 프로젝트의 data/dict에 있습니다.

#### 1. effect

호전, +1

개선, +1

환하다, +1

#### 2. symptom

어지러움, -1

붉어짐, -1

가려움, -1

#### 3. up

너무, +1

늘어나다, +1

갖다, +1

#### 4. down

불편하다, -1

없어지다, -1

적다, -1

