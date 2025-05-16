from datetime import datetime
from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.service.payments_service import PaymentsService
from module_admin.entity.vo.payments_vo import DeletePaymentsModel, PaymentsModel, PaymentsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


paymentsController = APIRouter(prefix='/system/payments', dependencies=[Depends(LoginService.get_current_user)])


@paymentsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:payments:list'))]
)
async def get_system_payments_list(
    request: Request,
payments_page_query: PaymentsPageQueryModel = Depends(PaymentsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    payments_page_query_result = await PaymentsService.get_payments_list_services(query_db, payments_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=payments_page_query_result)


@paymentsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:payments:add'))])
@ValidateFields(validate_model='add_payments')
@Log(title='支付订单', business_type=BusinessType.INSERT)
async def add_system_payments(
    request: Request,
    add_payments: PaymentsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_payments.create_by = current_user.user.user_name
    add_payments.create_time = datetime.now()
    add_payments.update_by = current_user.user.user_name
    add_payments.update_time = datetime.now()
    add_payments_result = await PaymentsService.add_payments_services(query_db, add_payments)
    logger.info(add_payments_result.message)

    return ResponseUtil.success(msg=add_payments_result.message)


@paymentsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:payments:edit'))])
@ValidateFields(validate_model='edit_payments')
@Log(title='支付订单', business_type=BusinessType.UPDATE)
async def edit_system_payments(
    request: Request,
    edit_payments: PaymentsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_payments.update_by = current_user.user.user_name
    edit_payments.update_time = datetime.now()
    edit_payments_result = await PaymentsService.edit_payments_services(query_db, edit_payments)
    logger.info(edit_payments_result.message)

    return ResponseUtil.success(msg=edit_payments_result.message)


@paymentsController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:payments:remove'))])
@Log(title='支付订单', business_type=BusinessType.DELETE)
async def delete_system_payments(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_payments = DeletePaymentsModel(ids=ids)
    delete_payments_result = await PaymentsService.delete_payments_services(query_db, delete_payments)
    logger.info(delete_payments_result.message)

    return ResponseUtil.success(msg=delete_payments_result.message)


@paymentsController.get(
    '/{id}', response_model=PaymentsModel, dependencies=[Depends(CheckUserInterfaceAuth('system:payments:query'))]
)
async def query_detail_system_payments(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    payments_detail_result = await PaymentsService.payments_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=payments_detail_result)


@paymentsController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:payments:export'))])
@Log(title='支付订单', business_type=BusinessType.EXPORT)
async def export_system_payments_list(
    request: Request,
    payments_page_query: PaymentsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    payments_query_result = await PaymentsService.get_payments_list_services(query_db, payments_page_query, is_page=False)
    payments_export_result = await PaymentsService.export_payments_list_services(request, payments_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(payments_export_result))
