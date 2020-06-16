#!/usr/bin/env python
# coding: utf-8

# In[1]:


from konlpy.tag import Okt
okt=Okt()

def get_words(data):
    tokens=okt.pos(data,stem=True)
    result=[word for word, tag in tokens if (len(word)>1 and (tag=="Noun" or tag=="Verb" or tag=="Adjective" or tag=="Adverb" or tag=="Determiner"))]
    return result
   


# In[2]:


openfile = 'data/blog/아토피.txt'
f = open(openfile, 'r', encoding='utf-8')
data=f.read()
print(get_words(data))


# In[6]:


from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
import codecs


openfile = 'data/blog/아토피.txt'
with codecs.open(openfile, 'r', 'utf-8') as f:
    lines = f.readlines() 
        
cv = CountVectorizer(max_features=100000, tokenizer=get_words)
tdm=cv.fit_transform(lines)
    
tfidf=TfidfTransformer() 
tdm2= tfidf.fit_transform(tdm)
    
words=cv.get_feature_names()
    
s = open('datas/new_dict_words/아토피_new.txt','w',encoding='utf-8')
for i, n in sorted(zip(tdm2[0].data, tdm2[0].indices),reverse=True):
    s.write(words[n]+', '+str(i)+'\n')
        
f.close()
s.close()


# In[ ]:




