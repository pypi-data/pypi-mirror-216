"""
Type annotations for osis service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/type_defs/)

Usage::

    ```python
    from types_aiobotocore_osis.type_defs import ChangeProgressStageTypeDef

    data: ChangeProgressStageTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    ChangeProgressStageStatusesType,
    ChangeProgressStatusesType,
    PipelineStatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ChangeProgressStageTypeDef",
    "CloudWatchLogDestinationTypeDef",
    "TagTypeDef",
    "VpcOptionsTypeDef",
    "DeletePipelineRequestRequestTypeDef",
    "GetPipelineBlueprintRequestRequestTypeDef",
    "PipelineBlueprintTypeDef",
    "GetPipelineChangeProgressRequestRequestTypeDef",
    "GetPipelineRequestRequestTypeDef",
    "PipelineBlueprintSummaryTypeDef",
    "ListPipelinesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PipelineStatusReasonTypeDef",
    "ResponseMetadataTypeDef",
    "StartPipelineRequestRequestTypeDef",
    "StopPipelineRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "ValidatePipelineRequestRequestTypeDef",
    "ValidationMessageTypeDef",
    "ChangeProgressStatusTypeDef",
    "LogPublishingOptionsTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "VpcEndpointTypeDef",
    "GetPipelineBlueprintResponseTypeDef",
    "ListPipelineBlueprintsResponseTypeDef",
    "PipelineSummaryTypeDef",
    "ValidatePipelineResponseTypeDef",
    "GetPipelineChangeProgressResponseTypeDef",
    "CreatePipelineRequestRequestTypeDef",
    "UpdatePipelineRequestRequestTypeDef",
    "PipelineTypeDef",
    "ListPipelinesResponseTypeDef",
    "CreatePipelineResponseTypeDef",
    "GetPipelineResponseTypeDef",
    "StartPipelineResponseTypeDef",
    "StopPipelineResponseTypeDef",
    "UpdatePipelineResponseTypeDef",
)

ChangeProgressStageTypeDef = TypedDict(
    "ChangeProgressStageTypeDef",
    {
        "Name": str,
        "Status": ChangeProgressStageStatusesType,
        "Description": str,
        "LastUpdatedAt": datetime,
    },
    total=False,
)

CloudWatchLogDestinationTypeDef = TypedDict(
    "CloudWatchLogDestinationTypeDef",
    {
        "LogGroup": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

_RequiredVpcOptionsTypeDef = TypedDict(
    "_RequiredVpcOptionsTypeDef",
    {
        "SubnetIds": Sequence[str],
    },
)
_OptionalVpcOptionsTypeDef = TypedDict(
    "_OptionalVpcOptionsTypeDef",
    {
        "SecurityGroupIds": Sequence[str],
    },
    total=False,
)


class VpcOptionsTypeDef(_RequiredVpcOptionsTypeDef, _OptionalVpcOptionsTypeDef):
    pass


DeletePipelineRequestRequestTypeDef = TypedDict(
    "DeletePipelineRequestRequestTypeDef",
    {
        "PipelineName": str,
    },
)

GetPipelineBlueprintRequestRequestTypeDef = TypedDict(
    "GetPipelineBlueprintRequestRequestTypeDef",
    {
        "BlueprintName": str,
    },
)

PipelineBlueprintTypeDef = TypedDict(
    "PipelineBlueprintTypeDef",
    {
        "BlueprintName": str,
        "PipelineConfigurationBody": str,
    },
    total=False,
)

GetPipelineChangeProgressRequestRequestTypeDef = TypedDict(
    "GetPipelineChangeProgressRequestRequestTypeDef",
    {
        "PipelineName": str,
    },
)

GetPipelineRequestRequestTypeDef = TypedDict(
    "GetPipelineRequestRequestTypeDef",
    {
        "PipelineName": str,
    },
)

PipelineBlueprintSummaryTypeDef = TypedDict(
    "PipelineBlueprintSummaryTypeDef",
    {
        "BlueprintName": str,
    },
    total=False,
)

ListPipelinesRequestRequestTypeDef = TypedDict(
    "ListPipelinesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

PipelineStatusReasonTypeDef = TypedDict(
    "PipelineStatusReasonTypeDef",
    {
        "Description": str,
    },
    total=False,
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

StartPipelineRequestRequestTypeDef = TypedDict(
    "StartPipelineRequestRequestTypeDef",
    {
        "PipelineName": str,
    },
)

StopPipelineRequestRequestTypeDef = TypedDict(
    "StopPipelineRequestRequestTypeDef",
    {
        "PipelineName": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "Arn": str,
        "TagKeys": Sequence[str],
    },
)

ValidatePipelineRequestRequestTypeDef = TypedDict(
    "ValidatePipelineRequestRequestTypeDef",
    {
        "PipelineConfigurationBody": str,
    },
)

ValidationMessageTypeDef = TypedDict(
    "ValidationMessageTypeDef",
    {
        "Message": str,
    },
    total=False,
)

ChangeProgressStatusTypeDef = TypedDict(
    "ChangeProgressStatusTypeDef",
    {
        "StartTime": datetime,
        "Status": ChangeProgressStatusesType,
        "TotalNumberOfStages": int,
        "ChangeProgressStages": List[ChangeProgressStageTypeDef],
    },
    total=False,
)

LogPublishingOptionsTypeDef = TypedDict(
    "LogPublishingOptionsTypeDef",
    {
        "IsLoggingEnabled": bool,
        "CloudWatchLogDestination": CloudWatchLogDestinationTypeDef,
    },
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "Arn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

VpcEndpointTypeDef = TypedDict(
    "VpcEndpointTypeDef",
    {
        "VpcEndpointId": str,
        "VpcId": str,
        "VpcOptions": VpcOptionsTypeDef,
    },
    total=False,
)

GetPipelineBlueprintResponseTypeDef = TypedDict(
    "GetPipelineBlueprintResponseTypeDef",
    {
        "Blueprint": PipelineBlueprintTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListPipelineBlueprintsResponseTypeDef = TypedDict(
    "ListPipelineBlueprintsResponseTypeDef",
    {
        "Blueprints": List[PipelineBlueprintSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PipelineSummaryTypeDef = TypedDict(
    "PipelineSummaryTypeDef",
    {
        "Status": PipelineStatusType,
        "StatusReason": PipelineStatusReasonTypeDef,
        "PipelineName": str,
        "PipelineArn": str,
        "MinUnits": int,
        "MaxUnits": int,
        "CreatedAt": datetime,
        "LastUpdatedAt": datetime,
    },
    total=False,
)

ValidatePipelineResponseTypeDef = TypedDict(
    "ValidatePipelineResponseTypeDef",
    {
        "isValid": bool,
        "Errors": List[ValidationMessageTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetPipelineChangeProgressResponseTypeDef = TypedDict(
    "GetPipelineChangeProgressResponseTypeDef",
    {
        "ChangeProgressStatuses": List[ChangeProgressStatusTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreatePipelineRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePipelineRequestRequestTypeDef",
    {
        "PipelineName": str,
        "MinUnits": int,
        "MaxUnits": int,
        "PipelineConfigurationBody": str,
    },
)
_OptionalCreatePipelineRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePipelineRequestRequestTypeDef",
    {
        "LogPublishingOptions": LogPublishingOptionsTypeDef,
        "VpcOptions": VpcOptionsTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreatePipelineRequestRequestTypeDef(
    _RequiredCreatePipelineRequestRequestTypeDef, _OptionalCreatePipelineRequestRequestTypeDef
):
    pass


_RequiredUpdatePipelineRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePipelineRequestRequestTypeDef",
    {
        "PipelineName": str,
    },
)
_OptionalUpdatePipelineRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePipelineRequestRequestTypeDef",
    {
        "MinUnits": int,
        "MaxUnits": int,
        "PipelineConfigurationBody": str,
        "LogPublishingOptions": LogPublishingOptionsTypeDef,
    },
    total=False,
)


class UpdatePipelineRequestRequestTypeDef(
    _RequiredUpdatePipelineRequestRequestTypeDef, _OptionalUpdatePipelineRequestRequestTypeDef
):
    pass


PipelineTypeDef = TypedDict(
    "PipelineTypeDef",
    {
        "PipelineName": str,
        "PipelineArn": str,
        "MinUnits": int,
        "MaxUnits": int,
        "Status": PipelineStatusType,
        "StatusReason": PipelineStatusReasonTypeDef,
        "PipelineConfigurationBody": str,
        "CreatedAt": datetime,
        "LastUpdatedAt": datetime,
        "IngestEndpointUrls": List[str],
        "LogPublishingOptions": LogPublishingOptionsTypeDef,
        "VpcEndpoints": List[VpcEndpointTypeDef],
    },
    total=False,
)

ListPipelinesResponseTypeDef = TypedDict(
    "ListPipelinesResponseTypeDef",
    {
        "NextToken": str,
        "Pipelines": List[PipelineSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreatePipelineResponseTypeDef = TypedDict(
    "CreatePipelineResponseTypeDef",
    {
        "Pipeline": PipelineTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetPipelineResponseTypeDef = TypedDict(
    "GetPipelineResponseTypeDef",
    {
        "Pipeline": PipelineTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartPipelineResponseTypeDef = TypedDict(
    "StartPipelineResponseTypeDef",
    {
        "Pipeline": PipelineTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopPipelineResponseTypeDef = TypedDict(
    "StopPipelineResponseTypeDef",
    {
        "Pipeline": PipelineTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdatePipelineResponseTypeDef = TypedDict(
    "UpdatePipelineResponseTypeDef",
    {
        "Pipeline": PipelineTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
