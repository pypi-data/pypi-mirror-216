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


class ModelBenchmarkState(
    schemas.EnumBase,
    schemas.StrSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Benchmark states for repository models.
    """


    class MetaOapg:
        enum_value_to_name = {
            "Unknown": "UNKNOWN",
            "Pending": "PENDING",
            "In Progress": "IN_PROGRESS",
            "Succeeded Fully": "SUCCEEDED_FULLY",
            "Failed": "FAILED",
        }
    
    @schemas.classproperty
    def UNKNOWN(cls):
        return cls("Unknown")
    
    @schemas.classproperty
    def PENDING(cls):
        return cls("Pending")
    
    @schemas.classproperty
    def IN_PROGRESS(cls):
        return cls("In Progress")
    
    @schemas.classproperty
    def SUCCEEDED_FULLY(cls):
        return cls("Succeeded Fully")
    
    @schemas.classproperty
    def FAILED(cls):
        return cls("Failed")
