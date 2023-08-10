↓ 원본 

https://www.notion.so/deepdaiv/5e9a50cbaf7c4009b4ccea3b81428627?pvs=4



# 교보문고 베스트셀러 추천 시스템

---

[GitHub - sigorzav-jong/Study_week-2](https://github.com/sigorzav-jong/Study_week-2.git)

---

# 1. 프로젝트 개요

주제 : 교보문고 베스트셀러 도서 추천시스템

기간 : 2023.08.03~2023.08.10

## 1️⃣ 주제 선정 동기

[지난해 국민 독서량 '뚝'…2년 전보다 성인 3권·학생 6.6권↓ | 연합뉴스](https://www.yna.co.kr/view/AKR20220114069200005)

 영상 콘텐츠 중심의 미디어 소비 문화가 발전하면서 사람들의 독서량이 크게 감소하고 문해력이 저하되고 있다는 문제점이 지속적으로 제기되고 있다. 이는 정보를 정제하여 보기 쉽게 제시해주는 영상물과 달리 스스로 이해하고 정보를 재구성해나가며 정보를 소화해야하는 책의 매체적 특성에 의한 것으로 보인다.

 이에 따라 책에 대한 사람들의 접근성을 독서를 권장하는 방안으로써 개인의 취향에 맞는 도서 추천시스템을 구상해보았다. 특히 읽을 수 있는 책이 너무 많고 다양해지면서 독서를 하고 싶으나 당장 읽고 싶은 책은 없어 어떤 책을 읽으면 좋을지 고민하는 경우, 혹은 독서의 필요성을 느끼지만 어려운 책들에 대한 진입 장벽을 느껴 한 권을 시작하는 것도 어려워하는 경우 등 책을 선정하는데 있어 겪는 어려움으로 인해 독서 자체를 포기하는 경우가 존재한다. 따라서 개인 취향 및 관심사에 맞는 도서 추천은 수많은 책 중 개인에 맞는 도서들로 선택지 줄이면서 독서에 대한 거부감을 최소화할 수 있을 것으로 기대된다.

## 2️⃣ 사용 데이터

- 교보문고  [소설, 인문, 자기계발, 경제/경영] 4가지 장르의 베스트셀러 1위~1000위 도서
- 총 3713권 도서의 `키워드Pick`과 `책 소개` 데이터 수집

# 2. 데이터 크롤링

[💻 도서정보 받아오기](https://velog.io/@jeo0534/도서정보-받아오기)

🔗 참고사이트 : https://jaydatum.tistory.com/186?category=1027561

💡 동적 크롤링을 진행하기 위해 ***selenium***을 활용!

---

## 1️⃣ 라이브러리 설치

```python
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import urllib.request as req
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

import pandas as pd
import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')
```

## 2️⃣ 주소 받아오기

```python
book_cate = {'소설':'01','시/에세이':'03','인문':'05','경제/경영':'13','자기계발':'15'}
# 01 : 소설 , 03 : 시/에세이 , 05 : 인문 , 13 : 경제/경영 , 15 : 자기계발
url = 'https://product.kyobobook.co.kr/category/KOR/'+book_cate['인문']+'#?page=1&type=best&per=20'

User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
chrome_options = Options()
chrome_options.add_argument(f"user-agent={User_Agent }")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

```

5개의 장르를 받아오기 위해 장르 딕셔너리를 정의해 효율적으로 url을 설정했다.

## 3️⃣ 데이터 리스트 정의

```python
book_titles = list() # 상품명
book_stories = list() # 책 소개
book_keyPicks = list() # 전체 도서 키워드Picks
keywordPick = list() # 한 도서에 있는 키워드Picks
book_page_urls = list() # 장르별 1000개의 href를 담고 있음
```

## 4️⃣ 웹페이지 크롤링 과정

### ▶︎ 제목

!https://velog.velcdn.com/images/jeo0534/post/115c8a24-fd0a-4070-b9b0-c0d3620c0f44/image.png

### ▶︎ 키워드 Pick

!https://velog.velcdn.com/images/jeo0534/post/10e8c001-b9f6-4ca6-bf96-db3c03526aa7/image.png

`'#contents > div.prod_detail_header > div > div.prod_detail_title_wrap > div > div.prod_title_box.auto_overflow_wrap > div.auto_overflow_contents > div > h1 > span'`을 받아오면 모든 키워드들을 포함한 list가 생성된다. for문을 통해 리스트의 요소를 하나씩(키워드를 하나씩) 방문하면서 keywordPick 리스트에 text로 변환해서 추가해야한다.

### ▶︎ 책 소개

!https://velog.velcdn.com/images/jeo0534/post/e4ca5a79-fd42-4479-b976-2bb8c6239f84/image.png

> ⚠️ 주의할 점 : 위의 문법을 가지고 있지 않을 수도 있기 때문에 try-except 구문을 활용한다.
> 

## 5️⃣ 크롤링 코드 (수정 전후 코드 비교)

[🔗 수정 전 코드 github](https://github.com/tjdmstj/deep.daiv/blob/main/2%EC%A3%BC%EC%B0%A8/%E1%84%80%E1%85%AD%E1%84%87%E1%85%A9%E1%84%86%E1%85%AE%E1%86%AB%E1%84%80%E1%85%A9%20%E1%84%8F%E1%85%B3%E1%84%85%E1%85%A9%E1%86%AF%E1%84%85%E1%85%B5%E1%86%BC%20%E1%84%8F%E1%85%A9%E1%84%83%E1%85%B3%20%E1%84%87%E1%85%A2%E1%84%91%E1%85%A9%E1%84%8B%E1%85%AD%E1%86%BC(%E1%84%89%E1%85%AE%E1%84%8C%E1%85%A5%E1%86%BC%20%E1%84%8C%E1%85%A5%E1%86%AB).ipynb)

[🔗 수정 후 코드](https://github.com/tjdmstj/deep.daiv/blob/main/2%EC%A3%BC%EC%B0%A8/%E1%84%80%E1%85%AD%E1%84%87%E1%85%A9%E1%84%86%E1%85%AE%E1%86%AB%E1%84%80%E1%85%A9%20%E1%84%8F%E1%85%B3%E1%84%85%E1%85%A9%E1%86%AF%E1%84%85%E1%85%B5%E1%86%BC%20%E1%84%8F%E1%85%A9%E1%84%83%E1%85%B3%20%E1%84%87%E1%85%A2%E1%84%91%E1%85%A9%E1%84%8B%E1%85%AD%E1%86%BC.ipynb) [github](https://github.com/tjdmstj/deep.daiv/blob/main/2%EC%A3%BC%EC%B0%A8/%E1%84%80%E1%85%AD%E1%84%87%E1%85%A9%E1%84%86%E1%85%AE%E1%86%AB%E1%84%80%E1%85%A9%20%E1%84%8F%E1%85%B3%E1%84%85%E1%85%A9%E1%86%AF%E1%84%85%E1%85%B5%E1%86%BC%20%E1%84%8F%E1%85%A9%E1%84%83%E1%85%B3%20%E1%84%87%E1%85%A2%E1%84%91%E1%85%A9%E1%84%8B%E1%85%AD%E1%86%BC(%E1%84%89%E1%85%AE%E1%84%8C%E1%85%A5%E1%86%BC%20%E1%84%8C%E1%85%A5%E1%86%AB).ipynb)

어떤 점이 달라졌을까?

```python
# 수정 전
for page in range(1,51):
    time.sleep(3)
    for book in range(1,21):
        xpath = f'/html/body/div[3]/main/section[2]/div/section/div[3]/div[4]/div[3]/ol/li[{book}]/div[2]/div[2]/a'
        book_url = driver.find_element(By.XPATH,xpath)
        book_url.send_keys(Keys.ENTER)
        time.sleep(3)
        title = driver.find_element(By.CSS_SELECTOR,'#contents > div.prod_detail_header > div > div.prod_detail_title_wrap > div > div.prod_title_box.auto_overflow_wrap > div.auto_overflow_contents > div > h1 > span')
        book_titles.append(title.text)
        keywordPick = list()
        try:
            # 키워드 Pick 수집
            keywordPicks = driver.find_elements(By.CSS_SELECTOR,'div.tab_list_wrap > ul >li> a > span.tab_text')
            for keyword in keywordPicks:
                keywordPick.append(keyword.text)
            book_keyPicks.append(keywordPick)
        except:
            pass

        try:
            # 책 소개 수집
            story = driver.find_element(By.CSS_SELECTOR,'div.intro_bottom')
            book_stories.append(story.text)
        except:
            pass
        driver.back()
    next_page = driver.find_element(By.CSS_SELECTOR,'#bestBottomPagi > button.btn_page.next')
    next_page.click()
```

▶︎ 수정 전에는 베스트셀러 페이지에 존재하는 책들을 1위부터 1000위까지 들어갔다 나왔다 하는 방법을 사용하여 정보를 수집하였다.

▶︎ driver.back()을 사용하면 이전 페이지로 돌아가는데, 이 경우 이전 페이지가 아닌 다른 페이지로 이동하는 문제점이 발생했다. →  크롤링 방법을 수정한다.

```python
# 수정 후
for i in range(1,51):
    page_links = driver.find_elements(By.CSS_SELECTOR,'#homeTabBest > div.switch_prod_wrap.view_type_list > ol > li > div.prod_area.horizontal > div.prod_info_box > a')
    for page_link in page_links:
        link = page_link.get_attribute('href')
        book_page_urls.append(link)
    if i== 50:
       break
    next_page = driver.find_element(By.CSS_SELECTOR,'#bestBottomPagi > button.btn_page.next')
    next_page.send_keys(Keys.ENTER)
    time.sleep(3)
#--------------------------------------------------------#
driver = webdriver.Chrome(options=chrome_options)
for url in book_page_urls:
    try:
        driver.get(url)
        time.sleep(3)
        title = driver.find_element(By.CSS_SELECTOR,'#contents > div.prod_detail_header > div > div.prod_detail_title_wrap > div > div.prod_title_box.auto_overflow_wrap > div.auto_overflow_contents > div > h1 > span')
        book_titles.append(title.text)
    except:
        book_titles.append('나중에 채우기!')

    try:
        # 키워드 Pick 수집
        keywordPicks = driver.find_elements(By.CSS_SELECTOR,'div.tab_list_wrap > ul >li> a > span.tab_text')
        keywordPick = list()
        for keyword in keywordPicks:
            keywordPick.append(keyword.text)
        book_keyPicks.append(keywordPick)
    except:
        book_keyPicks.append([])

    try:
         # 책 소개 수집
        story = driver.find_element(By.CSS_SELECTOR,'div.intro_bottom')
        book_stories.append(story.text)
    except:
        book_stories.append('')

driver.quit()
```

▶︎ 먼저 1위부터 1000위까지 모든 도서들의 href정보를 가져와 list로 저장한다. 이후 반복문을 통해 list에 존재한 링크를 driver.get(url)을 통해 들어가 정보를 수집한다.

👉🏻 **get_attribute('href')**을 이용하여 href 속성을 추출할 수 있다.

---

🚨 **ERROR Check**

`NoSuchElementException`  : 페이지를 렌더링 하기 전에 특정 요소를 찾으려 했기 때문에 발생

 = 아직 웹 페이지가 준비가 되지 않았는데 정보를 긁어오려 했기 때문에 발생하는 에러

👉🏻 time.sleep(5)과 같이 페이지가 로딩이 완료 될때까지 기다려 준다면 해결할 수 있다.

( 참고 : [https://yeko90.tistory.com/entry/파이썬-기초-NoSuchElementException-ElementNotVisibleException-에러-해결-방법](https://yeko90.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EA%B8%B0%EC%B4%88-NoSuchElementException-ElementNotVisibleException-%EC%97%90%EB%9F%AC-%ED%95%B4%EA%B2%B0-%EB%B0%A9%EB%B2%95) )

---

# 3. 데이터 전처리 및 EDA

### ✅ 크롤링 데이터 원본

- 소설, 인문, 자기계발. 경제/경영 4가지 장르별로 1000권
- 칼럼명 = [’상품명’, ‘책소개’, ‘키워드’]

자기계발 장르 크롤링 데이터 Dataframe 예시

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/76853085-9779-4145-bd77-6c4480611532/Untitled.png)

> ⚠️ 교보문고 베스트셀러 목록은 날짜가 넘어가면서 갱신된다. ‘시/에세이’ 영역의 경우 크롤링 과정에서 24시가 넘어가면서 정보가 부정확해지고, 결측치가 다수 발생하는 문제가 생겼다. 이에 따라 기존엔 5가지 장르에 대한 데이터를 수집하려 했으나,  ‘시/에세이’ 장르를 제외하여 4가지 장르로 줄여 분석을 진행했다.
> 

## 1️⃣ 데이터 전처리

### ▶︎ 결측치 처리

> ‘책소개’와 ‘키워드’ 칼럼에서 결측치가 존재하는 도서를 제거한다.
> 

### ▶︎중복 데이터 처리

> 소설 장르에서 중복 데이터 2권이 발견되었다. ‘상품명’, ‘책소개’, ‘키워드’가 동일하지만, 도서가 일반 표지와 양장본 두 가지 버전으로 출판이 되면서 서로 다른 도서로 등록되어 있었다. 두 버전이 모두 베스트셀러를 기록하면서 결과적으로 Dataframe 상에선 중복 데이터로 인식되고 있었다. 책의 특성을 기반으로 한 CBF를 구현하는 것이 목적에 비추어볼때 두 버전이 결과적으로 같은 도서라고 판단해 중복되는 행을 제거하는 과정을 진행했다.
> 

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/11338f2b-54c9-45a1-ab0d-78510532ba3d/Untitled.png)

### ▶︎장르명 키워드 추가

> 도서 장르가 4가지로 구분되지만 ‘키워드’열에는 장르에 대한 정보가 포함되어 있지 않다. 도서 장르 또한 책의 특징을 드러내는 중요한 특성이므로 각 도서의 ‘키워드’ 리스트에 해당 도서가 속한 장르 이름을 추가한다. (예를 들어 소설 장르에 속하는 모든 도서에 대하여 ‘키워드’로 ‘소설’을 추가한다.)
> 

자기계발 장르 전처리 후 Dataframe 예시

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/01c60d32-ee84-4903-9c99-491eae2134b3/Untitled.png)

## 2️⃣ ‘책소개 키워드’ 추출

: '키워드'의 경우 교보문고에서  제공하는 데이터로, 책의 특징을 키워드로 표현한 것이다. 따라서 책의 줄거리나 작가 특성 등의 정보와 관련된 키워드를 추가적으로 확보해 기존 '키워드' 기반 추천을 보완하고자 한다.

 글 형태로 되어있는 '책소개' 텍스트에서 키워드를 추출해 추천시스템에 사용한다. 키워드를 추출하는 방법을 크게 한글 형태소 분석기 Okt를 사용하는 방법과 KR-WordRank를 사용하는 방법 2가지로 시도했으며, 2번째 방법의 키워드 추출 결과를 최종 모델링에 활용했다.

### ▶︎ 한글 형태소 분석기 Okt

: `KoNLPy` python 패키지를 통해 한국어 형태소 분석기를 import할 수 있다.

- `KoNLPy` 제공 한국어 형태소 분석기 5가지
    - Okt(Open Korea Text)
    - Komoran(코모란)
    - Hannanum(한나눔)
    - Kkma
    - Mecab (Mecab은 윈도우에서 작동이 불가능)
- 형태소 분석기 method
    
    > `.nouns` : 명사 기준 추출
    > 
    > 
    > `.phrases` : 어절 기준 추출
    > 
    > `.pos` : 품사를 함께 태깅해서 추출
    > 
    > `.morphs` : 형태소 단위로 추출
    > 
    

본 프로젝트에서는 가장 성능이 좋다고 알려진 Okt를 사용한다.

- '책소개' 텍스트에 `Okt`의 `.pos` method를 적용하여 (단어, 품사) 리스트를 추출한 후 'None'만 추출하는 함수를 정의한다.
- 정의한 함수를 사용해 명사 키워드를 추출하고, 이를 기존 Dataframe에서 '책소개 키워드' 열로 추가한다.

```python
from konlpy.tag import Okt

def extract_words(text):
    
    okt = Okt()
    words_list = okt.pos(text)
    
    # 키워드를 담을 리스트
    keywords = []
    
    # 명사 추출
    for word, tag in words_list:
        if tag == 'Noun':
            keywords.append(word)
    
    # 중복 단어 제거
    keywords = set(keywords)
    
    return keywords

extracted_key = df['책소개'].apply(extract_words)
df_new = pd.concat([df, pd.DataFrame({'책소개 키워드':extracted_key})], axis=1)
```

### ▶︎ KR-WordRank

: 한국어의 특징을 반영하여 비지도학습 기반으로 한국어의 단어를 추출하며 토크나이저를 이용하지 않으면서도 단어/키워드 추출을 수행한다.

- df['책소개']는 **‘\n’**을 포함하여 하나의 문장으로 이루어져 있기 때문에 이를 여러 개의 문장으로 나눠야 한다.

```python
for text in df['책소개']:
  text.split('\n')
  text_list.append(text.split('\n'))

text_list[:2]
```

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/0765ea10-fe08-452b-8cf9-40625e070fd4/Untitled.png)

- normalize 함수를 이용하여 **불필요한 특수 기호를 제거한다**.
    
    ex) ‘▶︎', ’!’, ‘★’ 등…
    

```python
from krwordrank.hangle import normalize
texts = [[normalize(text, english=True, number=True) for text in texts] for texts in text_list]
texts[:2]
```

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/26331833-8c96-4b1f-bbb2-4bfc123b8ea7/Untitled.png)

- texts를 df에 ‘**책소개 전처리’**라는 열(column)이름으로 추가한다.
- `KRWordRank` 패키지를 이용하여 ’책소개 전처리’ 열에서 중요한 키워드를 추출하고, 이를 기존 Dataframe에서 '책소개 키워드 수정본' 열로 추가한다.

```python
from krwordrank.word import KRWordRank
from konlpy.tag import Okt

def KeyWord(x):
  sentence = []
  wordrank_extractor = KRWordRank(
    min_count = 1, # 단어의 최소 출현 빈도수 (그래프 생성 시)
    max_length = 10, # 단어의 최대 길이
    verbose = True
    )

  beta = 0.85    # PageRank의 decaying factor beta
  max_iter = 20
  keywords, rank, graph = wordrank_extractor.extract(x, beta, max_iter)
  word_list = list()
  for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:30]:
    if r >=1:
      word_list.append(word)
	# 한 문장으로 합친다.
  sent = ' '.join(word_list)
  sentence.append(sent)

	# 형태소 추출
  okt = Okt()
  OKT = okt.pos(sent)
  keyword_list = []

  # 조사와 접미사를 제외한 나머지만을 키워드로 채택
  for word, tag in OKT:
    if (tag not in ['Josa']) and (tag not in ['Suffix']):
      keyword_list.append(word)
  return keyword_list

df['책소개 키워드 수정본'] = df['책소개 키워드'].apply(KeyWord)![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/cfdd3f1b-f626-47ca-b8fc-c4271a4b7925/Untitled.png)
```

### ✅ 최종 Dataframe

[ ✅ 크롤링 데이터 원본](https://www.notion.so/7113a0cca6604cb38963b008b7753fd5?pvs=21)

- 결측치와 중복값 제거, 키워드에 장르명 추가
- ‘책소개 키워드’, ‘책소개 전처리’, ‘책소개 키워드 수정본’ 열 추가

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/199473c0-fb62-43cc-910f-3dc4cf1e06d9/Untitled.png)

## 3️⃣ 워드 클라우드 시각화

: ‘키워드’와 ‘책소개 키워드’에 등장하는 키워드에 대하여 워드 클라우드를 그려본다. 키워드에 등장하는 모든 단어에 대하여 각 단어의 등장 횟수(빈도수, count)를 계산한 후, 빈도수 순위를 확인하고 빈도수 기반 워드 클라우드 시각화를 진행했다.

### ▶︎ ‘키워드’ 워드 클라우드

- ‘키워드’ 빈도수 상위 30개 단어
    
    > 소설 : 1039
    경제경영 : 937
    자기계발 : 929
    인문 : 925
    세계고전문학 : 154
    주식투자 : 153
    투자자 : 151
    내면 : 147
    사랑 : 108
    재테크 : 82
    자기관리 : 81
    창업 : 75
    영화원작소설 : 69
    주식 시장 : 68
    한국소설 : 67
    인생 : 66
    인간관계 : 65
    수익 : 61
    판타지소설 : 61
    성장소설 : 60
    성공 : 55
    미스터리 : 51
    부자 : 50
    감정 : 48
    일본소설 : 48
    영미소설 : 48
    개인 투자자 : 46
    인공지능 : 46
    거래량 : 45
    습관 : 45
    > 
    

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e5a835ba-2b94-42e8-80df-469af494536d/Untitled.png)

