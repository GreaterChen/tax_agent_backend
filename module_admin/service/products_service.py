from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.products_dao import ProductsDao
from module_admin.entity.vo.products_vo import DeleteProductsModel, ProductsModel, ProductsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class ProductsService:
    """
    products模块服务层
    """

    @classmethod
    async def get_products_list_services(
        cls, query_db: AsyncSession, query_object: ProductsPageQueryModel, is_page: bool = False
    ):
        """
        获取products列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: products列表信息对象
        """
        products_list_result = await ProductsDao.get_products_list(query_db, query_object, is_page)

        return products_list_result


    @classmethod
    async def add_products_services(cls, query_db: AsyncSession, page_object: ProductsModel):
        """
        新增products信息service

        :param query_db: orm对象
        :param page_object: 新增products对象
        :return: 新增products校验结果
        """
        try:
            await ProductsDao.add_products_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_products_services(cls, query_db: AsyncSession, page_object: ProductsModel):
        """
        编辑products信息service

        :param query_db: orm对象
        :param page_object: 编辑products对象
        :return: 编辑products校验结果
        """
        edit_products = page_object.model_dump(exclude_unset=True, exclude={})
        products_info = await cls.products_detail_services(query_db, page_object.id)
        if products_info.id:
            try:
                await ProductsDao.edit_products_dao(query_db, edit_products)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='products不存在')

    @classmethod
    async def delete_products_services(cls, query_db: AsyncSession, page_object: DeleteProductsModel):
        """
        删除products信息service

        :param query_db: orm对象
        :param page_object: 删除products对象
        :return: 删除products校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await ProductsDao.delete_products_dao(query_db, ProductsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入为空')

    @classmethod
    async def products_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取products详细信息service

        :param query_db: orm对象
        :param id: 
        :return: 对应的信息
        """
        products = await ProductsDao.get_products_detail_by_id(query_db, id=id)
        if products:
            result = ProductsModel(**CamelCaseUtil.transform_result(products))
        else:
            result = ProductsModel(**dict())

        return result

    @staticmethod
    async def export_products_list_services(products_list: List):
        """
        导出products信息service

        :param products_list: products信息列表
        :return: products信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '',
            'name': '',
            'coverImg': '',
            'priceCny': '',
            'type': '',
            'aiBalance': '',
            'priceHkd': '',
            'introduction': '',
            'expiry': '',
            'isDeleted': '',
            'createdAt': '',
            'updatedAt': '',
        }
        binary_data = ExcelUtil.export_list2excel(products_list, mapping_dict)

        return binary_data
