from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class PaymentsModel(BaseModel):
    """
    支付订单表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='订单ID')
    user_id: Optional[int] = Field(default=None, description='用户ID')
    product_id: Optional[int] = Field(default=None, description='产品ID')
    product_name: Optional[str] = Field(default=None, description='产品名称')
    pay_price: Optional[Decimal] = Field(default=None, description='支付金额')
    pay_count: Optional[int] = Field(default=None, description='购买数量')
    pay_currency: Optional[str] = Field(default=None, description='支付币种(CNY/HKD)')
    status: Optional[str] = Field(default=None, description='订单状态(CREATED/PAID/REFUNDED/CANCELLED/FULFILLED/REFUNDING)')
    pay_time: Optional[datetime] = Field(default=None, description='支付时间')
    refund_time: Optional[datetime] = Field(default=None, description='退款时间')
    remark: Optional[str] = Field(default=None, description='备注')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='user_id', message='用户ID不能为空')
    def get_user_id(self):
        return self.user_id

    @NotBlank(field_name='product_id', message='产品ID不能为空')
    def get_product_id(self):
        return self.product_id

    @NotBlank(field_name='product_name', message='产品名称不能为空')
    def get_product_name(self):
        return self.product_name

    @NotBlank(field_name='pay_price', message='支付金额不能为空')
    def get_pay_price(self):
        return self.pay_price

    @NotBlank(field_name='pay_count', message='购买数量不能为空')
    def get_pay_count(self):
        return self.pay_count

    @NotBlank(field_name='pay_currency', message='支付币种(CNY/HKD)不能为空')
    def get_pay_currency(self):
        return self.pay_currency

    @NotBlank(field_name='status', message='订单状态(CREATED/PAID/REFUNDED/CANCELLED/FULFILLED/REFUNDING)不能为空')
    def get_status(self):
        return self.status

    @NotBlank(field_name='pay_time', message='支付时间不能为空')
    def get_pay_time(self):
        return self.pay_time


    def validate_fields(self):
        self.get_user_id()
        self.get_product_id()
        self.get_product_name()
        self.get_pay_price()
        self.get_pay_count()
        self.get_pay_currency()
        self.get_status()
        self.get_pay_time()




class PaymentsQueryModel(PaymentsModel):
    """
    支付订单不分页查询模型
    """
    pass


@as_query
class PaymentsPageQueryModel(PaymentsQueryModel):
    """
    支付订单分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeletePaymentsModel(BaseModel):
    """
    删除支付订单模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的订单ID')
