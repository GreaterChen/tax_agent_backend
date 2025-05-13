from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.package_dao import PackageDao
from module_admin.entity.vo.package_vo import DeletePackageModel, PackageModel, PackagePageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class PackageService:
    """
    package模块服务层
    """

    @classmethod
    async def get_package_list_services(
        cls, query_db: AsyncSession, query_object: PackagePageQueryModel, is_page: bool = False
    ):
        """
        获取package列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: package列表信息对象
        """
        package_list_result = await PackageDao.get_package_list(query_db, query_object, is_page)

        return package_list_result


    @classmethod
    async def add_package_services(cls, query_db: AsyncSession, page_object: PackageModel):
        """
        新增package信息service

        :param query_db: orm对象
        :param page_object: 新增package对象
        :return: 新增package校验结果
        """
        try:
            await PackageDao.add_package_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_package_services(cls, query_db: AsyncSession, page_object: PackageModel):
        """
        编辑package信息service

        :param query_db: orm对象
        :param page_object: 编辑package对象
        :return: 编辑package校验结果
        """
        edit_package = page_object.model_dump(exclude_unset=True, exclude={'create_time', })
        package_info = await cls.package_detail_services(query_db, page_object.id)
        if package_info.id:
            try:
                await PackageDao.edit_package_dao(query_db, edit_package)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='package不存在')

    @classmethod
    async def delete_package_services(cls, query_db: AsyncSession, page_object: DeletePackageModel):
        """
        删除package信息service

        :param query_db: orm对象
        :param page_object: 删除package对象
        :return: 删除package校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await PackageDao.delete_package_dao(query_db, PackageModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入ID为空')

    @classmethod
    async def package_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取package详细信息service

        :param query_db: orm对象
        :param id: ID
        :return: ID对应的信息
        """
        package = await PackageDao.get_package_detail_by_id(query_db, id=id)
        if package:
            result = PackageModel(**CamelCaseUtil.transform_result(package))
        else:
            result = PackageModel(**dict())

        return result

    @staticmethod
    async def export_package_list_services(package_list: List):
        """
        导出package信息service

        :param package_list: package信息列表
        :return: package信息对应excel的二进制数据
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
        binary_data = ExcelUtil.export_list2excel(package_list, mapping_dict)

        return binary_data
