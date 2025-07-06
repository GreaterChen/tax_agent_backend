from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.custom_ai_package_dao import Custom_ai_packageDao
from module_admin.entity.vo.custom_ai_package_vo import DeleteCustom_ai_packageModel, Custom_ai_packageModel, Custom_ai_packagePageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Custom_ai_packageService:
    """
    用户套餐情况模块服务层
    """

    @classmethod
    async def get_custom_ai_package_list_services(
        cls, query_db: AsyncSession, query_object: Custom_ai_packagePageQueryModel, is_page: bool = False
    ):
        """
        获取用户套餐情况列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 用户套餐情况列表信息对象
        """
        custom_ai_package_list_result = await Custom_ai_packageDao.get_custom_ai_package_list(query_db, query_object, is_page)

        return custom_ai_package_list_result


    @classmethod
    async def add_custom_ai_package_services(cls, query_db: AsyncSession, page_object: Custom_ai_packageModel):
        """
        新增用户套餐情况信息service

        :param query_db: orm对象
        :param page_object: 新增用户套餐情况对象
        :return: 新增用户套餐情况校验结果
        """
        try:
            await Custom_ai_packageDao.add_custom_ai_package_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_custom_ai_package_services(cls, query_db: AsyncSession, page_object: Custom_ai_packageModel):
        """
        编辑用户套餐情况信息service

        :param query_db: orm对象
        :param page_object: 编辑用户套餐情况对象
        :return: 编辑用户套餐情况校验结果
        """
        edit_custom_ai_package = page_object.model_dump(exclude_unset=True, exclude={'create_time', })
        custom_ai_package_info = await cls.custom_ai_package_detail_services(query_db, page_object.id)
        if custom_ai_package_info.id:
            try:
                await Custom_ai_packageDao.edit_custom_ai_package_dao(query_db, edit_custom_ai_package)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='用户套餐情况不存在')

    @classmethod
    async def delete_custom_ai_package_services(cls, query_db: AsyncSession, page_object: DeleteCustom_ai_packageModel):
        """
        删除用户套餐情况信息service

        :param query_db: orm对象
        :param page_object: 删除用户套餐情况对象
        :return: 删除用户套餐情况校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await Custom_ai_packageDao.delete_custom_ai_package_dao(query_db, Custom_ai_packageModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入ID为空')

    @classmethod
    async def custom_ai_package_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取用户套餐情况详细信息service

        :param query_db: orm对象
        :param id: ID
        :return: ID对应的信息
        """
        custom_ai_package = await Custom_ai_packageDao.get_custom_ai_package_detail_by_id(query_db, id=id)
        if custom_ai_package:
            result = Custom_ai_packageModel(**CamelCaseUtil.transform_result(custom_ai_package))
        else:
            result = Custom_ai_packageModel(**dict())

        return result

    @staticmethod
    async def export_custom_ai_package_list_services(custom_ai_package_list: List):
        """
        导出用户套餐情况信息service

        :param custom_ai_package_list: 用户套餐情况信息列表
        :return: 用户套餐情况信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': 'ID',
            'userId': '用户ID',
            'totalBalance': '总额度',
            'usedBalance': '已使用额度',
            'packageType': '套餐类型',
            'expireTime': '套餐过期时间',
            'createTime': '创建时间',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(custom_ai_package_list, mapping_dict)

        return binary_data
