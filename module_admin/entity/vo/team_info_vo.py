from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class Team_infoModel(BaseModel):
    """
    团队信息表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='团队成员ID')
    img_url: Optional[str] = Field(default=None, description='图片外链')
    header_text: Optional[str] = Field(default=None, description='头部文本')
    name: Optional[str] = Field(default=None, description='成员名字')
    desc_text1: Optional[str] = Field(default=None, description='描述文本1')
    desc_text2: Optional[str] = Field(default=None, description='描述文本2')
    language: Optional[str] = Field(default=None, description='语言')
    sort: Optional[int] = Field(default=None, description='排序')
    status: Optional[str] = Field(default=None, description='状态（0正常 1停用）')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='img_url', message='图片外链不能为空')
    def get_img_url(self):
        return self.img_url

    @NotBlank(field_name='header_text', message='头部文本不能为空')
    def get_header_text(self):
        return self.header_text

    @NotBlank(field_name='name', message='成员名字不能为空')
    def get_name(self):
        return self.name

    @NotBlank(field_name='desc_text1', message='描述文本1不能为空')
    def get_desc_text1(self):
        return self.desc_text1

    @NotBlank(field_name='desc_text2', message='描述文本2不能为空')
    def get_desc_text2(self):
        return self.desc_text2


    def validate_fields(self):
        self.get_img_url()
        self.get_header_text()
        self.get_name()
        self.get_desc_text1()
        self.get_desc_text2()




class Team_infoQueryModel(Team_infoModel):
    """
    团队信息不分页查询模型
    """
    pass


@as_query
class Team_infoPageQueryModel(Team_infoQueryModel):
    """
    团队信息分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteTeam_infoModel(BaseModel):
    """
    删除团队信息模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的团队成员ID')
