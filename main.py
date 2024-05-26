import requests
from send_email import send_email

api_key = '22814014830945708becbca6300ee90e'

url = "https://newsapi.org/v2/everything?q=tesla&from=2024-04-26&sortBy" \
        "=publishedAt&apiKey=22814014830945708becbca6300ee90e"

# Make a request
request = requests.get(url)

# Get the data
content = request.json()
articles = []
for article in content['articles']:
    articles.append(f"{article['title']}\n {article['description']}\n")
    
articles = "\n".join(articles)

msg = f"""Subject: News about Tesla\n\n
    {articles}""".encode("utf-8")

send_email(msg)