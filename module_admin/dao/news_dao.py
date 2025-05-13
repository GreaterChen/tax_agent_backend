from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.news_do import News
from module_admin.entity.vo.news_vo import NewsModel, NewsPageQueryModel
from utils.page_util import PageUtil


class NewsDao:
    """
    news模块数据库操作层
    """

    @classmethod
    async def get_news_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据获取news详细信息

        :param db: orm对象
        :param id: 
        :return: news信息对象
        """
        news_info = (
            (
                await db.execute(
                    select(News)
                    .where(
                        News.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return news_info

    @classmethod
    async def get_news_detail_by_info(cls, db: AsyncSession, news: NewsModel):
        """
        根据news参数获取news信息

        :param db: orm对象
        :param news: news参数对象
        :return: news信息对象
        """
        news_info = (
            (
                await db.execute(
                    select(News).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return news_info

    @classmethod
    async def get_news_list(cls, db: AsyncSession, query_object: NewsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取news列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: news列表信息对象
        """
        query = (
            select(News)
            .where(
                News.language == query_object.language if query_object.language else True,
                News.source == query_object.source if query_object.source else True,
                News.date == query_object.date if query_object.date else True,
                News.content == query_object.content if query_object.content else True,
                News.url == query_object.url if query_object.url else True,
                News.created_at == query_object.created_at if query_object.created_at else True,
                News.title == query_object.title if query_object.title else True,
            )
            .order_by(News.id)
            .distinct()
        )
        news_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return news_list

    @classmethod
    async def add_news_dao(cls, db: AsyncSession, news: NewsModel):
        """
        新增news数据库操作

        :param db: orm对象
        :param news: news对象
        :return:
        """
        db_news = News(**news.model_dump(exclude={}))
        db.add(db_news)
        await db.flush()

        return db_news

    @classmethod
    async def edit_news_dao(cls, db: AsyncSession, news: dict):
        """
        编辑news数据库操作

        :param db: orm对象
        :param news: 需要更新的news字典
        :return:
        """
        await db.execute(update(News), [news])

    @classmethod
    async def delete_news_dao(cls, db: AsyncSession, news: NewsModel):
        """
        删除news数据库操作

        :param db: orm对象
        :param news: news对象
        :return:
        """
        await db.execute(delete(News).where(News.id.in_([news.id])))

