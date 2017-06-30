# 电影爬虫（四）

>通过前面三期的内容，终于爬到了福利电影的下载链接。但是，一个完整的爬虫至少要包含数据采集和数据的存储。本期我们就来重点讨论最后一步，数据的存储，同时会涉及到简单的SQLAlchemy的操作。文末还有一个小惊喜，大家要看仔细咯 ^_^

## 数据模型

首先我们要考虑的是：应该将哪些数据存到数据库中？这个要根据实际情况决定，如果不能确定，则越详细越好。这里，我们选取本页面的url、电影名称、地区、评分、迅雷下载链接这5种，它们都可以通过爬虫从页面上爬取。

现在介绍Python社区最流行的一种ORM框架——SQLAlchemy来管理数据库，它本质上是创建了一个中间层，把关系数据库的表结构映射到对象上。有了这个中间层，就避免了直接操作数据库带来的诸多问题，代价就是轻微的性能损失。SQLAlchemy的安装命令如下：

```
pip install sqlalchemy
```

定义一个Movies类，它继承自SQLAlchemy自带的declarative_base()类，规定table的名称为"movies"，然后分别定义table的各个字段。

```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Unicode, UnicodeText
Base = declarative_base()
class Movies(Base):
    __tablename__ = 'movies'
    # 每个table都必须要有一个自动增长的id字段，Integer是整型，primary_key代表主键
    id = Column('id', Integer, primary_key=True)
    # String(128) ASCII编码字符串类型，最大长度为 128 Bytes
    url = Column('url', String(128))
    # UnicodeText() Unicode编码的字符串类型，不限长度
    title = Column('title', UnicodeText())
    # Unicode(128) Unicode编码的字符串类型，最大长度为 128 Bytes
    area = Column('area', Unicode(128))
    score = Column('score', Integer)
    thunder = Column('thunder', String(256))
```

定义好数据模型之后，我们要做的就是连接数据库，按照这个模型创建table。在连接数据库前，首先要确保有一个可以操作的数据库，聪哥用的是本地新建的一个数据库movie。此外，还需要安装pymysql库，它是用来连接MySQL数据库的。

```python
# 下面是engine对象的标准格式，这里我们规定了编码是utf8mb4
# 其中：username, password, ip_address, port, database_name 根据实际情况决定
engine = create_engine(
    'mysql+pymysql://username:password@ip_address:port/database_name?charset=utf8mb4'
)
# 下面是聪哥的engine对象
engine = create_engine(
    'mysql+pymysql://root:security@localhost:3306/movie?charset=utf8mb4'
)
# 绑定engine对象
Base.metadata.bind = engine
# 创建table
Base.metadata.create_all()
```

## 插入数据 

想要进行数据库操作就必须要在ORM和数据库之间创建一个会话，SQLAlchemy提供了创建会话的方法：`sessionmaker()`。

```python
# 引入sessionmaker创建会话
from sqlalchemy.orm import sessionmaker
# 绑定engine对象后创建一个新的Session()对象
Session = sessionmaker(bind=engine)
# 创建一个Session()对象的实例session，我们依靠它来和数据库交互
session = Session()
```

有了会话，我们就可以向table中插入数据了。

```python
# 假设我们爬取的数据是以字典的形式存放的，这个字典的名称是movie
# 新建一个Movies对象的实例obj
obj = Movies(
	url = movie['url'],
	title = movie['title'],
	area = movie['area'],
	score = movie['score'],
	thunder = movie['thunder']
)
# 会话中添加实例obj
session.add(obj)
# 将会话缓存与数据库同步
session.flush()
# 提交，使以上所有操作生效
session.commit()
```

> SQLAlchemy的功能远不止于此，它有众多API，几乎可以实现所有的数据库操作，关于SQLAlchemy的知识，我们以后还会再讲。

到此为止，一个完整的电影爬虫基本就完成了，它包括了爬取网页，解析网页，存入数据库这几个主要步骤。整理一下代码，你会发现内容其实并没有多少。这并不意味着爬虫就这么点知识，前面我们讲的每一步都有值得优化的地方。

可能你早就猜到了，本期的小惊喜就是：爬虫系列完整的代码。它将网页爬取、解析，数据库操作封装为几个类，可以实现全站电影的爬取，大家可以适当参考。GitHub链接：https://github.com/zhancongc/movie_parse。如果有看不懂的地方，随时可以给我留言或者在公众号后台提问。

## 总结

1. ORM在python对象和数据库表结构之间搭起了一个桥梁
2. 可以用SQLAlchemy创建数据库table，关键在于创建一个体现据模型的python类
3. 操作数据库时需要新建一个session会话，使用session.add()可以插入数据

**特别声明：电影爬虫这几期的文章和代码仅供爬虫学习的用途，请大家尊重电影网站的知识产权。**