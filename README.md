# Quasar Zone Price Finder

Quasar Zone Price Finder is a program that uses Selenium to find the best prices for user-inserted keywords on the [Quasar Zone community's](https://quasarzone.com/) special deals page.

<!-- vim-markdown-toc GFM -->

- [Features](#Features)
- [Installation](#Installation)
- [Usage](#Usage)

<!-- vim-markdown-toc -->

## Features

- Easy setup using Docker
- Run Selenium to avoid anti-scraping measures
- Find the best price in [QZ's](https://quasarzone.com/) Special Deals page
- print TOP3 links or all results

## Installation

```sh
docker build -t QZP .
```

## Usage

```sh
docker run -it --name deal QZP
```

1. After running the program, input the desired keyword.
2. The program will search for the keyword and provide output options  
   1: Display the top 3 lowest prices and links  
   2: Display all available deals and links

![run](https://github.com/chungJS/QZPriceFinder/raw/main/img/run.png)

---

# DockerFile

```docker
FROM ubuntu

LABEL maintainer = "Pan"

#기본 설치
RUN apt update && apt upgrade -y
#파이썬 환경 구축
RUN apt install python3 python3-pip -y
RUN pip install selenium
RUN pip install beautifulsoup4
#필요한 파일 다운받기위한 wget, 파일 압축해제를 위한 unzip
RUN apt install curl wget unzip -y

#dir 폴더 생성
WORKDIR /dir

#만든 파일 불러오기
ADD https://raw.githubusercontent.com/dpan0883/best_marketprice/main/main.py .

#크롬 설치
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install ./google-chrome-stable_current_amd64.deb -y
#크롬 드라이버(셀레니움 설치)
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /dir

CMD [ "python3", "/dir/main.py" ]
```

우분투 환경에서 실행하고 코드를 실행하기 위한 python과 라이브러리들을 불러오기 위한 pip를 설치하고 사용할 라이브러리인 selenium과 beautifulsoup를 받아온 후 Dockerfile에서 사용할 curl, wget, unzip을 받아준다.

내가 설치한 파일들을 보기 편하게 dir폴더를 만들고 지정한 후 깃허브에 올려져 있는 파이썬 파일과 리눅스 버전의 크롬 드라이버를 가져오고 크롬을 리눅스 버전으로 설치해준다.

마지막으로 CMD 명령어를 이용해 도커를 실행할 때 바로 프로그램을 실행한다.

---

# Python Code

```python
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re

def cr_hotdeal(keyword) :
    #가장 먼저 이 함수로 필요한 정보를 내보낼 리스트를 먼저 선언 한후
    results = []

    #입력받은 키워드를 붙여서 크롤링 할 주소를 만들어 줍니다.
    base_url = "https://quasarzone.com/bbs/qb_saleinfo?_method=post&kind=subject&keyword="
    final_url = f"{base_url}{keyword}"
    #셀레니움을 이용하여 크롤링합니다.
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches",["enable-logging"])

    #백그라운드에서 조용히 돌리기 위해서 넣는 옵션입니다.
    options.add_argument("--headless")
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')

    browser = webdriver.Chrome(options=options)
    browser.get(final_url)

    #BeautifulSoup를 이용하여 정보들을 찾아서 우리가 필요한 정보인 링크와 가격을 가져오고 후에 내보낼 리스트에 추가해줍니다.
    soup = BeautifulSoup(browser.page_source,'html.parser')
    deal_list = soup.find('div', class_="market-type-list market-info-type-list relative")
    deals = deal_list.find_all('div', class_="market-info-list-cont")
    for deal in deals :
        link = deal.select_one("a")['href']
        price0 = deal.find("span",class_="text-orange")
        if price0.string.find("KRW") != -1 :
            price = int(re.sub(r'[^0-9]', '', price0.string))
            if price > 100 :
                deal_data = {
                    'link' : f"https://quasarzone.com{link}".replace(","," "),
                    'price' : price
                }
                results.append(deal_data)
    #결과를 낮은 가격순으로 보고 싶기 때문에 딕셔너리의 키들로 분류합니다.
    result = sorted(results, key = lambda x : (x['price']))
    return result

print("나온 링크를 클릭해서 최근에 나온 가장 싼 특가를 확인하세요.")
print("100원 이하의 이벤트 상품은 제외했습니다.")
keyword = input("퀘이사존 특가 페이지에서 검색하고 싶은 아이템을 입력해주세요. : ")
result = cr_hotdeal(keyword)
while(True) :
    if len(result) < 3 :
        print("검색된 링크가 너무 적습니다.")
        break
    mode = input(f"{keyword}의 TOP3 링크만 출력하려면 숫자 1, 전체를 출력하려면 숫자 2를 입력해주세요. : ")
    if mode == "1" :
        print("=====")
        print(f"TOP1 = 가격 : {result[0]['price']} / 링크 : {result[0]['link']}")
        print(f"TOP2 = 가격 : {result[1]['price']} / 링크 : {result[1]['link']}")
        print(f"TOP3 = 가격 : {result[2]['price']} / 링크 : {result[2]['link']}")
        print("=====")
        break

    elif mode == "2" :
        print("=====")
        for i in range(len(result)) :
            print(f"{i+1}등 = 가격 : {result[i]['price']} / 링크 : {result[i]['link']}")
        print("=====")
        break

    else :
        print("제대로 입력해주세요")
```

이 코드는 [이전](https://github.com/dpan0883/best_marketprice)에 올렸던 코드이고 새로 추가된 명령어를 알아볼 것이다.

```python
options.add_argument("--headless")
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')
```

이 부분을 새로 추가하였는데 GUI가 없는 리눅스 환경에서 구동할 수 있게 설정해주기 위해 headless와 disable-gpu를 추가하였고 headless 옵션 때문에 robot.txt가 뜨는 경우를 방지하기 위해 user-agent를 추가해주었다.

그리고 PC환경에서의 창을 크롤링 하기 위해 원도우 사이즈를 고정시켜서 미연의 오류를 방지한다

마지막으로 no sandbox를 이용해 리눅스안에선 root에서 크롬을 실행시 자주 오류가 뜨는데 이것을 방지하기 위해 추가하였다.

---

# 실행

![캡처](https://user-images.githubusercontent.com/50360713/218379345-348b0742-2ab7-44fa-8670-9637a1a95a6a.PNG)

먼저 docker build 명령어를 이용해 이미지를 만들어 준다.

![캡처](https://user-images.githubusercontent.com/50360713/218376394-80291202-0ef5-44bb-b2f2-3b4c04b8e9fc.PNG)

다음으로 이미지를 이용해 도커 컨테이너를 만들면 바로 프로그램이 실행되면서 위와같이 작동된 후 컨테이너가 꺼진다.
