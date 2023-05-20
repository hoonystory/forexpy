import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime

from selenium import webdriver
import time

pattern = re.compile(r'\s+')
dt = datetime.datetime.now()
phantomjs_path = 'c:\\phantomJS\\bin\\phantomjs.exe'

# url = 'http://pythonscraping.com/pages/javascript/ajaxDemo.html'
url = 'https://kr.investing.com/earnings-calendar'
driver = webdriver.PhantomJS(executable_path=phantomjs_path)
driver.get(url)

# time.sleep(3)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

findTable = soup.find('table', {'id': 'earningsCalendarData'})
# findCompany = findTable.find_all('td', {'class': "left noWrap earnCalCompany"})
findName = findTable.find_all('span', {'class': "earnCalCompanyName middle"})
findSymbol = findTable.find_all('a')
findEPS = soup.select('#earningsCalendarData > tbody > tr > td:nth-child(3)')
findEPS_Forecast = soup.select('#earningsCalendarData > tbody > tr > td:nth-child(4)')
findRevenue = soup.select('#earningsCalendarData > tbody > tr > td:nth-child(5)')
findRevenue_Forecast = soup.select('#earningsCalendarData > tbody > tr > td:nth-child(6)')
findMarketCap = findTable.find_all('td', {'class': 'right'})
findTime = findTable.find_all('td', {'class': 'right time'})

name_result = []
symbol_result = []
eps_result = []
epsForecast_result = []
revenue_result = []
revenueForecast_result = []
marketCap_result = []
time_result = []

# result.append(driver.find_element_by_id("earningsCalendarData").text)
# result.append(driver.find_element_by_class_name('earnCalCompanyName').text)

# print(findMarketCap)

# M, B와 같은 문자열 --> 숫자 처리
# 크롤링 시간 정하기
# 과거 데이터 크롤링

for i in findName:
    name_result.append(i.text)
for i in findSymbol:
    symbol_result.append(i.text)
for i in findEPS:
    eps_result.append(i.text)
for i in findEPS_Forecast:
    result = str(i.text).replace('\xa0', '').replace('/', '')
    epsForecast_result.append(result)
for i in findRevenue:
    revenue_result.append(i.text)
for i in findRevenue_Forecast:
    result = str(i.text).replace('\xa0', '').replace('/', '')
    revenueForecast_result.append(result)
for i in findMarketCap:
    marketCap_result.append(i.text)

# for i in findTable:
#     time_result.append(i.text)

# 실적발표 없는 경우, DB에 업로드 중지

print(name_result)
print(symbol_result)
print(eps_result)
print(epsForecast_result)
print(revenue_result)
print(revenueForecast_result)
print(marketCap_result)

result = pd.DataFrame(zip(name_result, symbol_result,
                          eps_result, epsForecast_result,
                          revenue_result, revenueForecast_result, marketCap_result),
                      columns=['Company', 'Symbol', 'EPS',
                               'Forecast', 'Revenue', 'Forecast', 'MarketCap'])
print(result)
today = datetime.datetime.now().strftime('%Y-%m-%d')
result.to_csv('./earningCalender_result' + today + '.csv', encoding='ms949', index=False)

# 데이터 프레임 변환
# finalResult = pd.DataFrame(zip(nameList,linkList), columns=["title","link"])
# csv 파일로 저장
# finalResult.to_csv("./link_scraping_result.csv",encoding="ms949", index=False)


# print(soup)
driver.close()
