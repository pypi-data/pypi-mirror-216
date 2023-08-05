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


class DeepLearningTask(
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
            "classification": "CLASSIFICATION",
            "semantic_segmentation": "SEMANTIC_SEGMENTATION",
            "object_detection": "OBJECT_DETECTION",
            "nlp": "NLP",
            "text_recognition": "TEXT_RECOGNITION",
            "other": "OTHER",
        }
    
    @schemas.classproperty
    def CLASSIFICATION(cls):
        return cls("classification")
    
    @schemas.classproperty
    def SEMANTIC_SEGMENTATION(cls):
        return cls("semantic_segmentation")
    
    @schemas.classproperty
    def OBJECT_DETECTION(cls):
        return cls("object_detection")
    
    @schemas.classproperty
    def NLP(cls):
        return cls("nlp")
    
    @schemas.classproperty
    def TEXT_RECOGNITION(cls):
        return cls("text_recognition")
    
    @schemas.classproperty
    def OTHER(cls):
        return cls("other")
