from sqlalchemy import Integer, String, Column, Text, TIMESTAMP
from config.database import Base


class News(Base):
    """
    news表
    """

    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='')
    language = Column(String(10), nullable=True, comment='')
    source = Column(String(100), nullable=True, comment='')
    date = Column(String(10), nullable=True, comment='')
    content = Column(Text, nullable=True, comment='')
    url = Column(String(500), nullable=True, comment='')
    created_at = Column(TIMESTAMP, nullable=True, comment='')
    title = Column(String(200), nullable=True, comment='')
    news_type = Column(String(50), nullable=True, comment='新闻类别')



