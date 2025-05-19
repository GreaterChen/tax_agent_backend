from sqlalchemy import String, Column, Integer, SmallInteger, DECIMAL, DateTime
from config.database import Base


class Refunds(Base):
    """
    退款表
    """

    __tablename__ = 'refunds'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='退款ID')
    payment_id = Column(Integer, nullable=False, comment='订单ID')
    user_id = Column(Integer, nullable=False, comment='用户ID')
    product_id = Column(Integer, nullable=False, comment='产品ID')
    product_name = Column(String(100), nullable=False, comment='产品名称')
    refund_amount = Column(DECIMAL, nullable=False, comment='退款金额')
    refund_currency = Column(String(10), nullable=False, comment='退款币种(CNY/HKD)')
    status = Column(String(20), nullable=False, comment='退款状态(PENDING/APPROVED/REJECTED/COMPLETED)')
    reason = Column(String(500), nullable=False, comment='退款原因')
    admin_remark = Column(String(500), nullable=True, comment='管理员备注')
    approved = Column(SmallInteger, nullable=True, comment='是否审核通过')
    approved_time = Column(DateTime, nullable=True, comment='审核时间')
    approved_by = Column(String(64), nullable=True, comment='审核人')
    completed_time = Column(DateTime, nullable=True, comment='退款完成时间')
    create_by = Column(String(64), nullable=True, comment='创建者')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(64), nullable=True, comment='更新者')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



