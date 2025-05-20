from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.team_info_do import TeamInfo
from module_admin.entity.vo.team_info_vo import Team_infoModel, Team_infoPageQueryModel
from utils.page_util import PageUtil


class Team_infoDao:
    """
    团队信息模块数据库操作层
    """

    @classmethod
    async def get_team_info_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据团队成员ID获取团队信息详细信息

        :param db: orm对象
        :param id: 团队成员ID
        :return: 团队信息信息对象
        """
        team_info_info = (
            (
                await db.execute(
                    select(TeamInfo)
                    .where(
                        TeamInfo.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return team_info_info

    @classmethod
    async def get_team_info_detail_by_info(cls, db: AsyncSession, team_info: Team_infoModel):
        """
        根据团队信息参数获取团队信息信息

        :param db: orm对象
        :param team_info: 团队信息参数对象
        :return: 团队信息信息对象
        """
        team_info_info = (
            (
                await db.execute(
                    select(TeamInfo).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return team_info_info

    @classmethod
    async def get_team_info_list(cls, db: AsyncSession, query_object: Team_infoPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取团队信息列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 团队信息列表信息对象
        """
        query = (
            select(TeamInfo)
            .where(
                TeamInfo.img_url == query_object.img_url if query_object.img_url else True,
                TeamInfo.header_text == query_object.header_text if query_object.header_text else True,
                TeamInfo.name.like(f'%{query_object.name}%') if query_object.name else True,
                TeamInfo.desc_text1 == query_object.desc_text1 if query_object.desc_text1 else True,
                TeamInfo.desc_text2 == query_object.desc_text2 if query_object.desc_text2 else True,
                TeamInfo.sort == query_object.sort if query_object.sort else True,
                TeamInfo.status == query_object.status if query_object.status else True,
            )
            .order_by(TeamInfo.id)
            .distinct()
        )
        team_info_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return team_info_list

    @classmethod
    async def add_team_info_dao(cls, db: AsyncSession, team_info: Team_infoModel):
        """
        新增团队信息数据库操作

        :param db: orm对象
        :param team_info: 团队信息对象
        :return:
        """
        db_team_info = TeamInfo(**team_info.model_dump(exclude={}))
        db.add(db_team_info)
        await db.flush()

        return db_team_info

    @classmethod
    async def edit_team_info_dao(cls, db: AsyncSession, team_info: dict):
        """
        编辑团队信息数据库操作

        :param db: orm对象
        :param team_info: 需要更新的团队信息字典
        :return:
        """
        await db.execute(update(TeamInfo), [team_info])

    @classmethod
    async def delete_team_info_dao(cls, db: AsyncSession, team_info: Team_infoModel):
        """
        删除团队信息数据库操作

        :param db: orm对象
        :param team_info: 团队信息对象
        :return:
        """
        await db.execute(delete(TeamInfo).where(TeamInfo.id.in_([team_info.id])))

