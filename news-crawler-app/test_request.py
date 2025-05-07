import requests

url = 'https://www.reuters.com/world/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
response = requests.get(url, headers=headers)

print("Status code:", response.status_code)
print("Page length:", len(response.text))
