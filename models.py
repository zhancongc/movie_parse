# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, Unicode, UnicodeText
from sqlalchemy import select, and_, or_, asc, desc

Base = declarative_base()
class Movies(Base):
    __tablename__ = 'Movies'
    id = Column('id', Integer, primary_key=True)
    url = Column('url', String(128))
    title = Column('title', UnicodeText())
    image = Column('img', String(128))
    year = Column('year', Integer())
    area = Column('area', Unicode(128))
    score = Column('score', Integer)
    label = Column('label', Unicode(128))
    director = Column('director', Unicode(128))
    actor = Column('actor', Unicode(128))
    imdb = Column('imdb', String(128))
    introduction = Column('introduction', UnicodeText())
    thunder = Column('thunder', String(256))
    magnet = Column('magnet', String(256))

engine = create_engine('mysql+pymysql://root:security@localhost:3306/movie?charset=utf8mb4')

Base.metadata.bind = engine
Base.metadata.create_all()

Session = sessionmaker(bind=engine)
session = Session()

obj = Movies(
    url='http://m.idyjy.com/sub/112.html',
    title='三不管',
    image='http://img.idyjy.com/pic/uploadimg/2016-3/112.jpg',
    year='2008',
    area='香港',
    score='4.9分',
    label='动作 惊悚',
    director='邱礼涛',
    actor='林家栋，连凯，田蕊妮，方皓玟，陈望华，黄树棠',
    imdb='tt1288398',
    introduction='详细剧情：在城市尽头的破落寨城里聚居着的都是走投无路, 或拥有见不得光的过去的人. 他们干着「黄, 赌, 毒」等不法勾当. 这里有自己的秩序, 律法. 寨城俨如一个「三不管」的地带. 一天, 米奇用警车押解罪犯大海, 却失事闯入寨城, 更被寨城内 的人所扣押. 寨城霸主乌鸦憎恨警察, 认为两人当中必有一人是警察, 并准备处决其中一人. 此时, 寨城内经营妓院的阿玲却指诬诋大海才是警察. 米奇因此而获得 释放, 而大海则继续被扣押.原来, 大海是阿玲多年不见的情人, 阿玲认为大海抛弃了她和女儿阿恩, 所以要让大海吃苦头. 同时, 她希望得到米奇的帮助离开城寨, 因为乌鸦一直对阿恩虎视眈眈. 而阿恩遇到被拘禁的大海, 虽然不知道对方是自己父亲, 却因为一种感觉而决定要协助大海脱险. 与此同时, 寨城发现严重的致命瘟 疫, ZF更借口要屠城阻止瘟疫蔓延. 到底米奇, 大海, 阿玲母女四人能否脱离被屠杀的厄运?而大海和阿恩又会否父女相认?',
    thunder='thunder://QUFlZDJrOi8vfGZpbGV8ob6159OwvNLUsHd3dy5pZHlqeS5jb23PwtTYob/I/bK7udxEVkS5+tPv1tDX1mNkMS5ybXZifDE5MTIzMzcxMXw2NUU1OUVFQjIxNjExNzE0OEU2NDk0QUU3QzdBQjUxMHxoPTJXSlhSTUtBU1ZRSEozM0laUFhHVklGUlVCTzZaT0dSfC9aWg==',
    magnet=''
)
session.add(obj)
session.flush()
session.commit()