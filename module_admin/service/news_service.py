from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.news_dao import NewsDao
from module_admin.entity.vo.news_vo import DeleteNewsModel, NewsModel, NewsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class NewsService:
    """
    news模块服务层
    """

    @classmethod
    async def get_news_list_services(
        cls, query_db: AsyncSession, query_object: NewsPageQueryModel, is_page: bool = False
    ):
        """
        获取news列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: news列表信息对象
        """
        news_list_result = await NewsDao.get_news_list(query_db, query_object, is_page)

        return news_list_result


    @classmethod
    async def add_news_services(cls, query_db: AsyncSession, page_object: NewsModel):
        """
        新增news信息service

        :param query_db: orm对象
        :param page_object: 新增news对象
        :return: 新增news校验结果
        """
        try:
            await NewsDao.add_news_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_news_services(cls, query_db: AsyncSession, page_object: NewsModel):
        """
        编辑news信息service

        :param query_db: orm对象
        :param page_object: 编辑news对象
        :return: 编辑news校验结果
        """
        edit_news = page_object.model_dump(exclude_unset=True, exclude={})
        news_info = await cls.news_detail_services(query_db, page_object.id)
        if news_info.id:
            try:
                await NewsDao.edit_news_dao(query_db, edit_news)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='news不存在')

    @classmethod
    async def delete_news_services(cls, query_db: AsyncSession, page_object: DeleteNewsModel):
        """
        删除news信息service

        :param query_db: orm对象
        :param page_object: 删除news对象
        :return: 删除news校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await NewsDao.delete_news_dao(query_db, NewsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入为空')

    @classmethod
    async def news_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取news详细信息service

        :param query_db: orm对象
        :param id: 
        :return: 对应的信息
        """
        news = await NewsDao.get_news_detail_by_id(query_db, id=id)
        if news:
            result = NewsModel(**CamelCaseUtil.transform_result(news))
        else:
            result = NewsModel(**dict())

        return result

    @staticmethod
    async def export_news_list_services(news_list: List):
        """
        导出news信息service

        :param news_list: news信息列表
        :return: news信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '',
            'language': '',
            'source': '',
            'date': '',
            'content': '',
            'url': '',
            'createdAt': '',
            'title': '',
            'newsType': '新闻类别',
        }
        binary_data = ExcelUtil.export_list2excel(news_list, mapping_dict)

        return binary_data
