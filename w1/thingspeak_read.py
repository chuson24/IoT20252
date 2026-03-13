import requests

# URL
url = "https://api.thingspeak.com/channels/1529099/feeds.json?results=2"

response = requests.get(url)
data = response.json()  # chuyển dữ liệu JSON sang dạng Python

for feed in data['feeds']:
    print("Field1 (Temperature):", feed['field1'])
    print("Field2 (Humidity):", feed['field2'])
    print("---")

