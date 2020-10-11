# imports for current affairs
import joblib
import os
import nltk

# from yaksh.models import CurrentAffairs

from nltk.corpus import stopwords

from nltk.stem.snowball import SnowballStemmer

import string
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English

import requests as req

import pandas as pd

import json

import re

import datetime as dt
from dateutil.parser import parse

# from django.conf import settings

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("server", help="Posts Current Affairs data to Development Server or Production Server. Type 'prod' for production and 'dev' for development")
parser.add_argument("date", help="Enter the date Current affairs to be posted format: [dd-mm-yy]")
args = parser.parse_args()



print(args.server)
print(args.date)
if args.server == "prod":
    server_url="https://missionpcs.com/"
elif args.server == "dev":
    server_url="http://127.0.0.1:8000/"
else:
    print("Please use -h argument for help")
    exit()

url = 'http://127.0.0.1:8000/api/login/'
cred = {'username': 'test', 'password': 'test'}


nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
punctuations = string.punctuation
# Create our list of stopwords
stop_words = STOP_WORDS
# Load English tokenizer, tagger, parser, NER and word vectors
parser = English()


#utils functions
def clean_text(text, remove_stopwords=True, stem_words=False, stop_words=stop_words):
    # Convert words to lower case and split them
    text = str(text)
    # text = re.sub(r"IT", "information technology", text)
    text = text.lower().split()
    # Optionally, remove stop words
    if remove_stopwords:
        stops = set(stop_words)
        text = [w for w in text if not w in stops]

    text = " ".join(text)

    # Clean the text
    text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r",", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\/", " ", text)
    text = re.sub(r"\^", " ^ ", text)
    text = re.sub(r"\+", " + ", text)
    text = re.sub(r"\-", " - ", text)
    text = re.sub(r"\=", " = ", text)
    text = re.sub(r"'", " ", text)
    text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
    text = re.sub(r":", " : ", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r" u s ", " american ", text)
    text = re.sub(r"\0s", "0", text)
    text = re.sub(r" 9 11 ", "911", text)
    text = re.sub(r"e - mail", "email", text)
    text = re.sub(r"j k", "jk", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = text.replace('http\S+|www.\S+', '')

    # Optionally, shorten words to their stems
    if stem_words:
        text = text.split()
        stemmer = SnowballStemmer('english')
        stemmed_words = [stemmer.stem(word) for word in text]
        text = " ".join(stemmed_words)
    return ''.join(text)
    # Return a cleaned text

def spacy_tokenizer(sentence):
    # Creating our token object, which is used to create documents with linguistic annotations.
    mytokens = parser(sentence)
    # Lemmatizing each token and converting each token into lowercase
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]

    # Removing stop words
    mytokens = [ word for word in mytokens if word not in stop_words and word not in punctuations ]
    
    return mytokens
    # return preprocessed list 




# if __name__ == "__main__":
    
# model = joblib.load(os.path.join(settings.BASE_DIR, "current_affairs", "current_affairs_classification_joblib"))

model = joblib.load("../../current_affairs/current_affairs_classification_joblib")

# vectorizer = joblib.load(os.path.join(settings.BASE_DIR, "current_affairs", "bow_vectorizer_joblib"))
vectorizer = joblib.load("../../current_affairs/bow_vectorizer_joblib")

df = []
# with open(os.path.join(settings.BASE_DIR, "current_affairs", "today.json")) as f:

with open(f"../../current_affairs/{args.date}.json") as f:
    data = json.load(f)
    df.append(pd.DataFrame(data))
jsondata = pd.concat(df)
jsondata['news'] = jsondata['title = '] + '. ' + jsondata['total news']
jsondata['news']
jsondata['newsclean'] = jsondata['news'].apply(lambda x : clean_text(x))

vecnews = vectorizer.transform(jsondata['newsclean'])
jsondata['current_affairs'] = model.predict(vecnews)

user_response = req.post(url, data = cred)
user_token = user_response.json()['token']
ca_data = jsondata[jsondata['current_affairs'] == '1']

for dat in ca_data['title = '].index:
    pdate = ca_data['date = '][dat]
    pdateobj = dt.datetime.strptime(pdate, '%d/%m/%Y')
    
    if re.search(r'\b(\w*letter\w*)\b', ca_data['title = '][dat], re.IGNORECASE) and re.search(r'\b(\w*editor\w*)\b', ca_data['title = '][dat], re.IGNORECASE):
        continue
    response = req.post(f'{server_url}api/current_affairs/', json={'summary': ca_data['summary = '][dat], 'title': ca_data['title = '][dat], 'news': ca_data['total news'][dat], 'link': ca_data['link = '][dat], 'pubDate': pdateobj.isoformat() }, headers={'Authorization': f'token {user_token}'})
    print(ca_data['title = '][dat])
    print(response.status_code)
    # a = CurrentAffairs.objects.create(summary=ca_data['summary = '][dat], title=ca_data['title = '][dat], news=ca_data['newsclean'][dat])
    # a.save()

print("Current Affairs added")