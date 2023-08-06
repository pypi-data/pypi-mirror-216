from zs_utils.api.wildberries.base_api import WildberriesAPI


class GetWildberriesWarehouseList(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace/paths/~1api~1v2~1warehouses/get
    """

    http_method = "GET"
    resource_method = "api/v2/warehouses"
