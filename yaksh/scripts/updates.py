import xmltodict



import requests as req
import json
import datetime as dt

from dateutil.parser import parse

courses = req.get('http://127.0.0.1:8000/api/all_courses')
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
            # getres = req.get(f'http://127.0.0.1:8000/api/updates/{newguid}')
            # if getres.status_code == 200:
            #     continue
            if update['title'].find('result') !=-1:
                response = req.post('http://127.0.0.1:8000/api/updates/', json={'headline': update['title'], 'description': update['title'], 'link': update['link'], 'type': 'result', 'guid': update['guid']['#text'],'pubDate': pdate.isoformat(), 'course': cid})
                print(response.status_code)
                if response.status_code == 500:
                    break
            elif update['title'].find('admit') !=-1:
                response = req.post('http://127.0.0.1:8000/api/updates/', json={'headline': update['title'], 'description': update['title'], 'link': update['link'], 'type': 'admit_card', 'guid': update['guid']['#text'],'pubDate': pdate.isoformat(), 'course': cid})
                print(response.status_code)
                if response.status_code == 500:
                    break
            else:
                response = req.post('http://127.0.0.1:8000/api/updates/', json={'headline': update['title'], 'description': update['title'], 'link': update['link'], 'type': 'announcement', 'guid': update['guid']['#text'],'pubDate': pdate.isoformat(), 'course': cid})
                print(response.status_code)
                if response.status_code == 500:
                    break
            print(update['title'])
except Exception as e:
    print(e)