"""
Type annotations for scheduler service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/type_defs/)

Usage::

    ```python
    from types_aiobotocore_scheduler.type_defs import AwsVpcConfigurationTypeDef

    data: AwsVpcConfigurationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AssignPublicIpType,
    FlexibleTimeWindowModeType,
    LaunchTypeType,
    PlacementConstraintTypeType,
    PlacementStrategyTypeType,
    ScheduleGroupStateType,
    ScheduleStateType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AwsVpcConfigurationTypeDef",
    "CapacityProviderStrategyItemTypeDef",
    "TagTypeDef",
    "CreateScheduleGroupOutputTypeDef",
    "FlexibleTimeWindowTypeDef",
    "CreateScheduleOutputTypeDef",
    "DeadLetterConfigTypeDef",
    "DeleteScheduleGroupInputRequestTypeDef",
    "DeleteScheduleInputRequestTypeDef",
    "PlacementConstraintTypeDef",
    "PlacementStrategyTypeDef",
    "EventBridgeParametersTypeDef",
    "GetScheduleGroupInputRequestTypeDef",
    "GetScheduleGroupOutputTypeDef",
    "GetScheduleInputRequestTypeDef",
    "KinesisParametersTypeDef",
    "ListScheduleGroupsInputListScheduleGroupsPaginateTypeDef",
    "ListScheduleGroupsInputRequestTypeDef",
    "ScheduleGroupSummaryTypeDef",
    "ListSchedulesInputListSchedulesPaginateTypeDef",
    "ListSchedulesInputRequestTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "RetryPolicyTypeDef",
    "SageMakerPipelineParameterTypeDef",
    "TargetSummaryTypeDef",
    "SqsParametersTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateScheduleOutputTypeDef",
    "NetworkConfigurationTypeDef",
    "CreateScheduleGroupInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "TagResourceInputRequestTypeDef",
    "ListScheduleGroupsOutputTypeDef",
    "SageMakerPipelineParametersTypeDef",
    "ScheduleSummaryTypeDef",
    "EcsParametersTypeDef",
    "ListSchedulesOutputTypeDef",
    "TargetTypeDef",
    "CreateScheduleInputRequestTypeDef",
    "GetScheduleOutputTypeDef",
    "UpdateScheduleInputRequestTypeDef",
)

_RequiredAwsVpcConfigurationTypeDef = TypedDict(
    "_RequiredAwsVpcConfigurationTypeDef",
    {
        "Subnets": Sequence[str],
    },
)
_OptionalAwsVpcConfigurationTypeDef = TypedDict(
    "_OptionalAwsVpcConfigurationTypeDef",
    {
        "AssignPublicIp": AssignPublicIpType,
        "SecurityGroups": Sequence[str],
    },
    total=False,
)


class AwsVpcConfigurationTypeDef(
    _RequiredAwsVpcConfigurationTypeDef, _OptionalAwsVpcConfigurationTypeDef
):
    pass


_RequiredCapacityProviderStrategyItemTypeDef = TypedDict(
    "_RequiredCapacityProviderStrategyItemTypeDef",
    {
        "capacityProvider": str,
    },
)
_OptionalCapacityProviderStrategyItemTypeDef = TypedDict(
    "_OptionalCapacityProviderStrategyItemTypeDef",
    {
        "base": int,
        "weight": int,
    },
    total=False,
)


class CapacityProviderStrategyItemTypeDef(
    _RequiredCapacityProviderStrategyItemTypeDef, _OptionalCapacityProviderStrategyItemTypeDef
):
    pass


TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

CreateScheduleGroupOutputTypeDef = TypedDict(
    "CreateScheduleGroupOutputTypeDef",
    {
        "ScheduleGroupArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredFlexibleTimeWindowTypeDef = TypedDict(
    "_RequiredFlexibleTimeWindowTypeDef",
    {
        "Mode": FlexibleTimeWindowModeType,
    },
)
_OptionalFlexibleTimeWindowTypeDef = TypedDict(
    "_OptionalFlexibleTimeWindowTypeDef",
    {
        "MaximumWindowInMinutes": int,
    },
    total=False,
)


class FlexibleTimeWindowTypeDef(
    _RequiredFlexibleTimeWindowTypeDef, _OptionalFlexibleTimeWindowTypeDef
):
    pass


CreateScheduleOutputTypeDef = TypedDict(
    "CreateScheduleOutputTypeDef",
    {
        "ScheduleArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeadLetterConfigTypeDef = TypedDict(
    "DeadLetterConfigTypeDef",
    {
        "Arn": str,
    },
    total=False,
)

_RequiredDeleteScheduleGroupInputRequestTypeDef = TypedDict(
    "_RequiredDeleteScheduleGroupInputRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalDeleteScheduleGroupInputRequestTypeDef = TypedDict(
    "_OptionalDeleteScheduleGroupInputRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)


class DeleteScheduleGroupInputRequestTypeDef(
    _RequiredDeleteScheduleGroupInputRequestTypeDef, _OptionalDeleteScheduleGroupInputRequestTypeDef
):
    pass


_RequiredDeleteScheduleInputRequestTypeDef = TypedDict(
    "_RequiredDeleteScheduleInputRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalDeleteScheduleInputRequestTypeDef = TypedDict(
    "_OptionalDeleteScheduleInputRequestTypeDef",
    {
        "ClientToken": str,
        "GroupName": str,
    },
    total=False,
)


class DeleteScheduleInputRequestTypeDef(
    _RequiredDeleteScheduleInputRequestTypeDef, _OptionalDeleteScheduleInputRequestTypeDef
):
    pass


PlacementConstraintTypeDef = TypedDict(
    "PlacementConstraintTypeDef",
    {
        "expression": str,
        "type": PlacementConstraintTypeType,
    },
    total=False,
)

PlacementStrategyTypeDef = TypedDict(
    "PlacementStrategyTypeDef",
    {
        "field": str,
        "type": PlacementStrategyTypeType,
    },
    total=False,
)

EventBridgeParametersTypeDef = TypedDict(
    "EventBridgeParametersTypeDef",
    {
        "DetailType": str,
        "Source": str,
    },
)

GetScheduleGroupInputRequestTypeDef = TypedDict(
    "GetScheduleGroupInputRequestTypeDef",
    {
        "Name": str,
    },
)

GetScheduleGroupOutputTypeDef = TypedDict(
    "GetScheduleGroupOutputTypeDef",
    {
        "Arn": str,
        "CreationDate": datetime,
        "LastModificationDate": datetime,
        "Name": str,
        "State": ScheduleGroupStateType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetScheduleInputRequestTypeDef = TypedDict(
    "_RequiredGetScheduleInputRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalGetScheduleInputRequestTypeDef = TypedDict(
    "_OptionalGetScheduleInputRequestTypeDef",
    {
        "GroupName": str,
    },
    total=False,
)


class GetScheduleInputRequestTypeDef(
    _RequiredGetScheduleInputRequestTypeDef, _OptionalGetScheduleInputRequestTypeDef
):
    pass


KinesisParametersTypeDef = TypedDict(
    "KinesisParametersTypeDef",
    {
        "PartitionKey": str,
    },
)

ListScheduleGroupsInputListScheduleGroupsPaginateTypeDef = TypedDict(
    "ListScheduleGroupsInputListScheduleGroupsPaginateTypeDef",
    {
        "NamePrefix": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListScheduleGroupsInputRequestTypeDef = TypedDict(
    "ListScheduleGroupsInputRequestTypeDef",
    {
        "MaxResults": int,
        "NamePrefix": str,
        "NextToken": str,
    },
    total=False,
)

ScheduleGroupSummaryTypeDef = TypedDict(
    "ScheduleGroupSummaryTypeDef",
    {
        "Arn": str,
        "CreationDate": datetime,
        "LastModificationDate": datetime,
        "Name": str,
        "State": ScheduleGroupStateType,
    },
    total=False,
)

ListSchedulesInputListSchedulesPaginateTypeDef = TypedDict(
    "ListSchedulesInputListSchedulesPaginateTypeDef",
    {
        "GroupName": str,
        "NamePrefix": str,
        "State": ScheduleStateType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListSchedulesInputRequestTypeDef = TypedDict(
    "ListSchedulesInputRequestTypeDef",
    {
        "GroupName": str,
        "MaxResults": int,
        "NamePrefix": str,
        "NextToken": str,
        "State": ScheduleStateType,
    },
    total=False,
)

ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
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

RetryPolicyTypeDef = TypedDict(
    "RetryPolicyTypeDef",
    {
        "MaximumEventAgeInSeconds": int,
        "MaximumRetryAttempts": int,
    },
    total=False,
)

SageMakerPipelineParameterTypeDef = TypedDict(
    "SageMakerPipelineParameterTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)

TargetSummaryTypeDef = TypedDict(
    "TargetSummaryTypeDef",
    {
        "Arn": str,
    },
)

SqsParametersTypeDef = TypedDict(
    "SqsParametersTypeDef",
    {
        "MessageGroupId": str,
    },
    total=False,
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

UpdateScheduleOutputTypeDef = TypedDict(
    "UpdateScheduleOutputTypeDef",
    {
        "ScheduleArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

NetworkConfigurationTypeDef = TypedDict(
    "NetworkConfigurationTypeDef",
    {
        "awsvpcConfiguration": AwsVpcConfigurationTypeDef,
    },
    total=False,
)

_RequiredCreateScheduleGroupInputRequestTypeDef = TypedDict(
    "_RequiredCreateScheduleGroupInputRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateScheduleGroupInputRequestTypeDef = TypedDict(
    "_OptionalCreateScheduleGroupInputRequestTypeDef",
    {
        "ClientToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateScheduleGroupInputRequestTypeDef(
    _RequiredCreateScheduleGroupInputRequestTypeDef, _OptionalCreateScheduleGroupInputRequestTypeDef
):
    pass


ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

ListScheduleGroupsOutputTypeDef = TypedDict(
    "ListScheduleGroupsOutputTypeDef",
    {
        "NextToken": str,
        "ScheduleGroups": List[ScheduleGroupSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SageMakerPipelineParametersTypeDef = TypedDict(
    "SageMakerPipelineParametersTypeDef",
    {
        "PipelineParameterList": Sequence[SageMakerPipelineParameterTypeDef],
    },
    total=False,
)

ScheduleSummaryTypeDef = TypedDict(
    "ScheduleSummaryTypeDef",
    {
        "Arn": str,
        "CreationDate": datetime,
        "GroupName": str,
        "LastModificationDate": datetime,
        "Name": str,
        "State": ScheduleStateType,
        "Target": TargetSummaryTypeDef,
    },
    total=False,
)

_RequiredEcsParametersTypeDef = TypedDict(
    "_RequiredEcsParametersTypeDef",
    {
        "TaskDefinitionArn": str,
    },
)
_OptionalEcsParametersTypeDef = TypedDict(
    "_OptionalEcsParametersTypeDef",
    {
        "CapacityProviderStrategy": Sequence[CapacityProviderStrategyItemTypeDef],
        "EnableECSManagedTags": bool,
        "EnableExecuteCommand": bool,
        "Group": str,
        "LaunchType": LaunchTypeType,
        "NetworkConfiguration": NetworkConfigurationTypeDef,
        "PlacementConstraints": Sequence[PlacementConstraintTypeDef],
        "PlacementStrategy": Sequence[PlacementStrategyTypeDef],
        "PlatformVersion": str,
        "PropagateTags": Literal["TASK_DEFINITION"],
        "ReferenceId": str,
        "Tags": Sequence[Mapping[str, str]],
        "TaskCount": int,
    },
    total=False,
)


class EcsParametersTypeDef(_RequiredEcsParametersTypeDef, _OptionalEcsParametersTypeDef):
    pass


ListSchedulesOutputTypeDef = TypedDict(
    "ListSchedulesOutputTypeDef",
    {
        "NextToken": str,
        "Schedules": List[ScheduleSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredTargetTypeDef = TypedDict(
    "_RequiredTargetTypeDef",
    {
        "Arn": str,
        "RoleArn": str,
    },
)
_OptionalTargetTypeDef = TypedDict(
    "_OptionalTargetTypeDef",
    {
        "DeadLetterConfig": DeadLetterConfigTypeDef,
        "EcsParameters": EcsParametersTypeDef,
        "EventBridgeParameters": EventBridgeParametersTypeDef,
        "Input": str,
        "KinesisParameters": KinesisParametersTypeDef,
        "RetryPolicy": RetryPolicyTypeDef,
        "SageMakerPipelineParameters": SageMakerPipelineParametersTypeDef,
        "SqsParameters": SqsParametersTypeDef,
    },
    total=False,
)


class TargetTypeDef(_RequiredTargetTypeDef, _OptionalTargetTypeDef):
    pass


_RequiredCreateScheduleInputRequestTypeDef = TypedDict(
    "_RequiredCreateScheduleInputRequestTypeDef",
    {
        "FlexibleTimeWindow": FlexibleTimeWindowTypeDef,
        "Name": str,
        "ScheduleExpression": str,
        "Target": TargetTypeDef,
    },
)
_OptionalCreateScheduleInputRequestTypeDef = TypedDict(
    "_OptionalCreateScheduleInputRequestTypeDef",
    {
        "ClientToken": str,
        "Description": str,
        "EndDate": Union[datetime, str],
        "GroupName": str,
        "KmsKeyArn": str,
        "ScheduleExpressionTimezone": str,
        "StartDate": Union[datetime, str],
        "State": ScheduleStateType,
    },
    total=False,
)


class CreateScheduleInputRequestTypeDef(
    _RequiredCreateScheduleInputRequestTypeDef, _OptionalCreateScheduleInputRequestTypeDef
):
    pass


GetScheduleOutputTypeDef = TypedDict(
    "GetScheduleOutputTypeDef",
    {
        "Arn": str,
        "CreationDate": datetime,
        "Description": str,
        "EndDate": datetime,
        "FlexibleTimeWindow": FlexibleTimeWindowTypeDef,
        "GroupName": str,
        "KmsKeyArn": str,
        "LastModificationDate": datetime,
        "Name": str,
        "ScheduleExpression": str,
        "ScheduleExpressionTimezone": str,
        "StartDate": datetime,
        "State": ScheduleStateType,
        "Target": TargetTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateScheduleInputRequestTypeDef = TypedDict(
    "_RequiredUpdateScheduleInputRequestTypeDef",
    {
        "FlexibleTimeWindow": FlexibleTimeWindowTypeDef,
        "Name": str,
        "ScheduleExpression": str,
        "Target": TargetTypeDef,
    },
)
_OptionalUpdateScheduleInputRequestTypeDef = TypedDict(
    "_OptionalUpdateScheduleInputRequestTypeDef",
    {
        "ClientToken": str,
        "Description": str,
        "EndDate": Union[datetime, str],
        "GroupName": str,
        "KmsKeyArn": str,
        "ScheduleExpressionTimezone": str,
        "StartDate": Union[datetime, str],
        "State": ScheduleStateType,
    },
    total=False,
)


class UpdateScheduleInputRequestTypeDef(
    _RequiredUpdateScheduleInputRequestTypeDef, _OptionalUpdateScheduleInputRequestTypeDef
):
    pass
