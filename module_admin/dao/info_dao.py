from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.info_do import PracticalInfo
from module_admin.entity.vo.info_vo import InfoModel, InfoPageQueryModel
from utils.page_util import PageUtil


class InfoDao:
    """
    system模块数据库操作层
    """

    @classmethod
    async def get_info_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据主键ID获取system详细信息

        :param db: orm对象
        :param id: 主键ID
        :return: system信息对象
        """
        info_info = (
            (
                await db.execute(
                    select(PracticalInfo)
                    .where(
                        PracticalInfo.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return info_info

    @classmethod
    async def get_info_detail_by_info(cls, db: AsyncSession, info: InfoModel):
        """
        根据system参数获取system信息

        :param db: orm对象
        :param info: system参数对象
        :return: system信息对象
        """
        info_info = (
            (
                await db.execute(
                    select(PracticalInfo).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return info_info

    @classmethod
    async def get_info_list(cls, db: AsyncSession, query_object: InfoPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取system列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: system列表信息对象
        """
        query = (
            select(PracticalInfo)
            .where(
                PracticalInfo.md_content == query_object.md_content if query_object.md_content else True,
                PracticalInfo.language == query_object.language if query_object.language else True,
                PracticalInfo.is_deleted == query_object.is_deleted if query_object.is_deleted else True,
                PracticalInfo.created_at == query_object.created_at if query_object.created_at else True,
                PracticalInfo.updated_at == query_object.updated_at if query_object.updated_at else True,
            )
            .order_by(PracticalInfo.id)
            .distinct()
        )
        info_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return info_list

    @classmethod
    async def add_info_dao(cls, db: AsyncSession, info: InfoModel):
        """
        新增system数据库操作

        :param db: orm对象
        :param info: system对象
        :return:
        """
        db_info = PracticalInfo(**info.model_dump(exclude={}))
        db.add(db_info)
        await db.flush()

        return db_info

    @classmethod
    async def edit_info_dao(cls, db: AsyncSession, info: dict):
        """
        编辑system数据库操作

        :param db: orm对象
        :param info: 需要更新的system字典
        :return:
        """
        await db.execute(update(PracticalInfo), [info])

    @classmethod
    async def delete_info_dao(cls, db: AsyncSession, info: InfoModel):
        """
        删除system数据库操作

        :param db: orm对象
        :param info: system对象
        :return:
        """
        await db.execute(delete(PracticalInfo).where(PracticalInfo.id.in_([info.id])))

