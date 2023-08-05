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


class Architectures(
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
            "userArchitectures",
            "autonacs",
        }
        
        class properties:
            
            
            class userArchitectures(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['UserArchitecture']:
                        return UserArchitecture
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['UserArchitecture'], typing.List['UserArchitecture']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'userArchitectures':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'UserArchitecture':
                    return super().__getitem__(i)
            
            
            class autonacs(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['AutonacArchitecture']:
                        return AutonacArchitecture
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['AutonacArchitecture'], typing.List['AutonacArchitecture']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'autonacs':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'AutonacArchitecture':
                    return super().__getitem__(i)
            __annotations__ = {
                "userArchitectures": userArchitectures,
                "autonacs": autonacs,
            }
    
    userArchitectures: MetaOapg.properties.userArchitectures
    autonacs: MetaOapg.properties.autonacs
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["userArchitectures"]) -> MetaOapg.properties.userArchitectures: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["autonacs"]) -> MetaOapg.properties.autonacs: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["userArchitectures", "autonacs", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["userArchitectures"]) -> MetaOapg.properties.userArchitectures: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["autonacs"]) -> MetaOapg.properties.autonacs: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["userArchitectures", "autonacs", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        userArchitectures: typing.Union[MetaOapg.properties.userArchitectures, list, tuple, ],
        autonacs: typing.Union[MetaOapg.properties.autonacs, list, tuple, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'Architectures':
        return super().__new__(
            cls,
            *_args,
            userArchitectures=userArchitectures,
            autonacs=autonacs,
            _configuration=_configuration,
            **kwargs,
        )

from deci_platform_client.model.autonac_architecture import AutonacArchitecture
from deci_platform_client.model.user_architecture import UserArchitecture
