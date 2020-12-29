import requests
from pprint import pprint

days = 2
tag = 'Python'

response = requests.get('https://api.stackexchange.com/2.2/search',
                        params={
                                'site': 'stackoverflow',
                                'tagged': 'Python',
                                'fromdate': '2020-12-28',
                                'pagesize': 100,
                                'page': 1
                                })

for item in response.json()['items']:
    pprint(item['title'])
