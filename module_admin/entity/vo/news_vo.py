from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class NewsModel(BaseModel):
    """
    news表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='')
    language: Optional[str] = Field(default=None, description='')
    source: Optional[str] = Field(default=None, description='')
    date: Optional[str] = Field(default=None, description='')
    content: Optional[str] = Field(default=None, description='')
    url: Optional[str] = Field(default=None, description='')
    created_at: Optional[datetime] = Field(default=None, description='')
    title: Optional[str] = Field(default=None, description='')






class NewsQueryModel(NewsModel):
    """
    news不分页查询模型
    """
    pass


@as_query
class NewsPageQueryModel(NewsQueryModel):
    """
    news分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteNewsModel(BaseModel):
    """
    删除news模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的')
