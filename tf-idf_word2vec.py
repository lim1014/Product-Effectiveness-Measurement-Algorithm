#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
import codecs

okt=Okt()


# In[ ]:


def get_words(data):
    tokens=okt.pos(data,stem=True)
    result=[word for word, tag in tokens if (len(word)>1 and (tag=="Noun" or tag=="Verb" or tag=="Adjective" or tag=="Adverb" or tag=="Determiner"))]
    return result


# In[ ]:


# TF-IDF를 활용한 중요단어 추출을 위한 코드

openfile = 'data/blog_crawling_data/감마리놀렌산.txt'
with codecs.open(openfile, 'r', 'utf-8') as f:
    lines = f.readlines() 
        
cv = CountVectorizer(max_features=100000, tokenizer=get_words)
tdm=cv.fit_transform(lines)
    
tfidf=TfidfTransformer() 
tdm2= tfidf.fit_transform(tdm)
    
words=cv.get_feature_names()
    
s = open('data/dict_words/감마리놀렌산.txt','w',encoding='utf-8')
for i, n in sorted(zip(tdm2[0].data, tdm2[0].indices),reverse=True):
    s.write(words[n]+', '+str(i)+'\n')
        
f.close()
s.close()


# #### 위 코드의 결과를 가지고 1차적인 사전(up, down, effect, symptom)을 제작함.

# In[ ]:


# Word2vec을 활용한 주변단어 추출을 위한 코드

fread = open('data/blog_crawling_data/락토바실러스.txt','rt',encoding='UTF8')
# fread위치에 사전 제작시 고려하는 모든 키워드의 데이터를 삽입하나, 
# 시범적 확인을 위해 편의상 중요단어 추출 이외의 키워드 크롤링 데이터를 적용함
n=0
result = []

while True:
    line = fread.readline() #한 줄씩 읽음.
    if not line: break # 모두 읽으면 while문 종료.
    n=n+1
    if n%5000==0: # 5,000의 배수로 While문이 실행될 때마다 몇 번째 While문 실행인지 출력.
       # print("%d번째 While문."%n)
    tokenlist = okt.pos(line, stem=True, norm=True) # 단어 토큰화
    temp=[]
    for word in tokenlist:
        if word[1] in ["Noun"or "Adjective"or "Adverb" or "Verb" or "Determiner"]: 
            temp.append((word[0])) 
    if temp: 
        result.append(temp) 
fread.close()


# In[ ]:


from gensim.models import Word2Vec
model = Word2Vec(result, size=100, window=3, min_count=5, workers=4, sg=0)


# In[ ]:


model.save('word.model')


# #### 1차적으로 제작된 사전의 단어를 중심단어로 하여 주변단어를 추출하여 사전 확장

# In[ ]:


from gensim.models import Word2Vec

model = Word2Vec.load('word.model')

s_dict = open("data/dict/symptom.txt",'r', encoding='UTF8')
e_dict = open("data/dict/effect.txt",'r', encoding='UTF8')

s_word = s_dict.readlines()
e_word =  e_dict.readlines()

s_list=[]
e_list=[]

s_list_1 = []
e_list_1= []

sword = []
eword = []

#print('--------------------------------------------------------------------------------------------------\n증상예외\n') 
for w in s_word:
    w = w.replace('\n','')
    w = w.replace(' ','')
    sword.append(w)
    
    try:
        s = model.wv.most_similar(w)
        for i in s:
            if i[0] not in s_list:
                if i[0] not in sword:
                    s_list.append(i[0])

    except:
        #print(w)

#print('--------------------------------------------------------------------------------------------------\n효과예외\n') 
for w in e_word:
    w = w.replace('\n','')
    w = w.replace(' ','')
    eword.append(w)
    
    try:
        e = model.wv.most_similar(w)
        for m in e:
            if m[0] not in e_list:
                if m[0] not in eword:
                    e_list.append(m[0])

    except:
        #print(w)
        
for s in s_list:
    if s not in sword:
        s_list_1.append(s)
        
for e in e_list:
    if e not in eword:
        e_list_1.append(e)
        
print('--------------------------------------------------------------------------------------------------\n\n')        
print(s_list_1)

print('--------------------------------------------------------------------------------------------------\n\n') 
print(e_list_1)


# In[ ]:


u_dict = open("data/dict/up.txt",'r', encoding='UTF8')
d_dict = open("data/dict/down.txt",'r', encoding='UTF8')

u_word = u_dict.readlines()
d_word =  d_dict.readlines()

uword = []
dword = []

u_list=[]
d_list=[]

u_list_1 = []
d_list_1 = []

#print('--------------------------------------------------------------------------------------------------\n증상예외\n') 
for u in u_word:
    u = u.replace('\n','')
    u = u.replace(' ','')
    uword.append(u)
    
    try:
        uu = model.wv.most_similar(u)
        for n in uu:
            if n[0] not in u_list:
                if n[0] not in u_word:
                    u_list.append(n[0])

    except:
 #       print(u)

#print('--------------------------------------------------------------------------------------------------\n효과예외\n') 
for d in d_word:
    d = d.replace('\n','')
    d = d.replace(' ','')
    dword.append(d)
    
    try:
        dd = model.wv.most_similar(d)
        for k in dd:
            if k[0] not in d_list:
                if k[0] not in d_word:
                    d_list.append(k[0])

    except:
 #       print(d)

        
for u in u_list:
    if u not in uword:
        u_list_1.append(u)
        
for d in d_list:
    if d not in d_word:
        d_list_1.append(d)
        
print('--------------------------------------------------------------------------------------------------\n\n')        
print(u_list_1)
print('--------------------------------------------------------------------------------------------------\n\n') 
print(d_list_1)

