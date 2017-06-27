# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, Unicode, UnicodeText
from sqlalchemy import select, and_, or_, asc, desc
from config import SQLALCHEMY_DATABASE_URI

Base = declarative_base()
class Movies(Base):
    __tablename__ = 'Movies'
    id = Column('id', Integer, primary_key=True)
    url = Column('url', String(128))
    title = Column('title', UnicodeText())
    img = Column('img', String(128))
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

class Operate(object):
    def __init__(self):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI)
        self.__init_db__()
        self.session = self._get_session_()

    def _get_session_(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def __init_db__(self):
        Base.metadata.bind = self.engine
        Base.metadata.create_all()

    def insert(self, movie):
        obj = Movies(
            url = movie['url'],
            title = movie['title'],
            img = movie['img'],
            year = movie['year'],
            area = movie['area'],
            score = movie['score'],
            label = movie['label'],
            director = movie['director'],
            actor = movie['actor'],
            imdb = movie['imdb'],
            introduction = movie['introduction'],
            thunder = movie['thunder'],
            magnet = movie['magnet']
        )
        self.session.add(obj)
        self.session.flush()
        self.session.commit()

