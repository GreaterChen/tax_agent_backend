from datetime import datetime
from sqlalchemy import DateTime, SmallInteger, Integer, String, Column
from config.database import Base


class PracticalInfo(Base):
    """
    system表
    """

    __tablename__ = 'practical_info'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='主键ID')
    md_content = Column(String(255), nullable=False, comment='实用信息的URL地址')
    language = Column(String(10), nullable=True, comment='语言')
    is_deleted = Column(SmallInteger, nullable=True, comment='逻辑删除标志，0表示未删除，1表示已删除', default=0)
    created_at = Column(DateTime, nullable=True, comment='创建时间', default=datetime.now)
    updated_at = Column(DateTime, nullable=True, comment='更新时间', default=datetime.now, onupdate=datetime.now)



