from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.package_do import CustomAiPackage
from module_admin.entity.vo.package_vo import PackageModel, PackagePageQueryModel
from utils.page_util import PageUtil


class PackageDao:
    """
    package模块数据库操作层
    """

    @classmethod
    async def get_package_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据ID获取package详细信息

        :param db: orm对象
        :param id: ID
        :return: package信息对象
        """
        package_info = (
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

        return package_info

    @classmethod
    async def get_package_detail_by_info(cls, db: AsyncSession, package: PackageModel):
        """
        根据package参数获取package信息

        :param db: orm对象
        :param package: package参数对象
        :return: package信息对象
        """
        package_info = (
            (
                await db.execute(
                    select(CustomAiPackage).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return package_info

    @classmethod
    async def get_package_list(cls, db: AsyncSession, query_object: PackagePageQueryModel, is_page: bool = False):
        """
        根据查询参数获取package列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: package列表信息对象
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
        package_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return package_list

    @classmethod
    async def add_package_dao(cls, db: AsyncSession, package: PackageModel):
        """
        新增package数据库操作

        :param db: orm对象
        :param package: package对象
        :return:
        """
        db_package = CustomAiPackage(**package.model_dump(exclude={}))
        db.add(db_package)
        await db.flush()

        return db_package

    @classmethod
    async def edit_package_dao(cls, db: AsyncSession, package: dict):
        """
        编辑package数据库操作

        :param db: orm对象
        :param package: 需要更新的package字典
        :return:
        """
        await db.execute(update(CustomAiPackage), [package])

    @classmethod
    async def delete_package_dao(cls, db: AsyncSession, package: PackageModel):
        """
        删除package数据库操作

        :param db: orm对象
        :param package: package对象
        :return:
        """
        await db.execute(delete(CustomAiPackage).where(CustomAiPackage.id.in_([package.id])))

