# -*- coding: utf-8 -*-
from parse import Handler
from models import Operate
from config import BASE_URL

# get movie data
base_url = BASE_URL
movie_list = []

# 该网站目前最大的电影序号为23576
for i in range(21022, 21024):
    payload = (str(i) + '.html')
    try:
        page = Handler(base_url + payload)
        movie_list.append(page.movie)
    except Exception as e:
        print('url: ' + base_url + payload)
        print('error: {error}'.format(error = error))

print('Get movie successfully!')

# insert into database
operate = Operate()
for i in movie_list:
    try:
    	operate.insert(i)
    except Exception as error:
        print("ERROR： {error}".format(error = error))

print("Insert movies'data to mysql successfully!")
