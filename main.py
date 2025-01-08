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