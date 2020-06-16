#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import json
import math
import datetime
import requests
import urllib.request
import urllib.error
import urllib.parse
from bs4 import BeautifulSoup
from konlpy.tag import Okt
nlp = Okt()

#네이버 토큰 변경
naver_client_id = ""
naver_client_secret = ""


# In[ ]:


def naver_blog_crawling(search_blog_keyword, display_count, sort_type):

    search_result_blog_page_count = get_blog_search_result_pagination_count(search_blog_keyword, display_count)

    get_blog_post(search_blog_keyword, display_count, search_result_blog_page_count, sort_type)

    

def get_blog_search_result_pagination_count(search_blog_keyword, display_count):

    encode_search_keyword = urllib.parse.quote(search_blog_keyword)

    url = "https://openapi.naver.com/v1/search/blog?query=" + encode_search_keyword

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", naver_client_id)
    request.add_header("X-Naver-Client-Secret", naver_client_secret)

    response = urllib.request.urlopen(request)
    response_code = response.getcode()

    if response_code is 200:
        response_body = response.read()
        response_body_dict = json.loads(response_body.decode('utf-8'))

        if response_body_dict['total'] == 0:
            blog_pagination_count = 0

        else:
            blog_pagination_total_count = math.ceil(response_body_dict['total'] / int(display_count))

            if blog_pagination_total_count*10 >=1000 :
                blog_pagination_count = 1000

            else:
                blog_pagination_count = blog_pagination_total_count*10

            print("키워드 " + search_blog_keyword + " 에 해당하는 포스팅 수 : " + str(response_body_dict['total']))

        return blog_pagination_count


# In[ ]:



def get_blog_post(search_blog_keyword, display_count, search_result_blog_page_count, sort_type):

    stop_list_title=['한의','병원','프리허그','개미','공식','하늘마음','피부','뷰티','검색','화장품','님의','새집증후군','에셋','한방','의원','경매','렌탈','한약',
               '공동구매','공구','클리닉','주식','금융','투자','한의원','기자','펀드','증권','부동산','힐링스토리','의료','치료','아토피','Laboratory','Lab']
    stop_list_text=['무상제공','공동구매','공구','후원','제공','업체','소정','작성','마감','상한가','하한가','소개','제품','생리전증후군','월경전증후군']


    file = open("datas/blog_crawling_data/락토바실러스.txt","w", encoding='utf-8')
    encode_search_blog_keyword = urllib.parse.quote(search_blog_keyword)

    a=0
    for i in range(1,search_result_blog_page_count ,10 ):
        print('게시물수:',str(i))

        url = "https://openapi.naver.com/v1/search/blog?query=" + encode_search_blog_keyword +"&display=" + str(display_count) + "&start=" + str(i) + "&sort=" + sort_type

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", naver_client_id)
        request.add_header("X-Naver-Client-Secret", naver_client_secret)

        response = urllib.request.urlopen(request)
        response_code = response.getcode()

        if response_code is 200:
            response_body = response.read()
            response_body_dict = json.loads(response_body.decode('utf-8'))

            for j in range(0, len(response_body_dict['items'])):
                try:
                    blog_post_url = response_body_dict['items'][j]['link'].replace("amp;", "")

                    get_blog_post_content_code = requests.get(blog_post_url)
                    get_blog_post_content_text = get_blog_post_content_code.text
                    get_blog_post_content_soup = BeautifulSoup(get_blog_post_content_text, 'lxml')

                    for link in get_blog_post_content_soup.select('iframe#mainFrame'):
                        real_blog_post_url = "http://blog.naver.com" + link.get('src')
                        get_real_blog_post_content_code = requests.get(real_blog_post_url)
                        get_real_blog_post_content_text = get_real_blog_post_content_code.text
                        get_real_blog_post_content_soup = BeautifulSoup(get_real_blog_post_content_text, 'lxml')
                        
                        if get_real_blog_post_content_soup.find("div", {"class": "se-main-container"}) is not None:
                            component = 'div.se-main-container'

                        elif get_real_blog_post_content_soup.find("div", {"id": "postViewArea"}) is not None:
                            component = '#postViewArea'   

                        else:
                            component = '#postListBody'

                        for blog_post_content in get_real_blog_post_content_soup.select(component):    

                            blog_post_content_text = blog_post_content.get_text()
                            clean = re.compile('[^ .,!?~가-힣]+')
                            new_content =  re.sub(clean,"", blog_post_content_text)
                            clean1 = re.compile('[.!?~]+')
                            new_content =  re.sub(clean1,"\n", new_content)
                            remove_html_tag = re.compile('<.*?>')
                            blog_post_title = re.sub(remove_html_tag, '', response_body_dict['items'][j]['title'])
                            blog_post_postdate = datetime.datetime.strptime(response_body_dict['items'][j]['postdate'],"%Y%m%d").strftime("%y.%m.%d")
                            blog_post_blogger_name = str(response_body_dict['items'][j]['bloggername'])

                            blog_post_full_contents = str(new_content)

                            for stopword in stop_list_title:
                                if stopword in blog_post_blogger_name:
                                    blog_post_full_contents=''
                                    
                            for stopword in stop_list_text:
                                if stopword in blog_post_full_contents:
                                    blog_post_full_contents=''
                                    
                            if len(blog_post_full_contents)>3:
                                final_text = blog_post_full_contents.splitlines()
                                    #print(final_text)
                            
                                for line in final_text :
                                    if len(line)>2:
                                        file.write(line+'\n')
                        
                                file.write('\n\n')
                                a+=1
                                print(blog_post_blogger_name, a )
                               
                except:
                    file.write("포스팅 URL : " )
                    j += 1
    file.close()


if __name__ == '__main__':

    naver_blog_crawling("아토피+치료", 10, "sim")

