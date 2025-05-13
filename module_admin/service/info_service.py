from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.info_dao import InfoDao
from module_admin.entity.vo.info_vo import DeleteInfoModel, InfoModel, InfoPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class InfoService:
    """
    实用信息模块服务层
    """

    @classmethod
    async def get_info_list_services(
        cls, query_db: AsyncSession, query_object: InfoPageQueryModel, is_page: bool = False
    ):
        """
        获取实用信息列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 实用信息列表信息对象
        """
        info_list_result = await InfoDao.get_info_list(query_db, query_object, is_page)

        return info_list_result


    @classmethod
    async def add_info_services(cls, query_db: AsyncSession, page_object: InfoModel):
        """
        新增实用信息信息service

        :param query_db: orm对象
        :param page_object: 新增实用信息对象
        :return: 新增实用信息校验结果
        """
        try:
            await InfoDao.add_info_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_info_services(cls, query_db: AsyncSession, page_object: InfoModel):
        """
        编辑实用信息信息service

        :param query_db: orm对象
        :param page_object: 编辑实用信息对象
        :return: 编辑实用信息校验结果
        """
        edit_info = page_object.model_dump(exclude_unset=True, exclude={})
        info_info = await cls.info_detail_services(query_db, page_object.id)
        if info_info.id:
            try:
                await InfoDao.edit_info_dao(query_db, edit_info)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='实用信息不存在')

    @classmethod
    async def delete_info_services(cls, query_db: AsyncSession, page_object: DeleteInfoModel):
        """
        删除实用信息信息service

        :param query_db: orm对象
        :param page_object: 删除实用信息对象
        :return: 删除实用信息校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await InfoDao.delete_info_dao(query_db, InfoModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键ID为空')

    @classmethod
    async def info_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取实用信息详细信息service

        :param query_db: orm对象
        :param id: 主键ID
        :return: 主键ID对应的信息
        """
        info = await InfoDao.get_info_detail_by_id(query_db, id=id)
        if info:
            result = InfoModel(**CamelCaseUtil.transform_result(info))
        else:
            result = InfoModel(**dict())

        return result

    @staticmethod
    async def export_info_list_services(info_list: List):
        """
        导出实用信息信息service

        :param info_list: 实用信息信息列表
        :return: 实用信息信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键ID',
            'mdContent': '实用信息的URL地址',
            'isDeleted': '逻辑删除标志，0表示未删除，1表示已删除',
            'createdAt': '创建时间',
            'updatedAt': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(info_list, mapping_dict)

        return binary_data
