import requests

url = "https://uselessfacts.jsph.pl/random.json"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data['text'])
else:
    print("Error: Request failed with status code", response.status_code)