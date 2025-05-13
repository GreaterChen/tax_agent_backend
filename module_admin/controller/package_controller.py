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
from module_admin.service.package_service import PackageService
from module_admin.entity.vo.package_vo import DeletePackageModel, PackageModel, PackagePageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


packageController = APIRouter(prefix='/custom/package', dependencies=[Depends(LoginService.get_current_user)])


@packageController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('custom:package:list'))]
)
async def get_custom_package_list(
    request: Request,
package_page_query: PackagePageQueryModel = Depends(PackagePageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    package_page_query_result = await PackageService.get_package_list_services(query_db, package_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=package_page_query_result)


@packageController.post('', dependencies=[Depends(CheckUserInterfaceAuth('custom:package:add'))])
@ValidateFields(validate_model='add_package')
@Log(title='package', business_type=BusinessType.INSERT)
async def add_custom_package(
    request: Request,
    add_package: PackageModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_package.create_time = datetime.now()
    add_package.update_time = datetime.now()
    add_package_result = await PackageService.add_package_services(query_db, add_package)
    logger.info(add_package_result.message)

    return ResponseUtil.success(msg=add_package_result.message)


@packageController.put('', dependencies=[Depends(CheckUserInterfaceAuth('custom:package:edit'))])
@ValidateFields(validate_model='edit_package')
@Log(title='package', business_type=BusinessType.UPDATE)
async def edit_custom_package(
    request: Request,
    edit_package: PackageModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_package.update_by = current_user.user.user_name
    edit_package.update_time = datetime.now()
    edit_package_result = await PackageService.edit_package_services(query_db, edit_package)
    logger.info(edit_package_result.message)

    return ResponseUtil.success(msg=edit_package_result.message)


@packageController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('custom:package:remove'))])
@Log(title='package', business_type=BusinessType.DELETE)
async def delete_custom_package(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_package = DeletePackageModel(ids=ids)
    delete_package_result = await PackageService.delete_package_services(query_db, delete_package)
    logger.info(delete_package_result.message)

    return ResponseUtil.success(msg=delete_package_result.message)


@packageController.get(
    '/{id}', response_model=PackageModel, dependencies=[Depends(CheckUserInterfaceAuth('custom:package:query'))]
)
async def query_detail_custom_package(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    package_detail_result = await PackageService.package_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=package_detail_result)


@packageController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('custom:package:export'))])
@Log(title='package', business_type=BusinessType.EXPORT)
async def export_custom_package_list(
    request: Request,
    package_page_query: PackagePageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    package_query_result = await PackageService.get_package_list_services(query_db, package_page_query, is_page=False)
    package_export_result = await PackageService.export_package_list_services(package_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(package_export_result))
