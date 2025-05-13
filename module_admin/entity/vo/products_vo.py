from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class ProductsModel(BaseModel):
    """
    products表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='')
    name: Optional[str] = Field(default=None, description='')
    cover_img: Optional[str] = Field(default=None, description='')
    price_cny: Optional[Decimal] = Field(default=None, description='')
    type: Optional[str] = Field(default=None, description='')
    ai_balance: Optional[int] = Field(default=None, description='')
    price_hkd: Optional[Decimal] = Field(default=None, description='')
    introduction: Optional[str] = Field(default=None, description='')
    expiry: Optional[int] = Field(default=None, description='')
    is_deleted: Optional[int] = Field(default=None, description='')
    created_at: Optional[datetime] = Field(default=None, description='')
    updated_at: Optional[datetime] = Field(default=None, description='')






class ProductsQueryModel(ProductsModel):
    """
    products不分页查询模型
    """
    pass


@as_query
class ProductsPageQueryModel(ProductsQueryModel):
    """
    products分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteProductsModel(BaseModel):
    """
    删除products模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的')