### ▶︎ ‘책소개 키워드 수정본’ 워드 클라우드

- ‘키워드’ 빈도수 상위 30개 단어
    
    > 것 : 1311
    하는 : 1066
    있다 : 997
    있는 : 757
    저자 : 663
    한다 : 644
    사람 : 617
    책 : 611
    삶 : 596
    우리 : 578
    그 : 570
    대한 : 525
    통해 : 522
    세계 : 516
    자신 : 490
    가장 : 478
    위 : 465
    어떻게 : 437
    간 : 402
    위해 : 402
    된 : 401
    작가 : 399
    이야기 : 388
    방법 : 382
    말 : 377
    독자 : 369
    출 : 359
    인생 : 341
    소설 : 335
    투자 : 331
    > 

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/a70b3061-405e-4661-9b84-6a52c45e76e2/Untitled.png)

‘책소개’ 텍스트에서 추출한 키워드의 경우 ‘것’, ‘하는’, ‘있다’, ‘저자’와 같이 대부분의 책소개 텍스트에 들어가 있는 일반적인 단어가 많이 추출되었음을 확인할 수 있다. 이에 따라 단순히 단어의 등장 여부나 횟수가 아닌 특정 문서에서 특정 단어의 중요도 값을 기준으로 하는 TF-IDF 기반 추천 시스템이 더욱 적절할 것이라고 예상했다.

