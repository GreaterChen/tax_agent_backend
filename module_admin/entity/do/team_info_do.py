from sqlalchemy import Column, TIMESTAMP, Integer, String
from config.database import Base


class TeamInfo(Base):
    """
    团队信息表
    """

    __tablename__ = 'team_info'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='团队成员ID')
    img_url = Column(String(255), nullable=False, comment='图片外链')
    header_text = Column(String(100), nullable=False, comment='头部文本')
    name = Column(String(50), nullable=False, comment='成员名字')
    desc_text1 = Column(String(200), nullable=False, comment='描述文本1')
    desc_text2 = Column(String(200), nullable=False, comment='描述文本2')
    language = Column(String(10), nullable=True, comment='语言')
    sort = Column(Integer, nullable=True, comment='排序')
    status = Column(String(1), nullable=True, comment='状态（0正常 1停用）')
    create_by = Column(String(64), nullable=True, comment='创建者')
    create_time = Column(TIMESTAMP, nullable=True, comment='创建时间')
    update_by = Column(String(64), nullable=True, comment='更新者')
    update_time = Column(TIMESTAMP, nullable=True, comment='更新时间')



