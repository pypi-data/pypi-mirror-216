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


class AutonacArchitecture(
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
            "owner",
            "modelId",
            "initialPrimaryHardware",
            "initialModelSize",
            "initialHyperParameters",
            "source",
            "initialKpis",
            "deepLearningTask",
            "deliveryState",
            "initialInputDimensions",
            "name",
            "initialDescription",
            "initialAccuracyMetrics",
            "initialQuantizationLevel",
            "initialOptimizationState",
            "initialBaselineModelId",
            "architecture",
            "workspaceId",
        }
        
        class properties:
            workspaceId = schemas.UUIDSchema
            owner = schemas.UUIDSchema
            modelId = schemas.UUIDSchema
            name = schemas.StrSchema
        
            @staticmethod
            def deliveryState() -> typing.Type['AutonacDeliveryState']:
                return AutonacDeliveryState
        
            @staticmethod
            def deepLearningTask() -> typing.Type['DeepLearningTask']:
                return DeepLearningTask
        
            @staticmethod
            def source() -> typing.Type['AutonacSource']:
                return AutonacSource
            architecture = schemas.StrSchema
            initialModelSize = schemas.NumberSchema
        
            @staticmethod
            def initialQuantizationLevel() -> typing.Type['QuantizationLevel']:
                return QuantizationLevel
            
            
            class initialInputDimensions(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    items = schemas.AnyTypeSchema
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ]], typing.List[typing.Union[MetaOapg.items, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ]]],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'initialInputDimensions':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> MetaOapg.items:
                    return super().__getitem__(i)
            
            
            class initialAccuracyMetrics(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['AccuracyMetric']:
                        return AccuracyMetric
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['AccuracyMetric'], typing.List['AccuracyMetric']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'initialAccuracyMetrics':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'AccuracyMetric':
                    return super().__getitem__(i)
            
            
            class initialHyperParameters(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['HyperParameter']:
                        return HyperParameter
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['HyperParameter'], typing.List['HyperParameter']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'initialHyperParameters':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'HyperParameter':
                    return super().__getitem__(i)
            initialDescription = schemas.StrSchema
            
            
            class initialKpis(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['KPI']:
                        return KPI
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['KPI'], typing.List['KPI']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'initialKpis':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'KPI':
                    return super().__getitem__(i)
        
            @staticmethod
            def initialOptimizationState() -> typing.Type['ModelOptimizationState']:
                return ModelOptimizationState
            initialBaselineModelId = schemas.UUIDSchema
        
            @staticmethod
            def initialPrimaryHardware() -> typing.Type['HardwareType']:
                return HardwareType
            updateTime = schemas.DateTimeSchema
            creationTime = schemas.DateTimeSchema
            id = schemas.UUIDSchema
            deleted = schemas.BoolSchema
            
            
            class autonac(
                schemas.EnumBase,
                schemas.BoolSchema
            ):
            
            
                class MetaOapg:
                    enum_value_to_name = {
                        schemas.BoolClass.TRUE: "TRUE",
                    }
                
                @schemas.classproperty
                def TRUE(cls):
                    return cls(True)
            colabLink = schemas.StrSchema
            initialRawFormat = schemas.BoolSchema
            __annotations__ = {
                "workspaceId": workspaceId,
                "owner": owner,
                "modelId": modelId,
                "name": name,
                "deliveryState": deliveryState,
                "deepLearningTask": deepLearningTask,
                "source": source,
                "architecture": architecture,
                "initialModelSize": initialModelSize,
                "initialQuantizationLevel": initialQuantizationLevel,
                "initialInputDimensions": initialInputDimensions,
                "initialAccuracyMetrics": initialAccuracyMetrics,
                "initialHyperParameters": initialHyperParameters,
                "initialDescription": initialDescription,
                "initialKpis": initialKpis,
                "initialOptimizationState": initialOptimizationState,
                "initialBaselineModelId": initialBaselineModelId,
                "initialPrimaryHardware": initialPrimaryHardware,
                "updateTime": updateTime,
                "creationTime": creationTime,
                "id": id,
                "deleted": deleted,
                "autonac": autonac,
                "colabLink": colabLink,
                "initialRawFormat": initialRawFormat,
            }
    
    owner: MetaOapg.properties.owner
    modelId: MetaOapg.properties.modelId
    initialPrimaryHardware: 'HardwareType'
    initialModelSize: MetaOapg.properties.initialModelSize
    initialHyperParameters: MetaOapg.properties.initialHyperParameters
    source: 'AutonacSource'
    initialKpis: MetaOapg.properties.initialKpis
    deepLearningTask: 'DeepLearningTask'
    deliveryState: 'AutonacDeliveryState'
    initialInputDimensions: MetaOapg.properties.initialInputDimensions
    name: MetaOapg.properties.name
    initialDescription: MetaOapg.properties.initialDescription
    initialAccuracyMetrics: MetaOapg.properties.initialAccuracyMetrics
    initialQuantizationLevel: 'QuantizationLevel'
    initialOptimizationState: 'ModelOptimizationState'
    initialBaselineModelId: MetaOapg.properties.initialBaselineModelId
    architecture: MetaOapg.properties.architecture
    workspaceId: MetaOapg.properties.workspaceId
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["workspaceId"]) -> MetaOapg.properties.workspaceId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["owner"]) -> MetaOapg.properties.owner: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["modelId"]) -> MetaOapg.properties.modelId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["deliveryState"]) -> 'AutonacDeliveryState': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["deepLearningTask"]) -> 'DeepLearningTask': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["source"]) -> 'AutonacSource': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["architecture"]) -> MetaOapg.properties.architecture: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["initialModelSize"]) -> MetaOapg.properties.initialModelSize: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["initialQuantizationLevel"]) -> 'QuantizationLevel': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["initialInputDimensions"]) -> MetaOapg.properties.initialInputDimensions: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["initialAccuracyMetrics"]) -> MetaOapg.properties.initialAccuracyMetrics: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["initialHyperParameters"]) -> MetaOapg.properties.initialHyperParameters: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["initialDescription"]) -> MetaOapg.properties.initialDescription: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["initialKpis"]) -> MetaOapg.properties.initialKpis: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["initialOptimizationState"]) -> 'ModelOptimizationState': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["initialBaselineModelId"]) -> MetaOapg.properties.initialBaselineModelId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["initialPrimaryHardware"]) -> 'HardwareType': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["updateTime"]) -> MetaOapg.properties.updateTime: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["creationTime"]) -> MetaOapg.properties.creationTime: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["deleted"]) -> MetaOapg.properties.deleted: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["autonac"]) -> MetaOapg.properties.autonac: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["colabLink"]) -> MetaOapg.properties.colabLink: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["initialRawFormat"]) -> MetaOapg.properties.initialRawFormat: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["workspaceId", "owner", "modelId", "name", "deliveryState", "deepLearningTask", "source", "architecture", "initialModelSize", "initialQuantizationLevel", "initialInputDimensions", "initialAccuracyMetrics", "initialHyperParameters", "initialDescription", "initialKpis", "initialOptimizationState", "initialBaselineModelId", "initialPrimaryHardware", "updateTime", "creationTime", "id", "deleted", "autonac", "colabLink", "initialRawFormat", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["workspaceId"]) -> MetaOapg.properties.workspaceId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["owner"]) -> MetaOapg.properties.owner: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["modelId"]) -> MetaOapg.properties.modelId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["deliveryState"]) -> 'AutonacDeliveryState': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["deepLearningTask"]) -> 'DeepLearningTask': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["source"]) -> 'AutonacSource': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["architecture"]) -> MetaOapg.properties.architecture: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["initialModelSize"]) -> MetaOapg.properties.initialModelSize: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["initialQuantizationLevel"]) -> 'QuantizationLevel': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["initialInputDimensions"]) -> MetaOapg.properties.initialInputDimensions: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["initialAccuracyMetrics"]) -> MetaOapg.properties.initialAccuracyMetrics: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["initialHyperParameters"]) -> MetaOapg.properties.initialHyperParameters: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["initialDescription"]) -> MetaOapg.properties.initialDescription: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["initialKpis"]) -> MetaOapg.properties.initialKpis: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["initialOptimizationState"]) -> 'ModelOptimizationState': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["initialBaselineModelId"]) -> MetaOapg.properties.initialBaselineModelId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["initialPrimaryHardware"]) -> 'HardwareType': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["updateTime"]) -> typing.Union[MetaOapg.properties.updateTime, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["creationTime"]) -> typing.Union[MetaOapg.properties.creationTime, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> typing.Union[MetaOapg.properties.id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["deleted"]) -> typing.Union[MetaOapg.properties.deleted, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["autonac"]) -> typing.Union[MetaOapg.properties.autonac, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["colabLink"]) -> typing.Union[MetaOapg.properties.colabLink, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["initialRawFormat"]) -> typing.Union[MetaOapg.properties.initialRawFormat, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["workspaceId", "owner", "modelId", "name", "deliveryState", "deepLearningTask", "source", "architecture", "initialModelSize", "initialQuantizationLevel", "initialInputDimensions", "initialAccuracyMetrics", "initialHyperParameters", "initialDescription", "initialKpis", "initialOptimizationState", "initialBaselineModelId", "initialPrimaryHardware", "updateTime", "creationTime", "id", "deleted", "autonac", "colabLink", "initialRawFormat", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        owner: typing.Union[MetaOapg.properties.owner, str, uuid.UUID, ],
        modelId: typing.Union[MetaOapg.properties.modelId, str, uuid.UUID, ],
        initialPrimaryHardware: 'HardwareType',
        initialModelSize: typing.Union[MetaOapg.properties.initialModelSize, decimal.Decimal, int, float, ],
        initialHyperParameters: typing.Union[MetaOapg.properties.initialHyperParameters, list, tuple, ],
        source: 'AutonacSource',
        initialKpis: typing.Union[MetaOapg.properties.initialKpis, list, tuple, ],
        deepLearningTask: 'DeepLearningTask',
        deliveryState: 'AutonacDeliveryState',
        initialInputDimensions: typing.Union[MetaOapg.properties.initialInputDimensions, list, tuple, ],
        name: typing.Union[MetaOapg.properties.name, str, ],
        initialDescription: typing.Union[MetaOapg.properties.initialDescription, str, ],
        initialAccuracyMetrics: typing.Union[MetaOapg.properties.initialAccuracyMetrics, list, tuple, ],
        initialQuantizationLevel: 'QuantizationLevel',
        initialOptimizationState: 'ModelOptimizationState',
        initialBaselineModelId: typing.Union[MetaOapg.properties.initialBaselineModelId, str, uuid.UUID, ],
        architecture: typing.Union[MetaOapg.properties.architecture, str, ],
        workspaceId: typing.Union[MetaOapg.properties.workspaceId, str, uuid.UUID, ],
        updateTime: typing.Union[MetaOapg.properties.updateTime, str, datetime, schemas.Unset] = schemas.unset,
        creationTime: typing.Union[MetaOapg.properties.creationTime, str, datetime, schemas.Unset] = schemas.unset,
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        deleted: typing.Union[MetaOapg.properties.deleted, bool, schemas.Unset] = schemas.unset,
        autonac: typing.Union[MetaOapg.properties.autonac, bool, schemas.Unset] = schemas.unset,
        colabLink: typing.Union[MetaOapg.properties.colabLink, str, schemas.Unset] = schemas.unset,
        initialRawFormat: typing.Union[MetaOapg.properties.initialRawFormat, bool, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'AutonacArchitecture':
        return super().__new__(
            cls,
            *_args,
            owner=owner,
            modelId=modelId,
            initialPrimaryHardware=initialPrimaryHardware,
            initialModelSize=initialModelSize,
            initialHyperParameters=initialHyperParameters,
            source=source,
            initialKpis=initialKpis,
            deepLearningTask=deepLearningTask,
            deliveryState=deliveryState,
            initialInputDimensions=initialInputDimensions,
            name=name,
            initialDescription=initialDescription,
            initialAccuracyMetrics=initialAccuracyMetrics,
            initialQuantizationLevel=initialQuantizationLevel,
            initialOptimizationState=initialOptimizationState,
            initialBaselineModelId=initialBaselineModelId,
            architecture=architecture,
            workspaceId=workspaceId,
            updateTime=updateTime,
            creationTime=creationTime,
            id=id,
            deleted=deleted,
            autonac=autonac,
            colabLink=colabLink,
            initialRawFormat=initialRawFormat,
            _configuration=_configuration,
            **kwargs,
        )

from deci_platform_client.model.accuracy_metric import AccuracyMetric
from deci_platform_client.model.autonac_delivery_state import AutonacDeliveryState
from deci_platform_client.model.autonac_source import AutonacSource
from deci_platform_client.model.deep_learning_task import DeepLearningTask
from deci_platform_client.model.hardware_type import HardwareType
from deci_platform_client.model.hyper_parameter import HyperParameter
from deci_platform_client.model.kpi import KPI
from deci_platform_client.model.model_optimization_state import ModelOptimizationState
from deci_platform_client.model.quantization_level import QuantizationLevel
