from typing import List
from rest_framework.decorators import parser_classes, api_view

from rest_framework.parsers import JSONParser
from rest_framework.request import Request

from exceptions.CustomException import BadRequestException


def api_endpoint(http_method_names: List[str]):
    def _func(func):
        func = api_view(http_method_names)(func)
        func = parser_classes([JSONParser])(func)
        return func

    return _func


def examine_data(func):
    def wrapper(req: Request, *args, **kwargs):
        if not isinstance(req.data, dict):
            raise BadRequestException()
        return func(req, data=req.data, *args, **kwargs)

    return wrapper


def api_post(func):
    func = examine_data(func)
    func = api_endpoint(["POST"])(func)

    return func


def api_delete(func):
    _func = api_endpoint(["DELETE"])
    return _func(func)


def api_get(func):
    _func = api_endpoint(["GET"])
    return _func(func)
