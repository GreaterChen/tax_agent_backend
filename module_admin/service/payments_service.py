from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.service.dict_service import DictDataService
from module_admin.dao.payments_dao import PaymentsDao
from module_admin.entity.vo.payments_vo import DeletePaymentsModel, PaymentsModel, PaymentsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class PaymentsService:
    """
    支付订单模块服务层
    """

    @classmethod
    async def get_payments_list_services(
        cls, query_db: AsyncSession, query_object: PaymentsPageQueryModel, is_page: bool = False
    ):
        """
        获取支付订单列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 支付订单列表信息对象
        """
        payments_list_result = await PaymentsDao.get_payments_list(query_db, query_object, is_page)

        return payments_list_result


    @classmethod
    async def add_payments_services(cls, query_db: AsyncSession, page_object: PaymentsModel):
        """
        新增支付订单信息service

        :param query_db: orm对象
        :param page_object: 新增支付订单对象
        :return: 新增支付订单校验结果
        """
        try:
            await PaymentsDao.add_payments_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_payments_services(cls, query_db: AsyncSession, page_object: PaymentsModel):
        """
        编辑支付订单信息service

        :param query_db: orm对象
        :param page_object: 编辑支付订单对象
        :return: 编辑支付订单校验结果
        """
        edit_payments = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', })
        payments_info = await cls.payments_detail_services(query_db, page_object.id)
        if payments_info.id:
            try:
                await PaymentsDao.edit_payments_dao(query_db, edit_payments)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='支付订单不存在')

    @classmethod
    async def delete_payments_services(cls, query_db: AsyncSession, page_object: DeletePaymentsModel):
        """
        删除支付订单信息service

        :param query_db: orm对象
        :param page_object: 删除支付订单对象
        :return: 删除支付订单校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await PaymentsDao.delete_payments_dao(query_db, PaymentsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入订单ID为空')

    @classmethod
    async def payments_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取支付订单详细信息service

        :param query_db: orm对象
        :param id: 订单ID
        :return: 订单ID对应的信息
        """
        payments = await PaymentsDao.get_payments_detail_by_id(query_db, id=id)
        if payments:
            result = PaymentsModel(**CamelCaseUtil.transform_result(payments))
        else:
            result = PaymentsModel(**dict())

        return result

    @staticmethod
    async def export_payments_list_services(request: Request, payments_list: List):
        """
        导出支付订单信息service

        :param payments_list: 支付订单信息列表
        :return: 支付订单信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '订单ID',
            'userId': '用户ID',
            'productId': '产品ID',
            'productName': '产品名称',
            'payPrice': '支付金额',
            'payCount': '购买数量',
            'payCurrency': '支付币种(CNY/HKD)',
            'status': '订单状态(CREATED/PAID/REFUNDED/CANCELLED/FULFILLED/REFUNDING)',
            'payTime': '支付时间',
            'refundTime': '退款时间',
            'remark': '备注',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
        }
        order_status_list = await DictDataService.query_dict_data_list_from_cache_services(
            request.app.state.redis, dict_type='order_status'
        )
        order_status_option = [dict(label=item.get('dictLabel'), value=item.get('dictValue')) for item in order_status_list]
        order_status_option_dict = {item.get('value'): item for item in order_status_option}
        for item in payments_list:
            if str(item.get('status')) in order_status_option_dict.keys():
                item['status'] = order_status_option_dict.get(str(item.get('status'))).get('label')
        binary_data = ExcelUtil.export_list2excel(payments_list, mapping_dict)

        return binary_data
