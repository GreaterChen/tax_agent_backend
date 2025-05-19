from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.refunds_dao import RefundsDao
from module_admin.entity.vo.refunds_vo import DeleteRefundsModel, RefundsModel, RefundsPageQueryModel
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
