import requests
from send_email import send_email
from datetime import datetime
from dotenv import load_dotenv
from os import getenv

load_dotenv()
api_key = getenv("NEWS")
query = 'tesla'
from_date = '2024-05-26'
to_date = datetime.today().strftime("%Y-%m-%d")
language = 'en'
parent_url = 'https://newsapi.org/v2/everything?'

url = f"{parent_url}q={query}&from={from_date}&to={to_date}&sortBy=publishedAt&language={language}&apiKey={api_key}"

# Make a request
request = requests.get(url)

# Get the data
content = request.json()
articles = []
for article in content['articles'][:20]:
    body = f"{article['title']}\n {article['description']}\n {article['url']}\n"
    articles.append(body)
    
articles = "\n".join(articles)

msg = f"""Subject: News about Tesla\n\n
    {articles}""".encode("utf-8")

send_email(msg)