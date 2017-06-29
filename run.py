# -*- coding: utf-8 -*-
from parse import Handler
from models import Operate
from config import BASE_URL

# get movie data
base_url = BASE_URL
operate = Operate()

# 该网站目前最大的电影序号为23576
for i in range(2, 23577):
    print(i)
    payload = (str(i) + '.html')
    try:
        page = Handler(base_url + payload)
    except Exception as error:
        print('url: ' + base_url + payload)
        print('error: {0}'.format(error))
        # 主动销毁error变量
        del error
    if page.movie:
        try:
            operate.insert(page.movie)
        except Exception as error:
            print("ERROR： {0}".format(error))
            del error
    # 主动销毁page对象
    del page
print('Get movie successfully!')

