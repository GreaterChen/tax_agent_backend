from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class InfoModel(BaseModel):
    """
    system表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='主键ID')
    md_content: Optional[str] = Field(default=None, description='实用信息的URL地址')
    is_deleted: Optional[int] = Field(default=None, description='逻辑删除标志，0表示未删除，1表示已删除')
    created_at: Optional[datetime] = Field(default=None, description='')
    updated_at: Optional[datetime] = Field(default=None, description='')

    @NotBlank(field_name='md_content', message='实用信息的URL地址不能为空')
    def get_md_content(self):
        return self.md_content


    def validate_fields(self):
        self.get_md_content()




class InfoQueryModel(InfoModel):
    """
    system不分页查询模型
    """
    pass


@as_query
class InfoPageQueryModel(InfoQueryModel):
    """
    system分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteInfoModel(BaseModel):
    """
    删除system模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的主键ID')
