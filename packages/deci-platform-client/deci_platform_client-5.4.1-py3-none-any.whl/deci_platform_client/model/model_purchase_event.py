# coding: utf-8

"""
    Deci Platform API

    Train, deploy, optimize and serve your models using Deci's platform, in your cloud or on premise.  # noqa: E501

    The version of the OpenAPI document: 4.0.0
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from deci_platform_client import schemas  # noqa: F401


class ModelPurchaseEvent(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    A base class for all of Deci's model classes.
A model stores data in constant fields, and let us manipulate the data in a more readable way.
    """


    class MetaOapg:
        required = {
            "chosenModelId",
        }
        
        class properties:
            chosenModelId = schemas.UUIDSchema
            comparedModelId = schemas.UUIDSchema
            __annotations__ = {
                "chosenModelId": chosenModelId,
                "comparedModelId": comparedModelId,
            }
    
    chosenModelId: MetaOapg.properties.chosenModelId
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["chosenModelId"]) -> MetaOapg.properties.chosenModelId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["comparedModelId"]) -> MetaOapg.properties.comparedModelId: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["chosenModelId", "comparedModelId", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["chosenModelId"]) -> MetaOapg.properties.chosenModelId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["comparedModelId"]) -> typing.Union[MetaOapg.properties.comparedModelId, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["chosenModelId", "comparedModelId", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        chosenModelId: typing.Union[MetaOapg.properties.chosenModelId, str, uuid.UUID, ],
        comparedModelId: typing.Union[MetaOapg.properties.comparedModelId, str, uuid.UUID, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ModelPurchaseEvent':
        return super().__new__(
            cls,
            *_args,
            chosenModelId=chosenModelId,
            comparedModelId=comparedModelId,
            _configuration=_configuration,
            **kwargs,
        )
