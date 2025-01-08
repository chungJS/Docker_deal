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
#ADD https://raw.githubusercontent.com/dpan0883/best_marketprice/main/main.py .
COPY main.py .

#크롬 설치
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install ./google-chrome-stable_current_amd64.deb -y
#크롬 드라이버(셀레니움 설치)
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /dir

CMD [ "python3", "/dir/main.py" ]