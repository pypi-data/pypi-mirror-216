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


class AccuracyMetricsSchemaResponse(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    The fields of a accuracy metrics
:default = if given this is the main metric for this task we are comparing models acoording to.
    """


    class MetaOapg:
        required = {
            "metrics",
        }
        
        class properties:
            
            
            class metrics(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['AccuracyMetricKey']:
                        return AccuracyMetricKey
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['AccuracyMetricKey'], typing.List['AccuracyMetricKey']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'metrics':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'AccuracyMetricKey':
                    return super().__getitem__(i)
        
            @staticmethod
            def default() -> typing.Type['AccuracyMetricKey']:
                return AccuracyMetricKey
            __annotations__ = {
                "metrics": metrics,
                "default": default,
            }
    
    metrics: MetaOapg.properties.metrics
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["metrics"]) -> MetaOapg.properties.metrics: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["default"]) -> 'AccuracyMetricKey': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["metrics", "default", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["metrics"]) -> MetaOapg.properties.metrics: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["default"]) -> typing.Union['AccuracyMetricKey', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["metrics", "default", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        metrics: typing.Union[MetaOapg.properties.metrics, list, tuple, ],
        default: typing.Union['AccuracyMetricKey', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'AccuracyMetricsSchemaResponse':
        return super().__new__(
            cls,
            *_args,
            metrics=metrics,
            default=default,
            _configuration=_configuration,
            **kwargs,
        )

from deci_platform_client.model.accuracy_metric_key import AccuracyMetricKey