## 4️⃣ 추천 시스템 구상

: 데이터 전처리와 EDA 과정을 기반으로 추천 시스템 구현 방법을 구상한다.

▶︎ 구현한 추천 시스템 종류

1) 인코딩 기반 추천 시스템

2) TF-IDF 기반 추천 시스템

3) Word2Vec 기반 추천 시스템

---

# 4. 인코딩 **기반** 추천시스템

<aside>
📌 **키워드에서 각 단어의 등장 여부를 1과 0의 값으로 두고 도서를 벡터화
→ 도서 간 코사인 유사도 계산
→ 베스트셀러 추천 리스트 작성**

</aside>

## 1️⃣ 벡터화

: 벡터화 방법으로 `CountVectorizer 클래스`를 이용한 벡터화와 One-hot encoding 함수 정의를 통한 벡터화, 2가지 방법을 시도해보았다.

### ▶︎ ****CountVectorizer****

: `CountVectorizer`는 `sklearn.feature_extraction`에서 제공하는 문서 벡터화 클래스로, 주어진 문서에 각각의 단어가 몇 번 등장하는지 count하여 document-term matrix(DTM)를 만든다.

- `CountVectorizer` method
    - `.fit` : 단어 사전을 구축하는 기능, 주어진 문서 속 단어들에 대해 각 단어가 몇 번째 열에 올 것인지 index를 지정한다.
    - `.transform` : 구축한 단어 사전을 기반으로 주어진 문서를 벡터로 변환하는 기능, 단어 사전에 없는 단어가 문서에 포함된 경우 이를 무시해버린다.
    - `.fit_transform` : 문서 list를 이용해 단어 사전을 구축하고, 각 문서를 벡터화하여 document-term matrix로 변환한다.
