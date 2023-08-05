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


class InferyVersion(
    schemas.EnumBase,
    schemas.StrSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    An enumeration.
    """


    class MetaOapg:
        enum_value_to_name = {
            "cpu": "CPU",
            "gpu": "GPU",
            "jetson": "JETSON",
            "jetson_py36": "JETSON_PY36",
            "jetson_py38": "JETSON_PY38",
        }
    
    @schemas.classproperty
    def CPU(cls):
        return cls("cpu")
    
    @schemas.classproperty
    def GPU(cls):
        return cls("gpu")
    
    @schemas.classproperty
    def JETSON(cls):
        return cls("jetson")
    
    @schemas.classproperty
    def JETSON_PY36(cls):
        return cls("jetson_py36")
    
    @schemas.classproperty
    def JETSON_PY38(cls):
        return cls("jetson_py38")
