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


class DeepLearningTaskLabel(
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
            "Classification": "CLASSIFICATION",
            "Semantic Segmentation": "SEMANTIC_SEGMENTATION",
            "Object Detection": "OBJECT_DETECTION",
            "NLP": "NLP",
            "Text Recognition": "TEXT_RECOGNITION",
            "Other": "OTHER",
        }
    
    @schemas.classproperty
    def CLASSIFICATION(cls):
        return cls("Classification")
    
    @schemas.classproperty
    def SEMANTIC_SEGMENTATION(cls):
        return cls("Semantic Segmentation")
    
    @schemas.classproperty
    def OBJECT_DETECTION(cls):
        return cls("Object Detection")
    
    @schemas.classproperty
    def NLP(cls):
        return cls("NLP")
    
    @schemas.classproperty
    def TEXT_RECOGNITION(cls):
        return cls("Text Recognition")
    
    @schemas.classproperty
    def OTHER(cls):
        return cls("Other")