- CountVectorizer는 원래 string에서 각 단어의 빈도수를 세는 기능을 수행하지만, 현재 Dataframe의 경우 키워드 리스트에 각 단어가 중복되어 존재하지 않기 때문에 CountVectorizer를 적용하면 키워드에 존재하는 경우엔 1을, 그렇지 않은 경우엔 0의 값을 가지는 One-hot encoding과 같은 결과의 벡터화를 진행할 수 있다.

```python
from sklearn.feature_extraction.text import CountVectorizer

count_vectorizer_1 = CountVectorizer()
book_mat_keyword_1 = count_vectorizer_1.fit_transform(best['키워드'])

book_mat_keyword_1.toarray()
```

- 하지만 CountVectorizer를 실행하면 이미 완료된 키워드 토큰화가 다시 토큰화되는 문제가 발생했다. 이에 따라 기존 One-hot encoding을 이용한 벡터화로 다시 시도해보았다.

### ▶︎ **원-핫 인코딩**(One-hot encoding)

: 범주의 개수와 같은 크기의 벡터에 대하여 0과 1을 사용해 어떤 범주에 속하는지 표현하는 인코딩 방식이다. 문장에서 특정 단어의 출현 여부를 0과 1로 표현하여 단어 임베딩을 진행할 수 있다.

