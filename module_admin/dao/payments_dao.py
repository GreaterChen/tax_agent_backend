from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.payments_do import Payments
from module_admin.entity.vo.payments_vo import PaymentsModel, PaymentsPageQueryModel
from utils.page_util import PageUtil


class PaymentsDao:
    """
    支付订单模块数据库操作层
    """

    @classmethod
    async def get_payments_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据订单ID获取支付订单详细信息

        :param db: orm对象
        :param id: 订单ID
        :return: 支付订单信息对象
        """
        payments_info = (
            (
                await db.execute(
                    select(Payments)
                    .where(
                        Payments.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return payments_info

    @classmethod
    async def get_payments_detail_by_info(cls, db: AsyncSession, payments: PaymentsModel):
        """
        根据支付订单参数获取支付订单信息

        :param db: orm对象
        :param payments: 支付订单参数对象
        :return: 支付订单信息对象
        """
        payments_info = (
            (
                await db.execute(
                    select(Payments).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return payments_info

    @classmethod
    async def get_payments_list(cls, db: AsyncSession, query_object: PaymentsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取支付订单列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 支付订单列表信息对象
        """
        query = (
            select(Payments)
            .where(
                Payments.user_id == query_object.user_id if query_object.user_id else True,
                Payments.product_id == query_object.product_id if query_object.product_id else True,
                Payments.product_name.like(f'%{query_object.product_name}%') if query_object.product_name else True,
                Payments.pay_price == query_object.pay_price if query_object.pay_price else True,
                Payments.pay_currency == query_object.pay_currency if query_object.pay_currency else True,
                Payments.status == query_object.status if query_object.status else True,
                Payments.pay_time == query_object.pay_time if query_object.pay_time else True,
                Payments.refund_time == query_object.refund_time if query_object.refund_time else True,
            )
            .order_by(Payments.id)
            .distinct()
        )
        payments_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return payments_list

    @classmethod
    async def add_payments_dao(cls, db: AsyncSession, payments: PaymentsModel):
        """
        新增支付订单数据库操作

        :param db: orm对象
        :param payments: 支付订单对象
        :return:
        """
        db_payments = Payments(**payments.model_dump(exclude={'id', }))
        db.add(db_payments)
        await db.flush()

        return db_payments

    @classmethod
    async def edit_payments_dao(cls, db: AsyncSession, payments: dict):
        """
        编辑支付订单数据库操作

        :param db: orm对象
        :param payments: 需要更新的支付订单字典
        :return:
        """
        await db.execute(update(Payments), [payments])

    @classmethod
    async def delete_payments_dao(cls, db: AsyncSession, payments: PaymentsModel):
        """
        删除支付订单数据库操作

        :param db: orm对象
        :param payments: 支付订单对象
        :return:
        """
        await db.execute(delete(Payments).where(Payments.id.in_([payments.id])))

