import requests
import re
import csv
import os


API_KEY = os.getenv('YOUTUBE_API')
print(API_KEY)
# API請求參數
url = "https://www.googleapis.com/youtube/v3/videos"
params = {
    "part": "snippet,statistics,contentDetails",  # 獲取影片基本資料和統計資料
    "chart": "mostPopular",        # 熱門影片
    "regionCode": "TW",            # 設定區域（台灣）
    "maxResults": 20,              # 獲取最多幾部影片
    "key": API_KEY
}

def parse_duration(duration):
    match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', duration)
    hours = int(match.group(1)[:-1]) if match.group(1) else 0
    minutes = int(match.group(2)[:-1]) if match.group(2) else 0
    seconds = int(match.group(3)[:-1]) if match.group(3) else 0
    return hours, minutes, seconds


# 發送 GET 請求
response = requests.get(url, params=params)
titles = []
Data = []
# 處理回應
if response.status_code == 200:
    data = response.json()
    for item in data['items']:
        title = item['snippet']['title']
        views = item['statistics']['viewCount']
        likes = item['statistics']['likeCount']
        duration = item['contentDetails']['duration']
        hours, minutes, seconds = parse_duration(duration)
        Length = f'{hours}:{minutes}:{seconds}'
        hashtags = re.findall(r"(?<=#)\S+", title)
        if len(hashtags) == 0:
            hashtags = "No hashtag"
        else:
            title = re.sub(r"\s*#\S+\s*", "", title)

        Data.append([title,Length,views,likes,hashtags])
else:
    print("錯誤: 無法獲取資料，請檢查 API 金鑰或請求設定")
    
# write CSV
filename = "api.csv"
with open(filename, mode='w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Length", "View", "Like", "Hashtag"])  # 寫入欄位名稱
    writer.writerows(Data)  # 寫入每一筆資料
