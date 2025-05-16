from sqlalchemy import DECIMAL, String, Column, Integer, DateTime
from config.database import Base


class Payments(Base):
    """
    支付订单表
    """

    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='订单ID')
    user_id = Column(Integer, nullable=False, comment='用户ID')
    product_id = Column(Integer, nullable=False, comment='产品ID')
    product_name = Column(String(100), nullable=False, comment='产品名称')
    pay_price = Column(DECIMAL, nullable=False, comment='支付金额')
    pay_count = Column(Integer, nullable=False, comment='购买数量')
    pay_currency = Column(String(10), nullable=False, comment='支付币种(CNY/HKD)')
    status = Column(String(20), nullable=False, comment='订单状态(CREATED/PAID/REFUNDED/CANCELLED/FULFILLED/REFUNDING)')
    pay_time = Column(DateTime, nullable=False, comment='支付时间')
    refund_time = Column(DateTime, nullable=True, comment='退款时间')
    remark = Column(String(500), nullable=True, comment='备注')
    create_by = Column(String(64), nullable=True, comment='创建者')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(64), nullable=True, comment='更新者')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



