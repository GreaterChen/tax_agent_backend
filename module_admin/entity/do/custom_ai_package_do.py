from sqlalchemy import BigInteger, Column, String, Integer, DateTime
from config.database import Base


class CustomAiPackage(Base):
    """
    用户套餐情况表
    """

    __tablename__ = 'custom_ai_package'

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='ID')
    user_id = Column(BigInteger, nullable=False, comment='用户ID')
    total_balance = Column(Integer, nullable=False, comment='总额度')
    used_balance = Column(Integer, nullable=False, comment='已使用额度')
    package_type = Column(String(20), nullable=True, comment='套餐类型')
    expire_time = Column(DateTime, nullable=True, comment='套餐过期时间')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



