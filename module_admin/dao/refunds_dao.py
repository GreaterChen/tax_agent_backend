from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.refunds_do import Refunds
from module_admin.entity.vo.refunds_vo import RefundsModel, RefundsPageQueryModel, RefundAuditModel
from utils.page_util import PageUtil
from datetime import datetime


class RefundsDao:
    """
    退款模块数据库操作层
    """

    @classmethod
    async def get_refunds_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据退款ID获取退款详细信息

        :param db: orm对象
        :param id: 退款ID
        :return: 退款信息对象
        """
        refunds_info = (
            (
                await db.execute(
                    select(Refunds)
                    .where(
                        Refunds.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return refunds_info

    @classmethod
    async def get_refunds_detail_by_info(cls, db: AsyncSession, refunds: RefundsModel):
        """
        根据退款参数获取退款信息

        :param db: orm对象
        :param refunds: 退款参数对象
        :return: 退款信息对象
        """
        refunds_info = (
            (
                await db.execute(
                    select(Refunds).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return refunds_info

    @classmethod
    async def get_refunds_list(cls, db: AsyncSession, query_object: RefundsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取退款列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 退款列表信息对象
        """
        query = (
            select(Refunds)
            .where(
                Refunds.payment_id == query_object.payment_id if query_object.payment_id else True,
                Refunds.user_id == query_object.user_id if query_object.user_id else True,
                Refunds.product_id == query_object.product_id if query_object.product_id else True,
                Refunds.product_name.like(f'%{query_object.product_name}%') if query_object.product_name else True,
                Refunds.refund_amount == query_object.refund_amount if query_object.refund_amount else True,
                Refunds.refund_currency == query_object.refund_currency if query_object.refund_currency else True,
                Refunds.status == query_object.status if query_object.status else True,
                Refunds.reason == query_object.reason if query_object.reason else True,
                Refunds.admin_remark == query_object.admin_remark if query_object.admin_remark else True,
                Refunds.approved == query_object.approved if query_object.approved else True,
                Refunds.approved_time == query_object.approved_time if query_object.approved_time else True,
                Refunds.approved_by == query_object.approved_by if query_object.approved_by else True,
                Refunds.completed_time == query_object.completed_time if query_object.completed_time else True,
            )
            .order_by(Refunds.id)
            .distinct()
        )
        refunds_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return refunds_list

    @classmethod
    async def add_refunds_dao(cls, db: AsyncSession, refunds: RefundsModel):
        """
        新增退款数据库操作

        :param db: orm对象
        :param refunds: 退款对象
        :return:
        """
        db_refunds = Refunds(**refunds.model_dump(exclude={}))
        db.add(db_refunds)
        await db.flush()

        return db_refunds

    @classmethod
    async def edit_refunds_dao(cls, db: AsyncSession, refunds: dict):
        """
        编辑退款数据库操作

        :param db: orm对象
        :param refunds: 需要更新的退款字典
        :return:
        """
        await db.execute(update(Refunds), [refunds])

    @classmethod
    async def delete_refunds_dao(cls, db: AsyncSession, refunds: RefundsModel):
        """
        删除退款数据库操作

        :param db: orm对象
        :param refunds: 退款对象
        :return:
        """
        await db.execute(delete(Refunds).where(Refunds.id.in_([refunds.id])))

    @classmethod
    async def audit_refunds_dao(cls, db: AsyncSession, refund_audit: RefundAuditModel, username: str):
        """
        审核退款数据库操作

        :param db: orm对象
        :param refund_audit: 退款审核对象
        :param username: 审核人用户名
        :return: 更新后的退款对象
        """
        # 获取退款信息
        refund = await cls.get_refunds_detail_by_id(db, refund_audit.id)
        
        if not refund:
            return None
            
        # 更新退款状态
        if refund_audit.confirm:
            status = "APPROVED"
            approved = 1
        else:
            status = "REJECTED"
            approved = 0
            
        # 更新退款表
        update_data = {
            "id": refund_audit.id,
            "refund_amount": refund_audit.refund_amount,
            "status": status,
            "admin_remark": refund_audit.confirm_reason,
            "approved": approved,
            "approved_time": datetime.now(),
            "approved_by": username
        }
        
        await cls.edit_refunds_dao(db, update_data)
        
        # 返回更新后的退款对象
        return await cls.get_refunds_detail_by_id(db, refund_audit.id)

