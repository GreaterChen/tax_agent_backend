from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class PackageModel(BaseModel):
    """
    package表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='ID')
    user_id: Optional[int] = Field(default=None, description='用户ID')
    total_balance: Optional[int] = Field(default=None, description='总额度')
    used_balance: Optional[int] = Field(default=None, description='已使用额度')
    package_type: Optional[str] = Field(default=None, description='套餐类型')
    expire_time: Optional[datetime] = Field(default=None, description='套餐过期时间')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='user_id', message='用户ID不能为空')
    def get_user_id(self):
        return self.user_id

    @NotBlank(field_name='total_balance', message='总额度不能为空')
    def get_total_balance(self):
        return self.total_balance

    @NotBlank(field_name='used_balance', message='已使用额度不能为空')
    def get_used_balance(self):
        return self.used_balance


    def validate_fields(self):
        self.get_user_id()
        self.get_total_balance()
        self.get_used_balance()




class PackageQueryModel(PackageModel):
    """
    package不分页查询模型
    """
    pass


@as_query
class PackagePageQueryModel(PackageQueryModel):
    """
    package分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeletePackageModel(BaseModel):
    """
    删除package模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的ID')
