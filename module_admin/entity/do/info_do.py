from sqlalchemy import DateTime, Column, SmallInteger, String, Integer
from config.database import Base


class PracticalInfo(Base):
    """
    实用信息表
    """

    __tablename__ = 'practical_info'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='主键ID')
    md_content = Column(String(255), nullable=False, comment='实用信息的URL地址')
    is_deleted = Column(SmallInteger, nullable=True, comment='逻辑删除标志，0表示未删除，1表示已删除')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')



