from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.products_do import Products
from module_admin.entity.vo.products_vo import ProductsModel, ProductsPageQueryModel
from utils.page_util import PageUtil


class ProductsDao:
    """
    products模块数据库操作层
    """

    @classmethod
    async def get_products_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据获取products详细信息

        :param db: orm对象
        :param id: 
        :return: products信息对象
        """
        products_info = (
            (
                await db.execute(
                    select(Products)
                    .where(
                        Products.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return products_info

    @classmethod
    async def get_products_detail_by_info(cls, db: AsyncSession, products: ProductsModel):
        """
        根据products参数获取products信息

        :param db: orm对象
        :param products: products参数对象
        :return: products信息对象
        """
        products_info = (
            (
                await db.execute(
                    select(Products).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return products_info

    @classmethod
    async def get_products_list(cls, db: AsyncSession, query_object: ProductsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取products列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: products列表信息对象
        """
        query = (
            select(Products)
            .where(
                Products.name.like(f'%{query_object.name}%') if query_object.name else True,
                Products.cover_img == query_object.cover_img if query_object.cover_img else True,
                Products.price_cny == query_object.price_cny if query_object.price_cny else True,
                Products.type == query_object.type if query_object.type else True,
                Products.ai_balance == query_object.ai_balance if query_object.ai_balance else True,
                Products.price_hkd == query_object.price_hkd if query_object.price_hkd else True,
                Products.introduction == query_object.introduction if query_object.introduction else True,
                Products.expiry == query_object.expiry if query_object.expiry else True,
                Products.language == query_object.language if query_object.language else True,
                Products.is_deleted == query_object.is_deleted if query_object.is_deleted else True,
                Products.created_at == query_object.created_at if query_object.created_at else True,
                Products.updated_at == query_object.updated_at if query_object.updated_at else True,
            )
            .order_by(Products.id)
            .distinct()
        )
        products_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return products_list

    @classmethod
    async def add_products_dao(cls, db: AsyncSession, products: ProductsModel):
        """
        新增products数据库操作

        :param db: orm对象
        :param products: products对象
        :return:
        """
        db_products = Products(**products.model_dump(exclude={}))
        db.add(db_products)
        await db.flush()

        return db_products

    @classmethod
    async def edit_products_dao(cls, db: AsyncSession, products: dict):
        """
        编辑products数据库操作

        :param db: orm对象
        :param products: 需要更新的products字典
        :return:
        """
        await db.execute(update(Products), [products])

    @classmethod
    async def delete_products_dao(cls, db: AsyncSession, products: ProductsModel):
        """
        删除products数据库操作

        :param db: orm对象
        :param products: products对象
        :return:
        """
        await db.execute(delete(Products).where(Products.id.in_([products.id])))

