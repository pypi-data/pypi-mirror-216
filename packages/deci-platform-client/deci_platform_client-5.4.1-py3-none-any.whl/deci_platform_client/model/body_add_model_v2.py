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


class BodyAddModelV2(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "model",
        }
        
        class properties:
        
            @staticmethod
            def model() -> typing.Type['ModelMetadataIn']:
                return ModelMetadataIn
            
            
            class hardware_types(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['HardwareType']:
                        return HardwareType
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['HardwareType'], typing.List['HardwareType']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'hardware_types':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'HardwareType':
                    return super().__getitem__(i)
            conversion_parameters = schemas.DictSchema
            __annotations__ = {
                "model": model,
                "hardware_types": hardware_types,
                "conversion_parameters": conversion_parameters,
            }
    
    model: 'ModelMetadataIn'
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["model"]) -> 'ModelMetadataIn': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["hardware_types"]) -> MetaOapg.properties.hardware_types: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["conversion_parameters"]) -> MetaOapg.properties.conversion_parameters: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["model", "hardware_types", "conversion_parameters", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["model"]) -> 'ModelMetadataIn': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["hardware_types"]) -> typing.Union[MetaOapg.properties.hardware_types, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["conversion_parameters"]) -> typing.Union[MetaOapg.properties.conversion_parameters, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["model", "hardware_types", "conversion_parameters", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        model: 'ModelMetadataIn',
        hardware_types: typing.Union[MetaOapg.properties.hardware_types, list, tuple, schemas.Unset] = schemas.unset,
        conversion_parameters: typing.Union[MetaOapg.properties.conversion_parameters, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'BodyAddModelV2':
        return super().__new__(
            cls,
            *_args,
            model=model,
            hardware_types=hardware_types,
            conversion_parameters=conversion_parameters,
            _configuration=_configuration,
            **kwargs,
        )

from deci_platform_client.model.hardware_type import HardwareType
from deci_platform_client.model.model_metadata_in import ModelMetadataIn
