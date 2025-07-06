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
from module_admin.service.custom_ai_package_service import Custom_ai_packageService
from module_admin.entity.vo.custom_ai_package_vo import DeleteCustom_ai_packageModel, Custom_ai_packageModel, Custom_ai_packagePageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


custom_ai_packageController = APIRouter(prefix='/system/custom_ai_package', dependencies=[Depends(LoginService.get_current_user)])


@custom_ai_packageController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:custom_ai_package:list'))]
)
async def get_system_custom_ai_package_list(
    request: Request,
custom_ai_package_page_query: Custom_ai_packagePageQueryModel = Depends(Custom_ai_packagePageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    custom_ai_package_page_query_result = await Custom_ai_packageService.get_custom_ai_package_list_services(query_db, custom_ai_package_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=custom_ai_package_page_query_result)


@custom_ai_packageController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:custom_ai_package:add'))])
@ValidateFields(validate_model='add_custom_ai_package')
@Log(title='用户套餐情况', business_type=BusinessType.INSERT)
async def add_system_custom_ai_package(
    request: Request,
    add_custom_ai_package: Custom_ai_packageModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_custom_ai_package.create_time = datetime.now()
    add_custom_ai_package.update_time = datetime.now()
    add_custom_ai_package_result = await Custom_ai_packageService.add_custom_ai_package_services(query_db, add_custom_ai_package)
    logger.info(add_custom_ai_package_result.message)

    return ResponseUtil.success(msg=add_custom_ai_package_result.message)


@custom_ai_packageController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:custom_ai_package:edit'))])
@ValidateFields(validate_model='edit_custom_ai_package')
@Log(title='用户套餐情况', business_type=BusinessType.UPDATE)
async def edit_system_custom_ai_package(
    request: Request,
    edit_custom_ai_package: Custom_ai_packageModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    # edit_custom_ai_package.update_by = current_user.user.user_name
    edit_custom_ai_package.update_time = datetime.now()
    edit_custom_ai_package_result = await Custom_ai_packageService.edit_custom_ai_package_services(query_db, edit_custom_ai_package)
    logger.info(edit_custom_ai_package_result.message)

    return ResponseUtil.success(msg=edit_custom_ai_package_result.message)


@custom_ai_packageController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:custom_ai_package:remove'))])
@Log(title='用户套餐情况', business_type=BusinessType.DELETE)
async def delete_system_custom_ai_package(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_custom_ai_package = DeleteCustom_ai_packageModel(ids=ids)
    delete_custom_ai_package_result = await Custom_ai_packageService.delete_custom_ai_package_services(query_db, delete_custom_ai_package)
    logger.info(delete_custom_ai_package_result.message)

    return ResponseUtil.success(msg=delete_custom_ai_package_result.message)


@custom_ai_packageController.get(
    '/{id}', response_model=Custom_ai_packageModel, dependencies=[Depends(CheckUserInterfaceAuth('system:custom_ai_package:query'))]
)
async def query_detail_system_custom_ai_package(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    custom_ai_package_detail_result = await Custom_ai_packageService.custom_ai_package_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=custom_ai_package_detail_result)


@custom_ai_packageController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:custom_ai_package:export'))])
@Log(title='用户套餐情况', business_type=BusinessType.EXPORT)
async def export_system_custom_ai_package_list(
    request: Request,
    custom_ai_package_page_query: Custom_ai_packagePageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    custom_ai_package_query_result = await Custom_ai_packageService.get_custom_ai_package_list_services(query_db, custom_ai_package_page_query, is_page=False)
    custom_ai_package_export_result = await Custom_ai_packageService.export_custom_ai_package_list_services(custom_ai_package_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(custom_ai_package_export_result))
