# -*- coding: utf-8 -*-
import requests, random
from bs4 import BeautifulSoup as BS
from config import USER_AGENT

class Handler(object):
    ''' Get movies '''
    def __init__(self, url):
        self.url = url
        self.header = self._random_header_()
        self.content = self._get_content_()
        self.movie = self._get_movie_()

    @staticmethod
    def _random_header_():
        '''random headers makes requests looks like human doing''' 
        head_connection = ['Keep-Alive','close']
        head_accept = ['text/html, application/xhtml+xml, */*']
        head_accept_language = ['zh-CN,fr-FR;q=0.5','en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
        head_user_agent = USER_AGENT
        header = {
            'Connection': head_connection[0],
            'Accept': head_accept[0],
            'Accept-Language': head_accept_language[1],
            'User-Agent': head_user_agent[random.randrange(0,len(head_user_agent))]
        }
        return header

    def _get_content_(self):
        ''' get html content which contains movies' data '''
        if self.url is None:
            return None
        try:
            response = requests.get(self.url, headers=self.header)
        except Exception as e:
            print("Fail to open the url, error: {0}".format(e))
            return None
        self.status_code = response.status_code
        if response.status_code != 200:
            return None
        return response.content

    @staticmethod
    def _parse_text_(obj):
        obj.em.clear()
        return obj.get_text()

    def _get_movie_(self):
        ''' extract html content and movies' data will be in a list '''
        if self.content == None:
            return None
        soup = BS(self.content, 'lxml', from_encoding='gb2312')
        # get title and image
        picture = soup.find('div', attrs={'class': 'posterPic'}).find('img')
        title, image = picture.get('alt'), picture.get('src')
        # get year, area, score, label, director and actor
        tmp = soup.find('em', text='上映年代：')
        if tmp:
            year = str(self._parse_text_(tmp.parent))
        else:
            year = ''
        tmp = soup.find('em', text='地区：')
        if tmp:
            area = self._parse_text_(tmp.parent)
        else:
            area = ''
        tmp = soup.find('em', text='评分：')
        if tmp:
            score = str(self._parse_text_(tmp.parent)[:-1])
        else:
            score = ''
        tmp = soup.find('em', text='类型：')
        if tmp:
            label = self._parse_text_(tmp.parent)
        else:
            label = ''
        tmp = soup.find('em', text='导演：')
        if tmp:
            director = self._parse_text_(tmp.parent)
        else:
            director = ''
        tmp = soup.find('em', text='主演：')
        if tmp:
            actor = self._parse_text_(tmp.parent)
        else:
            actor = ''
        # get imdb
        tmp = soup.find('em', text='IMDB：')
        if tmp:
            imdb = self._parse_text_(tmp.parent)
        else:
            imdb = ''
        # get introduction
        intro = soup.find_all('div', attrs={'class':'pSummary globalPadding'})[-1].get_text()

        # get thunder and magnet
        uls = soup.find_all('ul', attrs={'class': 'dramaNumList dramaNumList3 clearfix'})
        if len(uls) == 2:
            thunder, magnet = uls[0].a.get('href'), uls[1].a.get('href')
        elif len(uls) == 1:
            thunder, magnet = uls[0].a.get('href'), ''
        else:
            thunder, magnet = '', ''
        movie = {
            'url': self.url,
            'title': title,
            'img': image,
            'year': year,
            'area': area,
            'score': score,
            'label': label,
            'director': director,
            'actor': actor,
            'imdb': imdb,
            'introduction': intro,
            'thunder': thunder,
            'magnet': magnet
        }
        return movie
