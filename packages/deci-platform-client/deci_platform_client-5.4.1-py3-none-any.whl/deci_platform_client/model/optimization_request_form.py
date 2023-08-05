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


class OptimizationRequestForm(
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
            "quantizationLevel",
            "optimizeAutonac",
            "targetBatchSize",
            "targetHardware",
            "optimizeModelSize",
        }
        
        class properties:
        
            @staticmethod
            def targetHardware() -> typing.Type['HardwareType']:
                return HardwareType
            targetBatchSize = schemas.IntSchema
            optimizeModelSize = schemas.BoolSchema
        
            @staticmethod
            def quantizationLevel() -> typing.Type['QuantizationLevel']:
                return QuantizationLevel
            optimizeAutonac = schemas.BoolSchema
            
            
            class targetMetric(
                schemas.ComposedSchema,
            ):
            
            
                class MetaOapg:
                    
                    @classmethod
                    @functools.lru_cache()
                    def all_of(cls):
                        # we need this here to make our import statements work
                        # we must store _composed_schemas in here so the code is only run
                        # when we invoke this method. If we kept this at the class
                        # level we would get an error because the class level
                        # code would be run when this module is imported, and these composed
                        # classes don't exist yet because their module has not finished
                        # loading
                        return [
                            Metric,
                        ]
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'targetMetric':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            name = schemas.StrSchema
            rawFormat = schemas.BoolSchema
            conversionParameters = schemas.DictSchema
            __annotations__ = {
                "targetHardware": targetHardware,
                "targetBatchSize": targetBatchSize,
                "optimizeModelSize": optimizeModelSize,
                "quantizationLevel": quantizationLevel,
                "optimizeAutonac": optimizeAutonac,
                "targetMetric": targetMetric,
                "name": name,
                "rawFormat": rawFormat,
                "conversionParameters": conversionParameters,
            }
    
    quantizationLevel: 'QuantizationLevel'
    optimizeAutonac: MetaOapg.properties.optimizeAutonac
    targetBatchSize: MetaOapg.properties.targetBatchSize
    targetHardware: 'HardwareType'
    optimizeModelSize: MetaOapg.properties.optimizeModelSize
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["targetHardware"]) -> 'HardwareType': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["targetBatchSize"]) -> MetaOapg.properties.targetBatchSize: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["optimizeModelSize"]) -> MetaOapg.properties.optimizeModelSize: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["quantizationLevel"]) -> 'QuantizationLevel': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["optimizeAutonac"]) -> MetaOapg.properties.optimizeAutonac: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["targetMetric"]) -> MetaOapg.properties.targetMetric: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["rawFormat"]) -> MetaOapg.properties.rawFormat: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["conversionParameters"]) -> MetaOapg.properties.conversionParameters: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["targetHardware", "targetBatchSize", "optimizeModelSize", "quantizationLevel", "optimizeAutonac", "targetMetric", "name", "rawFormat", "conversionParameters", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["targetHardware"]) -> 'HardwareType': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["targetBatchSize"]) -> MetaOapg.properties.targetBatchSize: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["optimizeModelSize"]) -> MetaOapg.properties.optimizeModelSize: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["quantizationLevel"]) -> 'QuantizationLevel': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["optimizeAutonac"]) -> MetaOapg.properties.optimizeAutonac: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["targetMetric"]) -> typing.Union[MetaOapg.properties.targetMetric, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> typing.Union[MetaOapg.properties.name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["rawFormat"]) -> typing.Union[MetaOapg.properties.rawFormat, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["conversionParameters"]) -> typing.Union[MetaOapg.properties.conversionParameters, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["targetHardware", "targetBatchSize", "optimizeModelSize", "quantizationLevel", "optimizeAutonac", "targetMetric", "name", "rawFormat", "conversionParameters", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        quantizationLevel: 'QuantizationLevel',
        optimizeAutonac: typing.Union[MetaOapg.properties.optimizeAutonac, bool, ],
        targetBatchSize: typing.Union[MetaOapg.properties.targetBatchSize, decimal.Decimal, int, ],
        targetHardware: 'HardwareType',
        optimizeModelSize: typing.Union[MetaOapg.properties.optimizeModelSize, bool, ],
        targetMetric: typing.Union[MetaOapg.properties.targetMetric, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        name: typing.Union[MetaOapg.properties.name, str, schemas.Unset] = schemas.unset,
        rawFormat: typing.Union[MetaOapg.properties.rawFormat, bool, schemas.Unset] = schemas.unset,
        conversionParameters: typing.Union[MetaOapg.properties.conversionParameters, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'OptimizationRequestForm':
        return super().__new__(
            cls,
            *_args,
            quantizationLevel=quantizationLevel,
            optimizeAutonac=optimizeAutonac,
            targetBatchSize=targetBatchSize,
            targetHardware=targetHardware,
            optimizeModelSize=optimizeModelSize,
            targetMetric=targetMetric,
            name=name,
            rawFormat=rawFormat,
            conversionParameters=conversionParameters,
            _configuration=_configuration,
            **kwargs,
        )

from deci_platform_client.model.hardware_type import HardwareType
from deci_platform_client.model.metric import Metric
from deci_platform_client.model.quantization_level import QuantizationLevel
