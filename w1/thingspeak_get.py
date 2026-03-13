import requests  # thư viện gửi HTTP

# API Key
api_key = "T7H40F0X82VGW7L5"

# Dữ liệu cần gửi
field1 = 25
field2 = 60

# URL 
url = f"https://api.thingspeak.com/update?api_key={api_key}&field1={field1}&field2={field2}"

response = requests.get(url)

print("Kết quả server trả về:", response.text)
