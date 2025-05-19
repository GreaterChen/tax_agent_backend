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
from module_admin.service.refunds_service import RefundsService
from module_admin.entity.vo.refunds_vo import DeleteRefundsModel, RefundsModel, RefundsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


refundsController = APIRouter(prefix='/system/refunds', dependencies=[Depends(LoginService.get_current_user)])


@refundsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:refunds:list'))]
)
async def get_system_refunds_list(
    request: Request,
refunds_page_query: RefundsPageQueryModel = Depends(RefundsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    refunds_page_query_result = await RefundsService.get_refunds_list_services(query_db, refunds_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=refunds_page_query_result)


@refundsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:refunds:add'))])
@ValidateFields(validate_model='add_refunds')
@Log(title='退款', business_type=BusinessType.INSERT)
async def add_system_refunds(
    request: Request,
    add_refunds: RefundsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_refunds.create_by = current_user.user.user_name
    add_refunds.create_time = datetime.now()
    add_refunds.update_by = current_user.user.user_name
    add_refunds.update_time = datetime.now()
    add_refunds_result = await RefundsService.add_refunds_services(query_db, add_refunds)
    logger.info(add_refunds_result.message)

    return ResponseUtil.success(msg=add_refunds_result.message)


@refundsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:refunds:edit'))])
@ValidateFields(validate_model='edit_refunds')
@Log(title='退款', business_type=BusinessType.UPDATE)
async def edit_system_refunds(
    request: Request,
    edit_refunds: RefundsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_refunds.update_by = current_user.user.user_name
    edit_refunds.update_time = datetime.now()
    edit_refunds_result = await RefundsService.edit_refunds_services(query_db, edit_refunds)
    logger.info(edit_refunds_result.message)

    return ResponseUtil.success(msg=edit_refunds_result.message)


@refundsController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:refunds:remove'))])
@Log(title='退款', business_type=BusinessType.DELETE)
async def delete_system_refunds(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_refunds = DeleteRefundsModel(ids=ids)
    delete_refunds_result = await RefundsService.delete_refunds_services(query_db, delete_refunds)
    logger.info(delete_refunds_result.message)

    return ResponseUtil.success(msg=delete_refunds_result.message)


@refundsController.get(
    '/{id}', response_model=RefundsModel, dependencies=[Depends(CheckUserInterfaceAuth('system:refunds:query'))]
)
async def query_detail_system_refunds(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    refunds_detail_result = await RefundsService.refunds_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=refunds_detail_result)


@refundsController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:refunds:export'))])
@Log(title='退款', business_type=BusinessType.EXPORT)
async def export_system_refunds_list(
    request: Request,
    refunds_page_query: RefundsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    refunds_query_result = await RefundsService.get_refunds_list_services(query_db, refunds_page_query, is_page=False)
    refunds_export_result = await RefundsService.export_refunds_list_services(refunds_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(refunds_export_result))
