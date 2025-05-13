from sqlalchemy import DECIMAL, TIMESTAMP, SmallInteger, String, Text, Column, Integer
from config.database import Base


class Products(Base):
    """
    products表
    """

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, nullable=False, comment='')
    name = Column(String(100), nullable=True, comment='')
    cover_img = Column(String(255), nullable=True, comment='')
    price_cny = Column(DECIMAL, nullable=True, comment='')
    type = Column(String(20), nullable=True, comment='')
    ai_balance = Column(Integer, nullable=True, comment='')
    price_hkd = Column(DECIMAL, nullable=True, comment='')
    introduction = Column(Text, nullable=True, comment='')
    expiry = Column(Integer, nullable=True, comment='')
    is_deleted = Column(SmallInteger, nullable=True, comment='')
    created_at = Column(TIMESTAMP, nullable=True, comment='')
    updated_at = Column(TIMESTAMP, nullable=True, comment='')



