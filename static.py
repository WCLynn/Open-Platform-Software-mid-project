import requests
from bs4 import BeautifulSoup
import csv
import re

web = requests.get("https://www.ettoday.net/news/hot-news.htm")
soup = BeautifulSoup(web.text, "html.parser")
Div_Temp = soup.findAll('div', "piece clearfix")
max = 10
titles = []
links = []
Keywords = []
cnt = 0

for link in Div_Temp:
    cnt += 1
    a_tag = link.find('a', class_='pic')
    title = link.find('h3')
    if link:
        href = a_tag['href']
        if re.match(r"^//", href):
            continue
        links.append(href)
    if title:
        titles.append(title.text)
    if cnt == max:
        break  

for t, l in zip(titles, links):
    web_content = requests.get(l)
    soup_content = BeautifulSoup(web_content.text, "html.parser")
    meta_tag = soup_content.find('meta', {'name': 'news_keywords'})    
    if meta_tag:
        content = meta_tag['content']
        Keywords.append(content)


data = zip(titles, Keywords)        

# write CSV
filename = "static.csv"
with open(filename, mode='w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Keyword"])  # 寫入欄位名稱
    writer.writerows(data)  # 寫入每一筆資料

print(f"CSV檔案已儲存為 {filename}")

