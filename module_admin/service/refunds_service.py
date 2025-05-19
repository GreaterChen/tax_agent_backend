from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime
from fastapi import Request
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.refunds_dao import RefundsDao
from module_admin.dao.payments_dao import PaymentsDao
from module_admin.dao.user_dao import UserDao
from module_admin.entity.vo.refunds_vo import DeleteRefundsModel, RefundsModel, RefundsPageQueryModel, RefundAuditModel
from module_admin.entity.vo.payments_vo import PaymentsModel
from module_admin.utils.email_service import EmailService
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class RefundsService:
    """
    退款模块服务层
    """

    @classmethod
    async def get_refunds_list_services(
        cls, query_db: AsyncSession, query_object: RefundsPageQueryModel, is_page: bool = False
    ):
        """
        获取退款列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 退款列表信息对象
        """
        refunds_list_result = await RefundsDao.get_refunds_list(query_db, query_object, is_page)

        return refunds_list_result


    @classmethod
    async def add_refunds_services(cls, query_db: AsyncSession, page_object: RefundsModel):
        """
        新增退款信息service

        :param query_db: orm对象
        :param page_object: 新增退款对象
        :return: 新增退款校验结果
        """
        try:
            await RefundsDao.add_refunds_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_refunds_services(cls, query_db: AsyncSession, page_object: RefundsModel):
        """
        编辑退款信息service

        :param query_db: orm对象
        :param page_object: 编辑退款对象
        :return: 编辑退款校验结果
        """
        edit_refunds = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', })
        refunds_info = await cls.refunds_detail_services(query_db, page_object.id)
        if refunds_info.id:
            try:
                await RefundsDao.edit_refunds_dao(query_db, edit_refunds)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='退款不存在')

    @classmethod
    async def delete_refunds_services(cls, query_db: AsyncSession, page_object: DeleteRefundsModel):
        """
        删除退款信息service

        :param query_db: orm对象
        :param page_object: 删除退款对象
        :return: 删除退款校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await RefundsDao.delete_refunds_dao(query_db, RefundsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入退款ID为空')

    @classmethod
    async def refunds_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取退款详细信息service

        :param query_db: orm对象
        :param id: 退款ID
        :return: 退款ID对应的信息
        """
        refunds = await RefundsDao.get_refunds_detail_by_id(query_db, id=id)
        if refunds:
            result = RefundsModel(**CamelCaseUtil.transform_result(refunds))
        else:
            result = RefundsModel(**dict())

        return result

    @staticmethod
    async def export_refunds_list_services(refunds_list: List):
        """
        导出退款信息service

        :param refunds_list: 退款信息列表
        :return: 退款信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '退款ID',
            'paymentId': '订单ID',
            'userId': '用户ID',
            'productId': '产品ID',
            'productName': '产品名称',
            'refundAmount': '退款金额',
            'refundCurrency': '退款币种(CNY/HKD)',
            'status': '退款状态(PENDING/APPROVED/REJECTED/COMPLETED)',
            'reason': '退款原因',
            'adminRemark': '管理员备注',
            'approved': '是否审核通过',
            'approvedTime': '审核时间',
            'approvedBy': '审核人',
            'completedTime': '退款完成时间',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(refunds_list, mapping_dict)

        return binary_data

    @classmethod
    async def audit_refunds_services(cls, request: Request, query_db: AsyncSession, refund_audit: RefundAuditModel, current_user_name: str):
        """
        审核退款信息service

        :param request: 请求对象
        :param query_db: orm对象
        :param refund_audit: 退款审核对象
        :param current_user_name: 当前用户名
        :return: 审核结果
        """
        try:
            # 验证退款ID是否存在
            refund_info = await cls.refunds_detail_services(query_db, refund_audit.id)
            if not refund_info.id:
                raise ServiceException(message='退款订单不存在')
                
            if refund_info.status != 'PENDING':
                raise ServiceException(message='该退款订单已审核，不能重复审核')
                
            # 执行退款审核
            refund_updated = await RefundsDao.audit_refunds_dao(query_db, refund_audit, current_user_name)
            if not refund_updated:
                raise ServiceException(message='审核失败，请重试')
                
            # 如果审核通过，更新支付订单状态为REFUNDED
            if refund_audit.confirm:
                # 获取关联的支付订单
                payment_id = refund_updated.payment_id
                # 获取支付订单信息
                payment_info = await PaymentsDao.get_payments_detail_by_id(query_db, payment_id)
                
                if payment_info:
                    # 更新支付订单状态为REFUNDED，更新退款时间
                    payment_update = {
                        "id": payment_id,
                        "status": "REFUNDED",
                        "refund_time": datetime.now(),
                        "update_by": current_user_name,
                        "update_time": datetime.now()
                    }
                    await PaymentsDao.edit_payments_dao(query_db, payment_update)
                
            # 发送邮件通知
            # 获取用户账号信息
            redis = request.app.state.redis
            
            # 获取用户详细信息
            user_basic_info = await UserDao.get_user_by_id(query_db, refund_updated.user_id)
            user_basic = user_basic_info.get('user_basic_info') if user_basic_info else None
            
            # 构建退款邮件所需信息
            user_info = {
                'user_id': refund_updated.user_id,
                'user_name': user_basic.nick_name if user_basic else f'用户{refund_updated.user_id}'
            }
            
            order_info = {
                'payment_id': refund_updated.payment_id,
                'product_name': refund_updated.product_name,
                'original_amount': refund_updated.refund_amount,  # 假设原订单金额等于退款金额
                'currency': refund_updated.refund_currency
            }
            
            refund_info = {
                'refund_amount': refund_audit.refund_amount,
                'refund_currency': refund_updated.refund_currency,
                'approved': refund_audit.confirm,
                'confirm_reason': refund_audit.confirm_reason
            }
            
            # 获取用户邮箱
            user_email = user_basic.email if user_basic and user_basic.email else None
            
            # 只有当用户有邮箱时才发送邮件
            email_result = False
            error_msg = "用户未设置邮箱，无法发送通知"
            
            if user_email:
                # 发送邮件通知
                email_result, error_msg = await EmailService.send_refund_notification_email(
                    user_email, user_info, order_info, refund_info
                )
            
            # 即使邮件发送失败，也认为审核成功
            await query_db.commit()
            
            if email_result:
                return CrudResponseModel(is_success=True, message='审核成功，已发送邮件通知')
            else:
                return CrudResponseModel(is_success=True, message=f'审核成功，但邮件通知失败: {error_msg}')
                
        except Exception as e:
            await query_db.rollback()
            raise e
