import xmltodict



import requests as req
import json
import datetime as dt

from dateutil.parser import parse

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("server", help="Posts Current Affairs data to Development Server or Production Server. Type 'prod' for production and 'dev' for development")
args = parser.parse_args()

print(args.server)

if args.server == "prod":
    server_url="https://missionpcs.com/"
elif args.server == "dev":
    server_url="http://127.0.0.1:8000/"
else:
    print("Please use -h argument for help")
    exit()

url = 'http://127.0.0.1:8000/api/login/'
cred = {'username': 'test', 'password': 'test'}

courses = req.get(f'{server_url}api/all_courses')

user_response = req.post(url, data = cred)
user_token = user_response.json()['token']
try:
    for course in courses.json():
        name = course['name']
        url = f'https://news.google.com/rss/search?q={name}&hl=en-US&sort=date&gl=US&num=10&ceid=US:en'
        cid = course['id']
        xml = req.get(url)
        for update in json.loads(json.dumps(xmltodict.parse(xml.text)))['rss']['channel']['item']:
            pdate = parse(update['pubDate'])
            print(pdate.isoformat())
            # newguid = update['guid']['#text']
            # getres = req.get(f'{server_url}api/updates/{newguid}')
            # if getres.status_code == 200:
            #     continue
            if update['title'].find('result') !=-1:
                response = req.post(f'{server_url}api/updates/', json={'headline': update['title'], 'description': update['title'], 'link': update['link'], 'type': 'result', 'guid': update['guid']['#text'],'pubDate': pdate.isoformat(), 'course': cid}, headers={'Authorization': f'token {user_token}'})
                print(response.status_code)
            elif update['title'].find('admit') !=-1:
                response = req.post(f'{server_url}api/updates/', json={'headline': update['title'], 'description': update['title'], 'link': update['link'], 'type': 'admit_card', 'guid': update['guid']['#text'],'pubDate': pdate.isoformat(), 'course': cid}, headers={'Authorization': f'token {user_token}'})
                print(response.status_code)
            else:
                response = req.post(f'{server_url}api/updates/', json={'headline': update['title'], 'description': update['title'], 'link': update['link'], 'type': 'announcement', 'guid': update['guid']['#text'],'pubDate': pdate.isoformat(), 'course': cid}, headers={'Authorization': f'token {user_token}'})
                print(response.status_code)
            print(update['title'])
except Exception as e:
    print(e)