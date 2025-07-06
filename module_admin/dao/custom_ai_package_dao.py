from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.custom_ai_package_do import CustomAiPackage
from module_admin.entity.vo.custom_ai_package_vo import Custom_ai_packageModel, Custom_ai_packagePageQueryModel
from utils.page_util import PageUtil


class Custom_ai_packageDao:
    """
    用户套餐情况模块数据库操作层
    """

    @classmethod
    async def get_custom_ai_package_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据ID获取用户套餐情况详细信息

        :param db: orm对象
        :param id: ID
        :return: 用户套餐情况信息对象
        """
        custom_ai_package_info = (
            (
                await db.execute(
                    select(CustomAiPackage)
                    .where(
                        CustomAiPackage.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return custom_ai_package_info

    @classmethod
    async def get_custom_ai_package_detail_by_info(cls, db: AsyncSession, custom_ai_package: Custom_ai_packageModel):
        """
        根据用户套餐情况参数获取用户套餐情况信息

        :param db: orm对象
        :param custom_ai_package: 用户套餐情况参数对象
        :return: 用户套餐情况信息对象
        """
        custom_ai_package_info = (
            (
                await db.execute(
                    select(CustomAiPackage).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return custom_ai_package_info

    @classmethod
    async def get_custom_ai_package_list(cls, db: AsyncSession, query_object: Custom_ai_packagePageQueryModel, is_page: bool = False):
        """
        根据查询参数获取用户套餐情况列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 用户套餐情况列表信息对象
        """
        query = (
            select(CustomAiPackage)
            .where(
                CustomAiPackage.user_id == query_object.user_id if query_object.user_id else True,
                CustomAiPackage.total_balance == query_object.total_balance if query_object.total_balance else True,
                CustomAiPackage.used_balance == query_object.used_balance if query_object.used_balance else True,
                CustomAiPackage.package_type == query_object.package_type if query_object.package_type else True,
                CustomAiPackage.expire_time == query_object.expire_time if query_object.expire_time else True,
            )
            .order_by(CustomAiPackage.id)
            .distinct()
        )
        custom_ai_package_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return custom_ai_package_list

    @classmethod
    async def add_custom_ai_package_dao(cls, db: AsyncSession, custom_ai_package: Custom_ai_packageModel):
        """
        新增用户套餐情况数据库操作

        :param db: orm对象
        :param custom_ai_package: 用户套餐情况对象
        :return:
        """
        db_custom_ai_package = CustomAiPackage(**custom_ai_package.model_dump(exclude={}))
        db.add(db_custom_ai_package)
        await db.flush()

        return db_custom_ai_package

    @classmethod
    async def edit_custom_ai_package_dao(cls, db: AsyncSession, custom_ai_package: dict):
        """
        编辑用户套餐情况数据库操作

        :param db: orm对象
        :param custom_ai_package: 需要更新的用户套餐情况字典
        :return:
        """
        await db.execute(update(CustomAiPackage), [custom_ai_package])

    @classmethod
    async def delete_custom_ai_package_dao(cls, db: AsyncSession, custom_ai_package: Custom_ai_packageModel):
        """
        删除用户套餐情况数据库操作

        :param db: orm对象
        :param custom_ai_package: 用户套餐情况对象
        :return:
        """
        await db.execute(delete(CustomAiPackage).where(CustomAiPackage.id.in_([custom_ai_package.id])))

