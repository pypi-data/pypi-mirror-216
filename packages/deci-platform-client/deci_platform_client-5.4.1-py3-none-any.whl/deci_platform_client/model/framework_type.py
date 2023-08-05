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


class FrameworkType(
    schemas.EnumBase,
    schemas.StrSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    A general deep learning framework, without a version.
    """


    class MetaOapg:
        enum_value_to_name = {
            "tf1": "TF1",
            "tf2": "TF2",
            "pytorch": "PYTORCH",
            "onnx": "ONNX",
            "torchscript": "TORCHSCRIPT",
            "trt": "TRT",
            "tvm": "TVM",
            "openvino": "OPENVINO",
            "keras": "KERAS",
            "tflite": "TFLITE",
            "coreml": "COREML",
            "tfjs": "TFJS",
        }
    
    @schemas.classproperty
    def TF1(cls):
        return cls("tf1")
    
    @schemas.classproperty
    def TF2(cls):
        return cls("tf2")
    
    @schemas.classproperty
    def PYTORCH(cls):
        return cls("pytorch")
    
    @schemas.classproperty
    def ONNX(cls):
        return cls("onnx")
    
    @schemas.classproperty
    def TORCHSCRIPT(cls):
        return cls("torchscript")
    
    @schemas.classproperty
    def TRT(cls):
        return cls("trt")
    
    @schemas.classproperty
    def TVM(cls):
        return cls("tvm")
    
    @schemas.classproperty
    def OPENVINO(cls):
        return cls("openvino")
    
    @schemas.classproperty
    def KERAS(cls):
        return cls("keras")
    
    @schemas.classproperty
    def TFLITE(cls):
        return cls("tflite")
    
    @schemas.classproperty
    def COREML(cls):
        return cls("coreml")
    
    @schemas.classproperty
    def TFJS(cls):
        return cls("tfjs")
