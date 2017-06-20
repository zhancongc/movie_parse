# coding = utf-8
import requests, random
from bs4 import BeautifulSoup as BS

class Handler(object):
    ''' Get movies '''
    def __init__(self, url, payload):
        self.url = url
        self.payload = payload
        self.header = self._random_header_()
        self.content = self._get_content_()
        self.movie = self._get_movie_()

    @staticmethod
    def _random_header_():
        '''random headers makes requests looks like human doing''' 
        head_connection = ['Keep-Alive','close']
        head_accept = ['text/html, application/xhtml+xml, */*']
        head_accept_language = ['zh-CN,fr-FR;q=0.5','en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
        head_user_agent = [
            'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
            'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
            'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
            'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
            'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11'
        ]
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
            response = requests.get(self.url + self.payload, headers=self.header)
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
        soup = BS(self.content, 'lxml', from_encoding='gb2312')
        # get title and image
        picture = soup.find('div', attrs={'class': 'posterPic'}).find('img')
        title, image = picture.get('alt'), picture.get('src')

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
        tmp = soup.find('em', text='IMDB：')
        if tmp:
            imdb = self._parse_text_(tmp.parent)
        else:
            imdb = ''
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
            'image': image,
            'year': year,
            'area': area,
            'score': score,
            'label': label,
            'director': director,
            'actor': actor,
            'IMDB': imdb,
            'introduction': intro,
            'thunder': thunder,
            'magnet': magnet
        }
        return movie

    def connect_db(self):
        pass