- 키워드에 존재하는 모든 단어를 정리한 단어 사전을 만들고, 각 도서에 대하여 각 단어가 존재하는지 따짐으로써 One-hot encoding을 진행했다.

```python
# 단어 사전 만들기
word=list()
for i in range(len(best2['키워드'])):
    keyword_list = best2.loc[i, '키워드']
    word += keyword_list
word_dic = list(set(word))

# One-hot encoding 수행하는 함수 정의
def vectorize(df, col, word_dic):
    df_matrix = pd.DataFrame()

    for i in range(df.shape[0]):
        tmp = []
        for voca in word_dic:
            tmp.append(df.loc[i, col].count(voca))
        df_matrix = pd.concat([df_matrix,  pd.DataFrame(tmp).T])
        #df_matrix.append(tmp)
    return df_matrix

# One-hot encoding 수행
df_matrix = vectorize(best2, '키워드', word_dic)
```

- One-hot encoding은 범주가 너무 넓거나 복잡하면 매우 sparse한 형태의 고차원 벡터로 표현되기 때문에 메모리 낭비 및 계산 복잡도가 커지는 단점이 있다. 실제 분석 과정에서 One-hot encoding을 이용한 벡터화 과정이 가장 오랜 시간이 소요되었다.

## 2️⃣ 유사도 측정

: `코사인 유사도`를 이용하여 각 DTM의 유사도 행렬을 계산한다.

| 사용한 칼럼 | DTM | 유사도 matrix |
| --- | --- | --- |
| 책소개 키워드 수정본 | book_mat_keyword | cosine_sim |
| 키워드 | book_mat_keyword_1 | cosine_sim_1 |
| 상품명 | book_mat_keyword_2 | cosine_sim_2 |

```python
from sklearn.metrics.pairwise import cosine_similarity

cosine_sim = cosine_similarity(book_mat_keyword.toarray())
cosine_sim_1 = cosine_similarity(book_mat_keyword_1.toarray())
cosine_sim_2 = cosine_similarity(book_mat_keyword_2.toarray())
```

## 3️⃣ 유사도 기반 도서 추천

: 세 가지의 코사인 유사도를 활용한 유사 도서 추천 시스템을 구현한다.

- 주어진 title에 대하여 코사인 유사도가 높은 순부터 내림차순 정렬한 후 상위 n개를 추출하는 함수를 정의한다.
- 세 가지의 코사인 유사도에 가중치를 설정하고, 가중합 유사도를 최종 유사도 판단의 기준 값으로 사용했다. ([▶︎ 가중치 부여 방법](https://www.notion.so/cef095f98b884ba58256222b16a683cd?pvs=21) 구체적인 설명)

```python
# 유사도 가중치 적용
sim = 0.4*cosine_sim + 0.5*cosine_sim_1 + 0.1*cosine_sim_2

# 추천 함수 정의
def find_sim_book(best, sim, query_index, top_k):
    # query 인덱스에 대한 유사도 값을 가져옴
    query_similarity = sim[query_index]

    # 코사인 유사도 값을 기준으로 유사도가 높은 순서대로 정렬된 인덱스를 얻음
    sorted_indices = np.argsort(query_similarity)[::-1]

    print(f'검색한 콘텐츠 : {best["상품명"].iloc[query_index]}')
    print('\n출력한 콘텐츠')
    print(sorted_indices)
    print(best['상품명'].iloc[sorted_indices[1:top_k +1]])

# 궁금한 도서의 index, 유사 도서 개수 입력
query_index = 0
top_k = 10

# 추천 함수 실행
find_sim_book(best, sim, query_index, top_k)
```

## 4️⃣ 추천 결과

****CountVectorizer를 이용한 경우 추천 결과****

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f810c99d-29c9-4b4e-be60-653810c8f900/Untitled.png)

**One-hot encoding을 이용한 경우 추천 결과**

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/3370d3b5-1994-4b89-9215-ccb48c953bb2/Untitled.png)

---

# 5. TF-IDF **기반** 추천시스템

<aside>
📌 **각 키워드의 TF-IDF 값으로 도서를 벡터화
→ 도서 간 코사인 유사도 계산
→ 베스트셀러 추천 리스트 작성**

</aside>

## ▶︎ TF-IDF(Term Frequency-Inverse Document Frequency)

