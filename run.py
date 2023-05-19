import requests
import bs4
import pandas as pd
import re
import datetime

pattern = re.compile(r'\s+')
dt = datetime.datetime.now()

dic_month = {1: 'jan', 2: 'feb', 3: 'mar',
             4: 'apr', 5: 'may', 6: 'jun',
             7: 'jul', 8: 'aug', 9: 'sep',
             10: 'oct', 11: 'nov', 12: 'dec'}


def month_():
    for item in dic_month:
        if dt.month == item:
            return str(dic_month[item]) + str(dt.day) + '.' + str(dt.year)


resp = requests.get('https://www.forexfactory.com/calendar.php?week=' + month_())
resp.encoding = 'utf-8'
html = resp.text
bs = bs4.BeautifulSoup(html, 'html.parser')

# find로 html table 가져오기
findTable = bs.find('table', {'class': "calendar__table"})

# 각 데이터를 담을 list
dateList = []
timeList = []
currencyList = []
eventList = []
actualList = []
forecastList = []
previousList = []

# findAll로 event 부분만 가져오기
findDate = findTable.find_all('td', {'class': "calendar__cell calendar__date date"})
findTime = findTable.find_all('td', {'class': "calendar__cell calendar__time time"})
findCurrency = findTable.find_all('td', {'class': "calendar__cell calendar__currency currency"})
findEvent = findTable.find_all('td', {'class': 'calendar__cell calendar__event event'})
findActual = findTable.find_all('td', {'class': 'calendar__cell calendar__actual actual'})
findForecast = findTable.find_all('td', {'class': 'calendar__cell calendar__forecast forecast'})
findPrevious = findTable.find_all('td', {'class': 'calendar__cell calendar__previous previous'})

tempVal_Date = None
for i in findDate:
    if i.text == ' ':
        dateList.append(tempVal_Date.text)
    else:
        dateList.append(i.text)
        tempVal_Date = i

tempVal_Time = None
for i in findTime:
    time = str(i.text).replace('\xa0', '')
    if time == '':
        timeList.append(tempVal_Time)
    else:
        timeList.append(time)
        tempVal_Time = time

for rows in findCurrency:
    currency = re.sub(pattern, '', rows.text)
    currencyList.append(currency)

for i in findEvent:
    event = str(i.text).strip()
    eventList.append(event)

for i in findActual:
    actualList.append(i.text)

for i in findForecast:
    forecastList.append(i.text)

for i in findPrevious:
    previousList.append(i.text)

allContent = []
rowContent = []

for i in range(len(dateList)):
    rowContent.append(dateList[i])
    rowContent.append(timeList[i])
    rowContent.append(currencyList[i])
    rowContent.append(eventList[i])
    rowContent.append(actualList[i])
    rowContent.append(forecastList[i])
    rowContent.append(previousList[i])
    allContent.append(rowContent)
    rowContent = []

for i in allContent:
    print(i)

result = pd.DataFrame(allContent)
today = datetime.datetime.now().strftime('%Y-%m-%d')
result.to_csv('./forexFactory_' + today + '.csv', encoding='ms949', index=False)
print(result)

# for i in eachRow:
#     for eachCol in i:
#         findDate = eachCol.find('span', {'class': "date"})
#         findTime = eachCol.find('td', {'class': "calendar__cell calendar__time time"})
#         findCurrency = eachCol.find('td', {'class': "calendar__cell calendar__currency currency"})
#         findEvent = eachCol.find('td', {'class': 'calendar__cell calendar__event event'})
#         findActual = eachCol.find('td', {'class': 'calendar__cell calendar__actual actual'})
#         findForecast = eachCol.find('td', {'class': 'calendar__cell calendar__forecast forecast'})
#         findPrevious = eachCol.find('td', {'class': 'calendar__cell calendar__previous previous'})
#         rowContent.append(findDate.text)
#         rowContent.append(findTime.text)
#         rowContent.append(findCurrency.text)
#         rowContent.append(findEvent.text)
#         rowContent.append(findActual.text)
#         rowContent.append(findForecast.text)
#         rowContent.append(findPrevious.text)
#     allContent.append(rowContent)
#     rowContent = []

# calendar__row calendar_row calendar__row--grey << unable to select all content
# eachRow = findTable.find_all('tr', {'class': 'calendar__row calendar_row calendar__row--grey'})
# print(eachRow)
# for i in eachRow:
#     findDate = i.find('span', {'class': "date"})
#     findTime = i.find('td', {'class': "calendar__cell calendar__time time"})
#     findCurrency = i.find('td', {'class': "calendar__cell calendar__currency currency"})
#     print(findDate)
#     print(findTime.text)
#     currency = re.sub(pattern, '', findCurrency.text)
#     print(currency)

#     rowContent.append(findDate.text)
#     rowContent.append(findTime.text)
#     allContent.append(rowContent)
#     rowContent = []
#
# print(allContent)

# for rows in findTable:
#     eachRow = rows.find_all('tr', {'class': 'calendar__row calendar_row calendar__row--grey'})
#     print(eachRow)

# for i in findCurrency:
#     print(i.text, end='')

# for i in findPrevious:
#     print(i.text)
