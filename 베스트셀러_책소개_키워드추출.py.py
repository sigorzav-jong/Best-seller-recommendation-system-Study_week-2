#!/usr/bin/env python
# coding: utf-8

# In[3]:


pip install openpyxl


# In[1]:


import pandas as pd


# In[2]:


df = pd.read_excel('베스트셀러 크롤링 데이터.xlsx')


# In[6]:


#불필요한 컬럼 제거 
del df['Unnamed: 0'] 


# In[9]:


#결측값 확인 
def print_book_info(df):
    print(df.info())
    print('*' * 90)
    print('*' * 90)
    print('')

print('Total')
print_book_info(df)


# In[10]:


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# In[11]:


import nltk
nltk.download('averaged_perceptron_tagger')


# #### '책소개'컬럼에서 키워드 추출 

# In[13]:


def extract_words(text):
    from konlpy.tag import Okt
    
    # 한국어 형태소 분석
    okt = Okt()
    malist = okt.pos(text)
    
    # 키워드를 담을 리스트
    keywords = []
    
    # 명사 추출
    for word, tag in malist:
        if tag in ['Noun']:
            keywords.append(word)
    
    # 길이가 1인 단어 제거('은,는,이' 등 조사나 대명사 제거)
    keywords = [word for word in keywords if len(word) > 1]
    
    
    # 불용어 제거(사용자 임의)
    #stopwords = []
    # keywords = [word for word in keywords if word not in stopwords]
    
    # 중복된 단어 제거
    keywords = set(keywords)
    
    return keywords


# In[14]:


#키워드 추출 함수 적용
merged_key = df['책소개'].apply(extract_words)


# In[16]:


#새로운 데이터 프레임 생성 
df_keywords = pd.concat([df, pd.DataFrame({'책소개 키워드':merged_key})], axis=1)


# In[17]:


df_keywords.head()


# In[19]:


#비교하려고만든 셀 
print(df_keywords['책소개'][0])
print(df_keywords['책소개 키워드'][0])


# import re
# 
# def remove_parentheses(text):
#     return re.sub(r'\([^)]*\)', '', text).strip()
# 
# nov_df['상품명'] = nov_df['상품명'].apply(remove_parentheses)
# 
# print(df.head())
# 

# In[ ]:




