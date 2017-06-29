# -*- coding: utf-8 -*-
from parse import Handler
from models import Operate
from config import BASE_URL

# get movie data
base_url = BASE_URL
operate = Operate()

# 该网站目前最大的电影序号为23576
for i in range(2, 23577):
    payload = (str(i) + '.html')
    url = base_url + payload
    print('Current url: {0}'.format(url))
    try:
        page = Handler(url)
    except Exception as error:
        print('error: {0}'.format(error))
        # 主动销毁error变量
        del error
    else:
        if page.movie:
            try:
                operate.insert(page.movie)
            except Exception as error:
                print("ERROR： {0}".format(error))
                del error
        else:
            print("There are no movie in current page.")
        # page对象使用完毕后，主动销毁
        del page

print('Get movie successfully!')
