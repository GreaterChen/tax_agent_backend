from fastapi import APIRouter, Depends, Form, Request
from datetime import datetime
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.service.products_service import ProductsService
from module_admin.entity.vo.products_vo import DeleteProductsModel, ProductsModel, ProductsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


productsController = APIRouter(prefix='/system/products', dependencies=[Depends(LoginService.get_current_user)])


@productsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:products:list'))]
)
async def get_system_products_list(
    request: Request,
products_page_query: ProductsPageQueryModel = Depends(ProductsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    products_page_query_result = await ProductsService.get_products_list_services(query_db, products_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=products_page_query_result)


@productsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:products:add'))])
@ValidateFields(validate_model='add_products')
@Log(title='products', business_type=BusinessType.INSERT)
async def add_system_products(
    request: Request,
    add_products: ProductsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_products_result = await ProductsService.add_products_services(query_db, add_products)
    logger.info(add_products_result.message)

    return ResponseUtil.success(msg=add_products_result.message)


@productsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:products:edit'))])
@ValidateFields(validate_model='edit_products')
@Log(title='products', business_type=BusinessType.UPDATE)
async def edit_system_products(
    request: Request,
    edit_products: ProductsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_products.update_by = current_user.user.user_name
    edit_products.update_time = datetime.now()
    edit_products_result = await ProductsService.edit_products_services(query_db, edit_products)
    logger.info(edit_products_result.message)

    return ResponseUtil.success(msg=edit_products_result.message)


@productsController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:products:remove'))])
@Log(title='products', business_type=BusinessType.DELETE)
async def delete_system_products(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_products = DeleteProductsModel(ids=ids)
    delete_products_result = await ProductsService.delete_products_services(query_db, delete_products)
    logger.info(delete_products_result.message)

    return ResponseUtil.success(msg=delete_products_result.message)


@productsController.get(
    '/{id}', response_model=ProductsModel, dependencies=[Depends(CheckUserInterfaceAuth('system:products:query'))]
)
async def query_detail_system_products(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    products_detail_result = await ProductsService.products_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=products_detail_result)


@productsController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:products:export'))])
@Log(title='products', business_type=BusinessType.EXPORT)
async def export_system_products_list(
    request: Request,
    products_page_query: ProductsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    products_query_result = await ProductsService.get_products_list_services(query_db, products_page_query, is_page=False)
    products_export_result = await ProductsService.export_products_list_services(products_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(products_export_result))
