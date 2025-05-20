from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.team_info_dao import Team_infoDao
from module_admin.entity.vo.team_info_vo import DeleteTeam_infoModel, Team_infoModel, Team_infoPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Team_infoService:
    """
    团队信息模块服务层
    """

    @classmethod
    async def get_team_info_list_services(
        cls, query_db: AsyncSession, query_object: Team_infoPageQueryModel, is_page: bool = False
    ):
        """
        获取团队信息列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 团队信息列表信息对象
        """
        team_info_list_result = await Team_infoDao.get_team_info_list(query_db, query_object, is_page)

        return team_info_list_result


    @classmethod
    async def add_team_info_services(cls, query_db: AsyncSession, page_object: Team_infoModel):
        """
        新增团队信息信息service

        :param query_db: orm对象
        :param page_object: 新增团队信息对象
        :return: 新增团队信息校验结果
        """
        try:
            await Team_infoDao.add_team_info_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_team_info_services(cls, query_db: AsyncSession, page_object: Team_infoModel):
        """
        编辑团队信息信息service

        :param query_db: orm对象
        :param page_object: 编辑团队信息对象
        :return: 编辑团队信息校验结果
        """
        edit_team_info = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', })
        team_info_info = await cls.team_info_detail_services(query_db, page_object.id)
        if team_info_info.id:
            try:
                await Team_infoDao.edit_team_info_dao(query_db, edit_team_info)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='团队信息不存在')

    @classmethod
    async def delete_team_info_services(cls, query_db: AsyncSession, page_object: DeleteTeam_infoModel):
        """
        删除团队信息信息service

        :param query_db: orm对象
        :param page_object: 删除团队信息对象
        :return: 删除团队信息校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await Team_infoDao.delete_team_info_dao(query_db, Team_infoModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入团队成员ID为空')

    @classmethod
    async def team_info_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取团队信息详细信息service

        :param query_db: orm对象
        :param id: 团队成员ID
        :return: 团队成员ID对应的信息
        """
        team_info = await Team_infoDao.get_team_info_detail_by_id(query_db, id=id)
        if team_info:
            result = Team_infoModel(**CamelCaseUtil.transform_result(team_info))
        else:
            result = Team_infoModel(**dict())

        return result

    @staticmethod
    async def export_team_info_list_services(team_info_list: List):
        """
        导出团队信息信息service

        :param team_info_list: 团队信息信息列表
        :return: 团队信息信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '团队成员ID',
            'imgUrl': '图片外链',
            'headerText': '头部文本',
            'name': '成员名字',
            'descText1': '描述文本1',
            'descText2': '描述文本2',
            'sort': '排序',
            'status': '状态',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(team_info_list, mapping_dict)

        return binary_data
