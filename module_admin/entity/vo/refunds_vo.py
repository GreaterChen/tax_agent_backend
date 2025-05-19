from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class RefundsModel(BaseModel):
    """
    退款表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='退款ID')
    payment_id: Optional[int] = Field(default=None, description='订单ID')
    user_id: Optional[int] = Field(default=None, description='用户ID')
    product_id: Optional[int] = Field(default=None, description='产品ID')
    product_name: Optional[str] = Field(default=None, description='产品名称')
    refund_amount: Optional[Decimal] = Field(default=None, description='退款金额')
    refund_currency: Optional[str] = Field(default=None, description='退款币种(CNY/HKD)')
    status: Optional[str] = Field(default=None, description='退款状态(PENDING/APPROVED/REJECTED/COMPLETED)')
    reason: Optional[str] = Field(default=None, description='退款原因')
    admin_remark: Optional[str] = Field(default=None, description='管理员备注')
    approved: Optional[int] = Field(default=None, description='是否审核通过')
    approved_time: Optional[datetime] = Field(default=None, description='审核时间')
    approved_by: Optional[str] = Field(default=None, description='审核人')
    completed_time: Optional[datetime] = Field(default=None, description='退款完成时间')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='payment_id', message='订单ID不能为空')
    def get_payment_id(self):
        return self.payment_id

    @NotBlank(field_name='user_id', message='用户ID不能为空')
    def get_user_id(self):
        return self.user_id

    @NotBlank(field_name='product_id', message='产品ID不能为空')
    def get_product_id(self):
        return self.product_id

    @NotBlank(field_name='product_name', message='产品名称不能为空')
    def get_product_name(self):
        return self.product_name

    @NotBlank(field_name='refund_amount', message='退款金额不能为空')
    def get_refund_amount(self):
        return self.refund_amount

    @NotBlank(field_name='refund_currency', message='退款币种(CNY/HKD)不能为空')
    def get_refund_currency(self):
        return self.refund_currency

    @NotBlank(field_name='status', message='退款状态(PENDING/APPROVED/REJECTED/COMPLETED)不能为空')
    def get_status(self):
        return self.status

    @NotBlank(field_name='reason', message='退款原因不能为空')
    def get_reason(self):
        return self.reason


    def validate_fields(self):
        self.get_payment_id()
        self.get_user_id()
        self.get_product_id()
        self.get_product_name()
        self.get_refund_amount()
        self.get_refund_currency()
        self.get_status()
        self.get_reason()




class RefundsQueryModel(RefundsModel):
    """
    退款不分页查询模型
    """
    pass


@as_query
class RefundsPageQueryModel(RefundsQueryModel):
    """
    退款分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteRefundsModel(BaseModel):
    """
    删除退款模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的退款ID')