🔗 출처 : [TF-IDF (Term Frequency-Inverse Document Frequency)](https://wikidocs.net/31698) 

!https://velog.velcdn.com/images/jeo0534/post/35740498-fb31-47bc-a928-470cad6d64e4/image.png

- `TF(w)` : 특정 단어 w가 특정 문서 d에 나온 빈도
- `DF(w)` : 특정 단어 w가 나타난 문서의 수👉🏻 여러문장에 쓰이는 범용적인 단어
- `IDF(w)` : 전체 문서 수 N을 해당 단어의 DF로 나눈 뒤 로그를 취한 값👉🏻 모든 문서에 등장하는 단어(DF)의 중요도를 낮춘다. (1을 더하는 이유는 분모가 0이 되는 것을 방지하기 위해)
- `N` : 전체 문서 수
- `Bag of Word`의 문제점을 보완
    
    > **Bag of Word Embedding**
    > 
    > - 단어의 순서를 고려하지 않고 빈도수로 텍스트를 임베딩하는 방법
    > - 많이 쓰인 단어가 주제와 관련이 있다고 가정한다.
    > - 🚨 문제점 : 영어 text일 경우 'a'와 같은 단어 때문에 예측하기 어렵다는 문제가 있다.
    > - BoW 예시
    >     
    >     !https://velog.velcdn.com/images/jeo0534/post/8d35cb3a-3018-43d3-a8b1-03ccd0568b1e/image.png
    >     
    > 
    > 🔗 출처 : [Bag of Word (BoW)](https://wikidocs.net/22650) 
    > 
    

## 1️⃣ 벡터화

: sklearn에 내장되어 있는 `TfidfVectorizer`을 이용한다.

```python
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['책소개 키워드 수정본'].map(' '.join))
tfidf_array = tfidf_matrix.toarray()
tfidf_df = pd.DataFrame(tfidf_array, columns=tfidf_vectorizer.get_feature_names_out())
tfidf_df
```

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/694e3605-c88d-4e61-ad41-58517838537c/Untitled.png)

- **fit_transform**은 학습과 변환을 동시에 진행할 수 있다. 
이를 이용하기 위해서는 input값으로 string type의 한 문장이 들어가야한다. 
현재 df['책소개 키워드 수정본']는 리스트 안 여러개의 단어들로 구성되어있기 때문에 `.map(' '.join))`을 이용하여 한 문장으로 변환해준다.
- ‘상품명’, ‘키워드’ 열에 대해서도 같은 방식으로 TF-IDF 행렬을 구해준다.

## 2️⃣ 유사도 측정

: `코사인 유사도`를 이용하여 각 DTM의 유사도 행렬을 계산한다.

```python
from sklearn.metrics.pairwise import cosine_similarity

cosine_sim = cosine_similarity(tfidf_array) # 책소개 키워드 기반 유사도
cosine_sim_1 = cosine_similarity(tfidf_array_1) # 키워드 기반 유사도
cosine_sim_2 = cosine_similarity(tfidf_array_2) # 상품명 기반 유사도
```

▶︎ 유사도 예시 (’책소개 키워드 수정본’ 기반 유사도)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/534fc1bd-157c-4c0b-a321-5d7b6f7d6d0f/Untitled.png)

## 3️⃣ 유사도 기반 도서 추천

: 세 가지의 코사인 유사도를 활용한 유사 도서 추천 시스템을 구현한다. 세 가지의 유사도를 동시에 사용하는 하나의 추천 시스템을 구축하기 위해 각각의 유사도에 대해 다른 가중치를 부여해 하나의 유사도로 도출했다.

▶︎ 가중치 부여 방법

- 세 가중치의 합이 1이 되도록 설정
- `상품명`의 경우 길이가 너무 짧고 책의 내용과는 상관없는 내용일 수 도 있기에 책의 특성을 많이 담고 있지 않다고 생각 → 가장 적은 가중치를 부여
- `키워드Pick`의 경우 교보문고에서 직접 부여한 키워드기 때문에 다른 변수보다도 책의 특성을 많이 반영하고 있다 생각 → 가장 많은 가중치를 부여
    
    👉🏻 **책소개 : 키워드Pick : 상품명 =   4 : 5 : 1 의 비율로 가중치를 부여!**
    

```python
# cosine_sim -> 책소개
# cosine_sim_1 -> 키워드Pick
# cosine_sim_2 -> 상품명

sim = 0.4*cosine_sim + 0.5*cosine_sim_1 + 0.1*cosine_sim_2
sim
```

## 4️⃣ 추천 결과

```python
query_index = -1 # 상품명 : 성격의 탄생
top_k = 10 # 상위 유사 도서 개수

query_similarity = sim[query_index]
sorted_indices = np.argsort(query_similarity)[::-1]

print('검색한 콘텐츠')
print(df['상품명'].iloc[query_index])
print()
print('출력한 콘텐츠')
df['상품명'].iloc[sorted_indices[1:top_k +1]]
```

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f5cf3333-6a73-424a-b399-d964fdd2e178/Untitled.png)

---

# 6.  **Word2Vec 기반** 추천시스템

<aside>
📌 **Word2Vec 모델로 주어진 단어와 가장 유사한 키워드 리스트 속 단어 추출
→ 유사 단어들을 키워드로 가장 많이 포함하고 있는 도서 추출
→ 베스트셀러 추천 리스트 작성**

</aside>

## ▶︎ '키워드'에 따른 책 추천 Word2Vec 알고리즘

: Word2Vec은 원시 텍스트로부터 단어 임베딩을 학습하는 데 특히 계산적으로 효율적인 예측 모델이다. 두 가지 방식으로 제공되는데, 연속적 CBOW 모델과 Skip-Gram 모델이 있다.

- **CBOW 모델: 주변 단어들을 이용해 대상 단어를 예측**
: CBOW는 주변 문맥 단어들(예: '고양이가 앉아 있는')로부터 대상 단어(예: '매트')를 예측한다. 통계적으로 CBOW는 분포를 매끄럽게 처리하는 효과가 있으며(전체 문맥을 하나의 관찰 결과로 취급), 작은 데이터 셋에 유용하다.

- **Skip-Gram 모델: 대상 단어를 이용해 주변 단어들을 예측
: S**kip-Gram은 대상 단어로부터 주변 문맥 단어를 예측한다(CBOW의 역). 통계적으로 Skip-Gram은 각 문맥-대상 쌍을 새로운 관찰로 취급하며, 이는 대규모 데이터 셋에서 더 나은 결과를 보인다.

