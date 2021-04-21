#!/usr/bin/env python
# coding: utf-8

# In[6]:


from konlpy.tag import Okt
import matplotlib.pyplot as plt
import numpy as np
okt=Okt()

import os
import re


# In[7]:


def make_list(location,keyword):
    f = open('datas/'+location+'/'+keyword+'.txt','r',encoding='utf-8')

    data=f.read().splitlines()
    for a in range(len(data)):
        data[a]=data[a].replace(',','').strip()
        data[a]=data[a].replace('\ufeff','')
        
    return data


# In[8]:


def make_key(directory, keyword):
    file = open('datas/'+directory+'/'+keyword+'.txt','r',encoding='utf-8')
    
    def clean(data):
        new = data.replace(",","")
        new = re.sub("'[^ ㄱ-ㅣ가-힣]+'", "",new)
        new = new.strip()
        return new
    
    n = 0
    blank = 'F'
    
    data = []
    post = []
    
    for line in file.readlines():
        l = line.splitlines()
 
        if l[0] != '' and blank == 'F':
            post.extend(l)
        
        elif l[0] !='' and blank == 'T':
            if n == 1:
                post.extend(l)
                n = 0
                blank = 'F'
                
            else:
                data.append(post)
                post = []
                post.extend(l)
                n = 0
                blank = 'F'
              
        elif l[0] == '':
            n += 1
            blank = 'T'
                
    data.append(post)
    file.close()
    
    return data


# In[9]:


def calculation(past,current,a,b):
   
    score=0
    if (past=='A' and current=='B') or (past=='B' and current=='A'): 
        score=a*b
        a=0
        b=0
        current=' '
        past=' '
    elif (past==' ' and current=='A') or (past=='A' and current==' ') or (past=='A' and current=='A'):
        score=a 
        a=0
        b=0
        current=' '
        past=' '
    else : 
        score=0
        a=a
        b=b
        current=current
        past=past
    output=[score,a,b,past,current]
    return output


# In[13]:


def score_key(key):
    
    symptom=make_list('new_dict','symptom')
    effect=make_list('new_dict','effect')
    up=make_list('new_dict','up')
    down=make_list('new_dict','down')

    score_total=0
    key_score=[]
    post_score=[]
    noline_count=0
    
    for posting in key:
        for line in posting:
            line_data=[] 
            line_pos=okt.pos(line,stem=True) 
            for pos in line_pos:
                #print(pos)
                if pos[0] in symptom:
                    line_data.append(['symptom',-1])
                elif pos[0] in effect:
                    line_data.append(['effect',1])
                elif pos[0] in down:
                    line_data.append(['down',-1])
                elif pos[0] in up:
                    line_data.append(['up',1])
                else :
                    line_data.append(' ')
    
            current_pos=' '
            line_score=[]
            a_score=0
            b_score=0
                
            for dict_key in line_data:
                if dict_key[0]=='symptom': 
                    a_score-=dict_key[1]
                    past_pos=current_pos
                    current_pos='A'
            
                elif dict_key[0]=='effect':
                    a_score+=dict_key[1]
                    past_pos=current_pos
                    current_pos='A'
                            
                elif dict_key[0]=='up':
                    past_pos=current_pos
                    current_pos='B'
                    if (past_pos==current_pos and abs(b_score)<=3): 
                        b_score+=dict_key[1]
                    elif (past_pos==current_pos and abs(b_score)>3):
                        b_score=pos[1]

                elif dict_key[0]=='down':
                    past_pos=current_pos
                    current_pos='B'
                    if (past_pos==current_pos and abs(b_score)==2): 
                        b_score+=dict_key[1]
                    elif (past_pos==current_pos and abs(b_score)>=3): 
                        b_score=dict_key[1]
                                
                else: 
                    past_pos=current_pos
                    current_pos=' '
                    
                calculate=calculation(past_pos,current_pos,a_score,b_score) 
                if calculate[0] != 0 :
                    line_score.append(calculate[0]) 
                a_score=calculate[1]
                b_score=calculate[2]
                past_pos=calculate[3]
                current_pos=calculate[4]

            line_num=0    
            for pos_num in line_score:
                line_num+=pos_num
                line_score=[]

                
                if line_num != 0:
                    post_score.append(line_num)               

        score=0
        for num in post_score: 
            score+=float(num)
        try: 
            key_score.append(round(score/len(post_score),3))
                    
            post_score=[]
        except ZeroDivisionError:
            pass

    all_score=0
    for post_score_index in range(len(key_score)): 
        all_score+=key_score[post_score_index]
    
    #return([key_score,round(all_score,3)])
    return([key_score,len(key_score)])


# In[14]:


def main():
    keyword=['락토바실러스'] # 시범적으로 예시 1개만 적용
    alpha=[]

    for i in range(1) :
        key=make_key('blog_crawling_data',keyword[i])
        alpha.append(score_key(key)[0])
        print(score_key(key)[1])


# In[15]:


main()


# In[ ]:




