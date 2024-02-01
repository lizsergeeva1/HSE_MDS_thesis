import pandas as pd
from urllib.parse import urlparse
import requests
import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from pymystem3 import Mystem


def collect_url_data(url):
    parsed_url = urlparse(url)
    vacancy_id = parsed_url.path.split("/")[-1]
    url_api = 'https://api.hh.ru/vacancies/' + vacancy_id
    response = requests.get(url_api)

    if response.status_code == 200:
        data = response.json()
    else:
        print("Error reading API:", response.status_code)
        return 0

    soup = BeautifulSoup(data['description'], 'html.parser')
    descr_string = soup.get_text()
    descr_clean = clean_and_lemmatize(descr_string)
    key_skills = ', '.join(value['name'].lower() for value in data['key_skills'])
    keys = ['prof_name', 'city', 'schedule', 'employment', 'experience_rus', 'key_skills', 'descr_clean', 'name']
    values = [data['professional_roles'][0]['name'], data['area']['name'],
              data['schedule']['name'], data['employment']['name'],
              data['experience']['name'], key_skills, descr_clean, data['name']
              ]
    return pd.DataFrame(data=values, index=keys).T


def clean_and_lemmatize(text):
    # clean punctuation and stop words
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    stop_words = set(stopwords.words('russian'))
    words = [w for w in words if w not in stop_words]
    # lemmatize
    mystem = Mystem()
    lemmas = [mystem.lemmatize(word)[0] for word in words]
    lemmatized_text = ' '.join(lemmas)
    return lemmatized_text