🔗 출처 : [Skip-gram and CBOW](https://towardsdatascience.com/nlp-101-word2vec-skip-gram-and-cbow-93512ee24314) 

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6c291490-28c7-4bd3-8fe0-67054cebe982/Untitled.png)

 본 프로젝트에서는 Skip-Gram 모델로 구현하였으며, [gensim](https://radimrehurek.com/gensim/)이라는 라이브러리를 이용했다. `gensim`은 자연어를 벡터로 변환하는데 필요한 대부분의 편의 기능을 제공해주는 대표적인 라이브러리이다. 

## 1️⃣ 문자열 리스트화

: Word2Vec로 학습하기 위해선 문자열을 리스트로 바꿔야한다.  이에 따라 기존 Dataframe의 ‘키워드’ 열에 대하여 각 행별로 리스트화를 진행하였다.

```python
import ast

text= []
for keywordin df['키워드']:
    keyword_list= ast.literal_eval(keyword)# 문자열을 리스트로 변환
text.append(keyword_list)
```

## 2️⃣ Word2Vec 모델 학습

: 단어를 입력하면 해당 단어 가장 유사한 ‘키워드’ 속 단어를 순서대로 출력해주는 모델을 생성한다.

⚠️ 실험 키워드로 ‘경제’를 입력하였다.

```python
from gensim.models.word2vec import Word2Vec

model = Word2Vec(text, sg = 1, window = 2, min_count = 3)
model.init_sims(replace = True)
model.wv.most_similar("경제", topn = 10) #키워드 입력
```

- `sg`: 학습 알고리즘을 선택하는 인자이다. `sg=0`일 경우, CBOW(Co ntinuous Bag of Words) 알고리즘을 사용하고, `sg=1`일 경우, Skip-gram 알고리즘을 사용한다. 이 실습에서는 `sg=1`로 설정되어 있어 Skip-gram 알고리즘이 사용된다.
- `window`: 목표 단어와 주변 단어 사이의 최대 거리를 나타내는 인자이다. `window=2`의 경우, 목표 단어 앞뒤로 두 개의 단어를 고려하여 학습한다.
- `min_count`: 모델 학습에 포함시킬 단어의 최소 빈도수를 설정하는 인자이다. 이 예제에서는 단어가 최소 3번 이상 등장해야 학습에 포함된다.

- **`model.init_sims(replace = True)`: 모델의 단어 벡터를 정규화하여 메모리 효율성을 높인다. 이 과정은 모델 학습이 완료된 후에 실행되며, 모델의 크기를 줄이는 데 도움이 된다.**

🔗 출처 : [Word2vec 예제](https://medium.com/@zafaralibagh6/a-simple-word2vec-tutorial-61e64e38a6a1) 

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/17342e6e-f04b-462d-b8b1-349df4193bb4/Untitled.png)

### 출력 결과

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/75e9769a-3c93-4c4c-a867-6567ffada90d/Untitled.png)

‘경제’ 키워드 입력 시 출력해주는 유사 단어 상위 10개이다. ‘경제’와 비슷한 ‘부자’, ‘경제경영’ 등의 단어도 있었고, ‘사랑’이나 ‘미스터리’ 같이 큰 관계가 없는 단어도 출력되었다.

## 3️⃣ **상위 연관키워드를 포함하는 상위 10개 책 출력**

: 위에서 학습한 Word2Vec 모델을 확장하여, 해당 모델이 제시하는 상위 연관 키워드들을 가장 많이 포함하는 상위 10개의 책을 추천하는 추천 시스템을 구현한다.

```python
# 연관 단어 목록  
similar_words = [word[0] for word in model.wv.most_similar("경제", topn=10)]

# 각 책에 대해 연관 단어가 몇 개 포함되어 있는지 계산
df['count'] = df['키워드'].apply(lambda x: len(set(ast.literal_eval(x)).intersection(similar_words)))

# 상위 10개의 책 출력
top_products = df.nlargest(10, 'count')

# 책제목 출력하기
for idx, row in top_products.iterrows():
    print(row['상품명'])
```

### 출력 결과

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/eab92d0f-3240-44c3-a27b-79def6bee957/Untitled.png)

앞서 확인한 ‘경제’ 키워드 입력 시 출력해주는 유사 단어들을 가장 많이 포함하는 상위 10개의 책을 추천하였다. 

(피드백)**‘책소개’ 관련해서 이 부분에서는 Word2Vec 이 적절하지 않을 수 있음. 노이즈가 너무 많음. (Ex. 베스트셀러 선정 등등)**

---

# 7.  **프로젝트 결과**

### ▶︎데이터

- 교보문고  [소설, 인문, 자기계발, 경제/경영] 4가지 장르의 베스트셀러 3713권 도서
- 교보문고 웹페이지 크롤링 : `키워드Pick`과 `책 소개` 데이터 수집
- 키워드 추출을 통해 `책 소개` 에서 ‘책소개 키워드’ 추출
- [✅ 최종 Dataframe](https://www.notion.so/Dataframe-390663378dd74e03833a9553716847f6?pvs=21)

### ▶︎ 추천 시스템 모델링

**인코딩 기반 추천시스템**

<aside>
📌 **키워드에서 각 단어의 등장 여부를 1과 0의 값으로 두고 도서를 벡터화
→ 도서 간 코사인 유사도 계산
→ 베스트셀러 추천 리스트 작성**

</aside>

**TF-IDF 기반 추천시스템**

<aside>
📌 **각 키워드의 TF-IDF 값으로 도서를 벡터화
→ 도서 간 코사인 유사도 계산
→ 베스트셀러 추천 리스트 작성**

</aside>

**Word2Vec 기반 추천시스템**

<aside>
📌 **Word2Vec 모델로 주어진 단어와 가장 유사한 키워드 리스트 속 단어 추출
→ 유사 단어들을 키워드로 가장 많이 포함하고 있는 도서 추출
→ 베스트셀러 추천 리스트 작성**

</aside>

## ✅ 추천 결과 비교

(예 1) 도서명 ‘부자의 그릇’

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e4e29d5a-6b97-4bde-b71b-000cf3d9bcf8/Untitled.png)

