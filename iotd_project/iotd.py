import streamlit as st
import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()
api_key = getenv("NASA")
url = f"https://api.nasa.gov/planetary/apod?&api_key={api_key}"
response = requests.get(url)
content = response.json()
explanation = content['explanation']
image_url = content['url']
author = content['copyright']
title = content['title'].title()
date = content['date']
st.set_page_config(page_title="api.nasa/apod", page_icon="🌌")

st.title("🌌 "+title)

st.image(image_url)

st.markdown(f"<div style='text-align: justify'>{explanation}.</div>", unsafe_allow_html=True)
st.info(f"By: {author}, {date}")
