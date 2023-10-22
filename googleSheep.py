import pandas as pd
import pygsheets
import json

gc = pygsheets.authorize(service_file='amazing-centaur-402708-e4103538d255.json')

sh = gc.open('facebook_club_post')
wks = sh[0] 

with open('data/club_posts.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

dataset = pd.DataFrame(data)
wks.set_dataframe(dataset, start='A1')