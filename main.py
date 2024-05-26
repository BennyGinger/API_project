import requests

api_key = '22814014830945708becbca6300ee90e'

url = "https://newsapi.org/v2/everything?q=tesla&from=2024-04-26&sortBy" \
        "=publishedAt&apiKey=22814014830945708becbca6300ee90e"

# Make a request
request = requests.get(url)

# Get the data
content = request.json()
for article in content['articles']:
    print(article['title'])