- ‘부자의 그릇’과 유사한 상위 10권의 도서 추천 리스트

                          인코딩 기반 추천시스템          |          TF-IDF 기반 추천시스템

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/8ad44336-8841-4d5c-bca6-c04a85f45427/Untitled.png)

- ‘부자되는법’ 키워드 관련 상위 키워드 10개, 10권의 도서 추천 리스트

       Word2Vec 기반 추천시스템

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/88c1684b-592f-4da9-812a-105c222c4f9a/Untitled.png)

(예 2) 도서명 ‘위기의 역사’

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/97504960-053b-4f29-bf3d-b6a55e99c1cc/Untitled.png)

- ‘위기의 역사’와 유사한 상위 10권의 도서 추천 리스트

                          인코딩 기반 추천시스템          |          TF-IDF 기반 추천시스템

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/02eed931-d926-4fa2-9908-ed4096f20628/Untitled.png)

- ‘금리’ 키워드 관련 상위 키워드 10개, 10권의 도서 추천 리스트

       Word2Vec 기반 추천시스템

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/94a55d48-a5c3-442d-8680-0b46e45190a5/Untitled.png)

(예 3) 도서명 ‘어린 왕자(Le Petit Prince)(교보문고 특별판)’

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f8faf17d-79f8-4587-8d47-9962e8e703db/Untitled.png)

- ‘어린 왕자(Le Petit Prince)(교보문고 특별판)’과 유사한 상위 10권의 도서 추천 리스트

             인코딩 기반 추천시스템        |        TF-IDF 기반 추천시스템

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/82967e2e-8626-4da4-859c-3ae516e769a1/Untitled.png)

(예 4) 도서명 ‘죽고 싶은 사람은 없다’

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e36c1ea0-62c5-493f-88fe-2249ad51c450/Untitled.png)

- ‘죽고 싶은 사람은 없다’와 유사한 상위 10권의 도서 추천 리스트

             인코딩 기반 추천시스템        |        TF-IDF 기반 추천시스템

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/0c6081ae-3a26-474b-b9ee-4638a2b33c14/Untitled.png)

## 🚨 한계 및 개선 방안

1. **데이터 칼럼의 부족**

문제점 : 고유 번호, 출판사, 작가 등 도서를 구별할 수 있는 정보가 충분하지 않아 동일한 제목의 도서들이 존재하는 경우가 있었다.

👉🏻 개선 방안 : 도서의 고유 번호, 출판사, 작가 등과 같이 책을 구별할 수 있는 정보를 원본 데이터에 추가한다. 나아가 도서의 판매 페이지나 링크도 포함한다면, 추천 리스트를 제시할 때 함께 보여줌으로써 해당 도서가 무엇인지 바로 확인할 수 있도록 구현할 수 있을 것이다.

1. **도서 종류의 한계**

문제점 : 현재는 4가지 분야에 대해서, 베스트셀러 도서에 대해서만 추천 시스템을 적용할 수 있는 상태이다.

👉🏻 개선 방안 : 더 많은 분야와 도서에 대해 도서 DB를 확장한다면 더 활용도 높은 도서 추천 서비스를 제공할 수 있을 것으로 기대된다.

1. **‘책소개’ 키워드 추출**

문제점 : ‘책소개’ 텍스트에서 키워드를 추출하기 위해 2가지 방법을 사용했다. 하지만 첫 번째 방법의 경우 토큰화가 부정확해지는 문제가, 두 번째 방법의 경우 어떤 책이든 적용될 수 있는 너무 일반적인 단어들이 주요 키워드로 나온다는 문제가 존재했다.

👉🏻 개선 방안 : 단순히 단어를 추출하는 것이 아닌, 해당 문서에서 중요한 키워드만 추출하는 방식으로 개선한다면 ‘책소개 키워드’가 추천 시스템의 정확성을 더 높일 수 있을 것이라 생각된다.

1. **유사도 가중치 결정의 어려움**

문제점 : 인코딩 기반과 TF-IDF 기반 추천시스템의 경우 3가지 유사도 값의 가중합을 최종 유사도 판단 기준으로 활용했다. 이때 가장 적절한 가중치를 찾기 위한 과정을 엄밀하게 진행하지 못했다는 문제점이 있다.

👉🏻 개선 방안 : Cross Validation이나 Grid Search와 같이 최적의 가중치 비율을 정하기 위한 과정을 진행한다면 개선할 수 있을 것이라 생각했다. 추천시스템에서는 파라미터 튜닝을 어떻게 진행할 수 있는지에 대한 추가적인 학습이 필요하다.

1. **Word2Vec 알고리즘에 대한 이해**

문제점 : Word2Vec 알고리즘은 단어 주변의 문맥 정보를 중요하게 생각하기 때문에 순서가 굉장히 중요하다. 하지만 알고리즘을 제대로 공부하지 않고 구현했기 때문에 키워드가 무작위로 배열된 피처를 가지고 학습을 진행하였다. 그렇기 때문에 다른 키워드를 입력했을 땐 엉뚱한 결과 값이 나올 때도 많았다. 따라서 위 실습에서 입력 키워드와 비슷한 도서들이 추천된 사유는 (무작위로 배치된)주변 맥락에 관련 정보가 많아서 그저 운이 좋았던 **잘못된** 결과였던 것이다. 

👉🏻 개선 방안 : 형태소 분석을 한 다음 불용어를 제거 하였을 때 단어들의 순서는 그대로 유지해야한다. 앞 뒤 단어의 맥락 정보가 굉장히 중요하기 때문에 순서를 바꾸면 모델이 제대로 학습을 하지 못한다. 추후 알고리즘 구현에 있어선 꼭 확인해야 할 부분이다. 따라서 이번 실습에선 해당 모델을 구현해 본 것과 해당 모델이 제대로 학습되기 위해선 어떤 조건을 만족해야 하는지 배울 수 있었던 것에 의의를 둔다.
