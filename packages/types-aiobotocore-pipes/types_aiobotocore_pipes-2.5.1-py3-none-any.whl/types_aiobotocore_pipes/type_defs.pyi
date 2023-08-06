"""
Type annotations for pipes service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pipes/type_defs/)

Usage::

    ```python
    from types_aiobotocore_pipes.type_defs import AwsVpcConfigurationTypeDef

    data: AwsVpcConfigurationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AssignPublicIpType,
    BatchJobDependencyTypeType,
    BatchResourceRequirementTypeType,
    DynamoDBStreamStartPositionType,
    EcsResourceRequirementTypeType,
    KinesisStreamStartPositionType,
    LaunchTypeType,
    MSKStartPositionType,
    PipeStateType,
    PipeTargetInvocationTypeType,
    PlacementConstraintTypeType,
    PlacementStrategyTypeType,
    RequestedPipeStateDescribeResponseType,
    RequestedPipeStateType,
    SelfManagedKafkaStartPositionType,
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
    "BatchArrayPropertiesTypeDef",
    "BatchEnvironmentVariableTypeDef",
    "BatchResourceRequirementTypeDef",
    "BatchJobDependencyTypeDef",
    "BatchRetryStrategyTypeDef",
    "CapacityProviderStrategyItemTypeDef",
    "CreatePipeResponseTypeDef",
    "DeadLetterConfigTypeDef",
    "DeletePipeRequestRequestTypeDef",
    "DeletePipeResponseTypeDef",
    "DescribePipeRequestRequestTypeDef",
    "EcsEnvironmentFileTypeDef",
    "EcsEnvironmentVariableTypeDef",
    "EcsResourceRequirementTypeDef",
    "EcsEphemeralStorageTypeDef",
    "EcsInferenceAcceleratorOverrideTypeDef",
    "FilterTypeDef",
    "ListPipesRequestListPipesPaginateTypeDef",
    "ListPipesRequestRequestTypeDef",
    "PipeTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MQBrokerAccessCredentialsTypeDef",
    "MSKAccessCredentialsTypeDef",
    "PaginatorConfigTypeDef",
    "PipeEnrichmentHttpParametersTypeDef",
    "PipeSourceSqsQueueParametersTypeDef",
    "SelfManagedKafkaAccessConfigurationCredentialsTypeDef",
    "SelfManagedKafkaAccessConfigurationVpcTypeDef",
    "PipeTargetCloudWatchLogsParametersTypeDef",
    "PlacementConstraintTypeDef",
    "PlacementStrategyTypeDef",
    "TagTypeDef",
    "PipeTargetEventBridgeEventBusParametersTypeDef",
    "PipeTargetHttpParametersTypeDef",
    "PipeTargetKinesisStreamParametersTypeDef",
    "PipeTargetLambdaFunctionParametersTypeDef",
    "PipeTargetRedshiftDataParametersTypeDef",
    "PipeTargetSqsQueueParametersTypeDef",
    "PipeTargetStateMachineParametersTypeDef",
    "SageMakerPipelineParameterTypeDef",
    "ResponseMetadataTypeDef",
    "StartPipeRequestRequestTypeDef",
    "StartPipeResponseTypeDef",
    "StopPipeRequestRequestTypeDef",
    "StopPipeResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdatePipeResponseTypeDef",
    "UpdatePipeSourceSqsQueueParametersTypeDef",
    "NetworkConfigurationTypeDef",
    "BatchContainerOverridesTypeDef",
    "PipeSourceDynamoDBStreamParametersTypeDef",
    "PipeSourceKinesisStreamParametersTypeDef",
    "UpdatePipeSourceDynamoDBStreamParametersTypeDef",
    "UpdatePipeSourceKinesisStreamParametersTypeDef",
    "EcsContainerOverrideTypeDef",
    "FilterCriteriaTypeDef",
    "ListPipesResponseTypeDef",
    "PipeSourceActiveMQBrokerParametersTypeDef",
    "PipeSourceRabbitMQBrokerParametersTypeDef",
    "UpdatePipeSourceActiveMQBrokerParametersTypeDef",
    "UpdatePipeSourceRabbitMQBrokerParametersTypeDef",
    "PipeSourceManagedStreamingKafkaParametersTypeDef",
    "UpdatePipeSourceManagedStreamingKafkaParametersTypeDef",
    "PipeEnrichmentParametersTypeDef",
    "PipeSourceSelfManagedKafkaParametersTypeDef",
    "UpdatePipeSourceSelfManagedKafkaParametersTypeDef",
    "PipeTargetSageMakerPipelineParametersTypeDef",
    "PipeTargetBatchJobParametersTypeDef",
    "EcsTaskOverrideTypeDef",
    "PipeSourceParametersTypeDef",
    "UpdatePipeSourceParametersTypeDef",
    "PipeTargetEcsTaskParametersTypeDef",
    "PipeTargetParametersTypeDef",
    "CreatePipeRequestRequestTypeDef",
    "DescribePipeResponseTypeDef",
    "UpdatePipeRequestRequestTypeDef",
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

BatchArrayPropertiesTypeDef = TypedDict(
    "BatchArrayPropertiesTypeDef",
    {
        "Size": int,
    },
    total=False,
)

BatchEnvironmentVariableTypeDef = TypedDict(
    "BatchEnvironmentVariableTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

BatchResourceRequirementTypeDef = TypedDict(
    "BatchResourceRequirementTypeDef",
    {
        "Type": BatchResourceRequirementTypeType,
        "Value": str,
    },
)

BatchJobDependencyTypeDef = TypedDict(
    "BatchJobDependencyTypeDef",
    {
        "JobId": str,
        "Type": BatchJobDependencyTypeType,
    },
    total=False,
)

BatchRetryStrategyTypeDef = TypedDict(
    "BatchRetryStrategyTypeDef",
    {
        "Attempts": int,
    },
    total=False,
)

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

CreatePipeResponseTypeDef = TypedDict(
    "CreatePipeResponseTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "CurrentState": PipeStateType,
        "DesiredState": RequestedPipeStateType,
        "LastModifiedTime": datetime,
        "Name": str,
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

DeletePipeRequestRequestTypeDef = TypedDict(
    "DeletePipeRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeletePipeResponseTypeDef = TypedDict(
    "DeletePipeResponseTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "CurrentState": PipeStateType,
        "DesiredState": RequestedPipeStateDescribeResponseType,
        "LastModifiedTime": datetime,
        "Name": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribePipeRequestRequestTypeDef = TypedDict(
    "DescribePipeRequestRequestTypeDef",
    {
        "Name": str,
    },
)

EcsEnvironmentFileTypeDef = TypedDict(
    "EcsEnvironmentFileTypeDef",
    {
        "type": Literal["s3"],
        "value": str,
    },
)

EcsEnvironmentVariableTypeDef = TypedDict(
    "EcsEnvironmentVariableTypeDef",
    {
        "name": str,
        "value": str,
    },
    total=False,
)

EcsResourceRequirementTypeDef = TypedDict(
    "EcsResourceRequirementTypeDef",
    {
        "type": EcsResourceRequirementTypeType,
        "value": str,
    },
)

EcsEphemeralStorageTypeDef = TypedDict(
    "EcsEphemeralStorageTypeDef",
    {
        "sizeInGiB": int,
    },
)

EcsInferenceAcceleratorOverrideTypeDef = TypedDict(
    "EcsInferenceAcceleratorOverrideTypeDef",
    {
        "deviceName": str,
        "deviceType": str,
    },
    total=False,
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Pattern": str,
    },
    total=False,
)

ListPipesRequestListPipesPaginateTypeDef = TypedDict(
    "ListPipesRequestListPipesPaginateTypeDef",
    {
        "CurrentState": PipeStateType,
        "DesiredState": RequestedPipeStateType,
        "NamePrefix": str,
        "SourcePrefix": str,
        "TargetPrefix": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListPipesRequestRequestTypeDef = TypedDict(
    "ListPipesRequestRequestTypeDef",
    {
        "CurrentState": PipeStateType,
        "DesiredState": RequestedPipeStateType,
        "Limit": int,
        "NamePrefix": str,
        "NextToken": str,
        "SourcePrefix": str,
        "TargetPrefix": str,
    },
    total=False,
)

PipeTypeDef = TypedDict(
    "PipeTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "CurrentState": PipeStateType,
        "DesiredState": RequestedPipeStateType,
        "Enrichment": str,
        "LastModifiedTime": datetime,
        "Name": str,
        "Source": str,
        "StateReason": str,
        "Target": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

MQBrokerAccessCredentialsTypeDef = TypedDict(
    "MQBrokerAccessCredentialsTypeDef",
    {
        "BasicAuth": str,
    },
    total=False,
)

MSKAccessCredentialsTypeDef = TypedDict(
    "MSKAccessCredentialsTypeDef",
    {
        "ClientCertificateTlsAuth": str,
        "SaslScram512Auth": str,
    },
    total=False,
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

PipeEnrichmentHttpParametersTypeDef = TypedDict(
    "PipeEnrichmentHttpParametersTypeDef",
    {
        "HeaderParameters": Mapping[str, str],
        "PathParameterValues": Sequence[str],
        "QueryStringParameters": Mapping[str, str],
    },
    total=False,
)

PipeSourceSqsQueueParametersTypeDef = TypedDict(
    "PipeSourceSqsQueueParametersTypeDef",
    {
        "BatchSize": int,
        "MaximumBatchingWindowInSeconds": int,
    },
    total=False,
)

SelfManagedKafkaAccessConfigurationCredentialsTypeDef = TypedDict(
    "SelfManagedKafkaAccessConfigurationCredentialsTypeDef",
    {
        "BasicAuth": str,
        "ClientCertificateTlsAuth": str,
        "SaslScram256Auth": str,
        "SaslScram512Auth": str,
    },
    total=False,
)

SelfManagedKafkaAccessConfigurationVpcTypeDef = TypedDict(
    "SelfManagedKafkaAccessConfigurationVpcTypeDef",
    {
        "SecurityGroup": Sequence[str],
        "Subnets": Sequence[str],
    },
    total=False,
)

PipeTargetCloudWatchLogsParametersTypeDef = TypedDict(
    "PipeTargetCloudWatchLogsParametersTypeDef",
    {
        "LogStreamName": str,
        "Timestamp": str,
    },
    total=False,
)

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

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

PipeTargetEventBridgeEventBusParametersTypeDef = TypedDict(
    "PipeTargetEventBridgeEventBusParametersTypeDef",
    {
        "DetailType": str,
        "EndpointId": str,
        "Resources": Sequence[str],
        "Source": str,
        "Time": str,
    },
    total=False,
)

PipeTargetHttpParametersTypeDef = TypedDict(
    "PipeTargetHttpParametersTypeDef",
    {
        "HeaderParameters": Mapping[str, str],
        "PathParameterValues": Sequence[str],
        "QueryStringParameters": Mapping[str, str],
    },
    total=False,
)

PipeTargetKinesisStreamParametersTypeDef = TypedDict(
    "PipeTargetKinesisStreamParametersTypeDef",
    {
        "PartitionKey": str,
    },
)

PipeTargetLambdaFunctionParametersTypeDef = TypedDict(
    "PipeTargetLambdaFunctionParametersTypeDef",
    {
        "InvocationType": PipeTargetInvocationTypeType,
    },
    total=False,
)

_RequiredPipeTargetRedshiftDataParametersTypeDef = TypedDict(
    "_RequiredPipeTargetRedshiftDataParametersTypeDef",
    {
        "Database": str,
        "Sqls": Sequence[str],
    },
)
_OptionalPipeTargetRedshiftDataParametersTypeDef = TypedDict(
    "_OptionalPipeTargetRedshiftDataParametersTypeDef",
    {
        "DbUser": str,
        "SecretManagerArn": str,
        "StatementName": str,
        "WithEvent": bool,
    },
    total=False,
)

class PipeTargetRedshiftDataParametersTypeDef(
    _RequiredPipeTargetRedshiftDataParametersTypeDef,
    _OptionalPipeTargetRedshiftDataParametersTypeDef,
):
    pass

PipeTargetSqsQueueParametersTypeDef = TypedDict(
    "PipeTargetSqsQueueParametersTypeDef",
    {
        "MessageDeduplicationId": str,
        "MessageGroupId": str,
    },
    total=False,
)

PipeTargetStateMachineParametersTypeDef = TypedDict(
    "PipeTargetStateMachineParametersTypeDef",
    {
        "InvocationType": PipeTargetInvocationTypeType,
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

StartPipeRequestRequestTypeDef = TypedDict(
    "StartPipeRequestRequestTypeDef",
    {
        "Name": str,
    },
)

StartPipeResponseTypeDef = TypedDict(
    "StartPipeResponseTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "CurrentState": PipeStateType,
        "DesiredState": RequestedPipeStateType,
        "LastModifiedTime": datetime,
        "Name": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopPipeRequestRequestTypeDef = TypedDict(
    "StopPipeRequestRequestTypeDef",
    {
        "Name": str,
    },
)

StopPipeResponseTypeDef = TypedDict(
    "StopPipeResponseTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "CurrentState": PipeStateType,
        "DesiredState": RequestedPipeStateType,
        "LastModifiedTime": datetime,
        "Name": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

UpdatePipeResponseTypeDef = TypedDict(
    "UpdatePipeResponseTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "CurrentState": PipeStateType,
        "DesiredState": RequestedPipeStateType,
        "LastModifiedTime": datetime,
        "Name": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdatePipeSourceSqsQueueParametersTypeDef = TypedDict(
    "UpdatePipeSourceSqsQueueParametersTypeDef",
    {
        "BatchSize": int,
        "MaximumBatchingWindowInSeconds": int,
    },
    total=False,
)

NetworkConfigurationTypeDef = TypedDict(
    "NetworkConfigurationTypeDef",
    {
        "awsvpcConfiguration": AwsVpcConfigurationTypeDef,
    },
    total=False,
)

BatchContainerOverridesTypeDef = TypedDict(
    "BatchContainerOverridesTypeDef",
    {
        "Command": Sequence[str],
        "Environment": Sequence[BatchEnvironmentVariableTypeDef],
        "InstanceType": str,
        "ResourceRequirements": Sequence[BatchResourceRequirementTypeDef],
    },
    total=False,
)

_RequiredPipeSourceDynamoDBStreamParametersTypeDef = TypedDict(
    "_RequiredPipeSourceDynamoDBStreamParametersTypeDef",
    {
        "StartingPosition": DynamoDBStreamStartPositionType,
    },
)
_OptionalPipeSourceDynamoDBStreamParametersTypeDef = TypedDict(
    "_OptionalPipeSourceDynamoDBStreamParametersTypeDef",
    {
        "BatchSize": int,
        "DeadLetterConfig": DeadLetterConfigTypeDef,
        "MaximumBatchingWindowInSeconds": int,
        "MaximumRecordAgeInSeconds": int,
        "MaximumRetryAttempts": int,
        "OnPartialBatchItemFailure": Literal["AUTOMATIC_BISECT"],
        "ParallelizationFactor": int,
    },
    total=False,
)

class PipeSourceDynamoDBStreamParametersTypeDef(
    _RequiredPipeSourceDynamoDBStreamParametersTypeDef,
    _OptionalPipeSourceDynamoDBStreamParametersTypeDef,
):
    pass

_RequiredPipeSourceKinesisStreamParametersTypeDef = TypedDict(
    "_RequiredPipeSourceKinesisStreamParametersTypeDef",
    {
        "StartingPosition": KinesisStreamStartPositionType,
    },
)
_OptionalPipeSourceKinesisStreamParametersTypeDef = TypedDict(
    "_OptionalPipeSourceKinesisStreamParametersTypeDef",
    {
        "BatchSize": int,
        "DeadLetterConfig": DeadLetterConfigTypeDef,
        "MaximumBatchingWindowInSeconds": int,
        "MaximumRecordAgeInSeconds": int,
        "MaximumRetryAttempts": int,
        "OnPartialBatchItemFailure": Literal["AUTOMATIC_BISECT"],
        "ParallelizationFactor": int,
        "StartingPositionTimestamp": Union[datetime, str],
    },
    total=False,
)

class PipeSourceKinesisStreamParametersTypeDef(
    _RequiredPipeSourceKinesisStreamParametersTypeDef,
    _OptionalPipeSourceKinesisStreamParametersTypeDef,
):
    pass

UpdatePipeSourceDynamoDBStreamParametersTypeDef = TypedDict(
    "UpdatePipeSourceDynamoDBStreamParametersTypeDef",
    {
        "BatchSize": int,
        "DeadLetterConfig": DeadLetterConfigTypeDef,
        "MaximumBatchingWindowInSeconds": int,
        "MaximumRecordAgeInSeconds": int,
        "MaximumRetryAttempts": int,
        "OnPartialBatchItemFailure": Literal["AUTOMATIC_BISECT"],
        "ParallelizationFactor": int,
    },
    total=False,
)

UpdatePipeSourceKinesisStreamParametersTypeDef = TypedDict(
    "UpdatePipeSourceKinesisStreamParametersTypeDef",
    {
        "BatchSize": int,
        "DeadLetterConfig": DeadLetterConfigTypeDef,
        "MaximumBatchingWindowInSeconds": int,
        "MaximumRecordAgeInSeconds": int,
        "MaximumRetryAttempts": int,
        "OnPartialBatchItemFailure": Literal["AUTOMATIC_BISECT"],
        "ParallelizationFactor": int,
    },
    total=False,
)

EcsContainerOverrideTypeDef = TypedDict(
    "EcsContainerOverrideTypeDef",
    {
        "Command": Sequence[str],
        "Cpu": int,
        "Environment": Sequence[EcsEnvironmentVariableTypeDef],
        "EnvironmentFiles": Sequence[EcsEnvironmentFileTypeDef],
        "Memory": int,
        "MemoryReservation": int,
        "Name": str,
        "ResourceRequirements": Sequence[EcsResourceRequirementTypeDef],
    },
    total=False,
)

FilterCriteriaTypeDef = TypedDict(
    "FilterCriteriaTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

ListPipesResponseTypeDef = TypedDict(
    "ListPipesResponseTypeDef",
    {
        "NextToken": str,
        "Pipes": List[PipeTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredPipeSourceActiveMQBrokerParametersTypeDef = TypedDict(
    "_RequiredPipeSourceActiveMQBrokerParametersTypeDef",
    {
        "Credentials": MQBrokerAccessCredentialsTypeDef,
        "QueueName": str,
    },
)
_OptionalPipeSourceActiveMQBrokerParametersTypeDef = TypedDict(
    "_OptionalPipeSourceActiveMQBrokerParametersTypeDef",
    {
        "BatchSize": int,
        "MaximumBatchingWindowInSeconds": int,
    },
    total=False,
)

class PipeSourceActiveMQBrokerParametersTypeDef(
    _RequiredPipeSourceActiveMQBrokerParametersTypeDef,
    _OptionalPipeSourceActiveMQBrokerParametersTypeDef,
):
    pass

_RequiredPipeSourceRabbitMQBrokerParametersTypeDef = TypedDict(
    "_RequiredPipeSourceRabbitMQBrokerParametersTypeDef",
    {
        "Credentials": MQBrokerAccessCredentialsTypeDef,
        "QueueName": str,
    },
)
_OptionalPipeSourceRabbitMQBrokerParametersTypeDef = TypedDict(
    "_OptionalPipeSourceRabbitMQBrokerParametersTypeDef",
    {
        "BatchSize": int,
        "MaximumBatchingWindowInSeconds": int,
        "VirtualHost": str,
    },
    total=False,
)

class PipeSourceRabbitMQBrokerParametersTypeDef(
    _RequiredPipeSourceRabbitMQBrokerParametersTypeDef,
    _OptionalPipeSourceRabbitMQBrokerParametersTypeDef,
):
    pass

_RequiredUpdatePipeSourceActiveMQBrokerParametersTypeDef = TypedDict(
    "_RequiredUpdatePipeSourceActiveMQBrokerParametersTypeDef",
    {
        "Credentials": MQBrokerAccessCredentialsTypeDef,
    },
)
_OptionalUpdatePipeSourceActiveMQBrokerParametersTypeDef = TypedDict(
    "_OptionalUpdatePipeSourceActiveMQBrokerParametersTypeDef",
    {
        "BatchSize": int,
        "MaximumBatchingWindowInSeconds": int,
    },
    total=False,
)

class UpdatePipeSourceActiveMQBrokerParametersTypeDef(
    _RequiredUpdatePipeSourceActiveMQBrokerParametersTypeDef,
    _OptionalUpdatePipeSourceActiveMQBrokerParametersTypeDef,
):
    pass

_RequiredUpdatePipeSourceRabbitMQBrokerParametersTypeDef = TypedDict(
    "_RequiredUpdatePipeSourceRabbitMQBrokerParametersTypeDef",
    {
        "Credentials": MQBrokerAccessCredentialsTypeDef,
    },
)
_OptionalUpdatePipeSourceRabbitMQBrokerParametersTypeDef = TypedDict(
    "_OptionalUpdatePipeSourceRabbitMQBrokerParametersTypeDef",
    {
        "BatchSize": int,
        "MaximumBatchingWindowInSeconds": int,
    },
    total=False,
)

class UpdatePipeSourceRabbitMQBrokerParametersTypeDef(
    _RequiredUpdatePipeSourceRabbitMQBrokerParametersTypeDef,
    _OptionalUpdatePipeSourceRabbitMQBrokerParametersTypeDef,
):
    pass

_RequiredPipeSourceManagedStreamingKafkaParametersTypeDef = TypedDict(
    "_RequiredPipeSourceManagedStreamingKafkaParametersTypeDef",
    {
        "TopicName": str,
    },
)
_OptionalPipeSourceManagedStreamingKafkaParametersTypeDef = TypedDict(
    "_OptionalPipeSourceManagedStreamingKafkaParametersTypeDef",
    {
        "BatchSize": int,
        "ConsumerGroupID": str,
        "Credentials": MSKAccessCredentialsTypeDef,
        "MaximumBatchingWindowInSeconds": int,
        "StartingPosition": MSKStartPositionType,
    },
    total=False,
)

class PipeSourceManagedStreamingKafkaParametersTypeDef(
    _RequiredPipeSourceManagedStreamingKafkaParametersTypeDef,
    _OptionalPipeSourceManagedStreamingKafkaParametersTypeDef,
):
    pass

UpdatePipeSourceManagedStreamingKafkaParametersTypeDef = TypedDict(
    "UpdatePipeSourceManagedStreamingKafkaParametersTypeDef",
    {
        "BatchSize": int,
        "Credentials": MSKAccessCredentialsTypeDef,
        "MaximumBatchingWindowInSeconds": int,
    },
    total=False,
)

PipeEnrichmentParametersTypeDef = TypedDict(
    "PipeEnrichmentParametersTypeDef",
    {
        "HttpParameters": PipeEnrichmentHttpParametersTypeDef,
        "InputTemplate": str,
    },
    total=False,
)

_RequiredPipeSourceSelfManagedKafkaParametersTypeDef = TypedDict(
    "_RequiredPipeSourceSelfManagedKafkaParametersTypeDef",
    {
        "TopicName": str,
    },
)
_OptionalPipeSourceSelfManagedKafkaParametersTypeDef = TypedDict(
    "_OptionalPipeSourceSelfManagedKafkaParametersTypeDef",
    {
        "AdditionalBootstrapServers": Sequence[str],
        "BatchSize": int,
        "ConsumerGroupID": str,
        "Credentials": SelfManagedKafkaAccessConfigurationCredentialsTypeDef,
        "MaximumBatchingWindowInSeconds": int,
        "ServerRootCaCertificate": str,
        "StartingPosition": SelfManagedKafkaStartPositionType,
        "Vpc": SelfManagedKafkaAccessConfigurationVpcTypeDef,
    },
    total=False,
)

class PipeSourceSelfManagedKafkaParametersTypeDef(
    _RequiredPipeSourceSelfManagedKafkaParametersTypeDef,
    _OptionalPipeSourceSelfManagedKafkaParametersTypeDef,
):
    pass

UpdatePipeSourceSelfManagedKafkaParametersTypeDef = TypedDict(
    "UpdatePipeSourceSelfManagedKafkaParametersTypeDef",
    {
        "BatchSize": int,
        "Credentials": SelfManagedKafkaAccessConfigurationCredentialsTypeDef,
        "MaximumBatchingWindowInSeconds": int,
        "ServerRootCaCertificate": str,
        "Vpc": SelfManagedKafkaAccessConfigurationVpcTypeDef,
    },
    total=False,
)

PipeTargetSageMakerPipelineParametersTypeDef = TypedDict(
    "PipeTargetSageMakerPipelineParametersTypeDef",
    {
        "PipelineParameterList": Sequence[SageMakerPipelineParameterTypeDef],
    },
    total=False,
)

_RequiredPipeTargetBatchJobParametersTypeDef = TypedDict(
    "_RequiredPipeTargetBatchJobParametersTypeDef",
    {
        "JobDefinition": str,
        "JobName": str,
    },
)
_OptionalPipeTargetBatchJobParametersTypeDef = TypedDict(
    "_OptionalPipeTargetBatchJobParametersTypeDef",
    {
        "ArrayProperties": BatchArrayPropertiesTypeDef,
        "ContainerOverrides": BatchContainerOverridesTypeDef,
        "DependsOn": Sequence[BatchJobDependencyTypeDef],
        "Parameters": Mapping[str, str],
        "RetryStrategy": BatchRetryStrategyTypeDef,
    },
    total=False,
)

class PipeTargetBatchJobParametersTypeDef(
    _RequiredPipeTargetBatchJobParametersTypeDef, _OptionalPipeTargetBatchJobParametersTypeDef
):
    pass

EcsTaskOverrideTypeDef = TypedDict(
    "EcsTaskOverrideTypeDef",
    {
        "ContainerOverrides": Sequence[EcsContainerOverrideTypeDef],
        "Cpu": str,
        "EphemeralStorage": EcsEphemeralStorageTypeDef,
        "ExecutionRoleArn": str,
        "InferenceAcceleratorOverrides": Sequence[EcsInferenceAcceleratorOverrideTypeDef],
        "Memory": str,
        "TaskRoleArn": str,
    },
    total=False,
)

PipeSourceParametersTypeDef = TypedDict(
    "PipeSourceParametersTypeDef",
    {
        "ActiveMQBrokerParameters": PipeSourceActiveMQBrokerParametersTypeDef,
        "DynamoDBStreamParameters": PipeSourceDynamoDBStreamParametersTypeDef,
        "FilterCriteria": FilterCriteriaTypeDef,
        "KinesisStreamParameters": PipeSourceKinesisStreamParametersTypeDef,
        "ManagedStreamingKafkaParameters": PipeSourceManagedStreamingKafkaParametersTypeDef,
        "RabbitMQBrokerParameters": PipeSourceRabbitMQBrokerParametersTypeDef,
        "SelfManagedKafkaParameters": PipeSourceSelfManagedKafkaParametersTypeDef,
        "SqsQueueParameters": PipeSourceSqsQueueParametersTypeDef,
    },
    total=False,
)

UpdatePipeSourceParametersTypeDef = TypedDict(
    "UpdatePipeSourceParametersTypeDef",
    {
        "ActiveMQBrokerParameters": UpdatePipeSourceActiveMQBrokerParametersTypeDef,
        "DynamoDBStreamParameters": UpdatePipeSourceDynamoDBStreamParametersTypeDef,
        "FilterCriteria": FilterCriteriaTypeDef,
        "KinesisStreamParameters": UpdatePipeSourceKinesisStreamParametersTypeDef,
        "ManagedStreamingKafkaParameters": UpdatePipeSourceManagedStreamingKafkaParametersTypeDef,
        "RabbitMQBrokerParameters": UpdatePipeSourceRabbitMQBrokerParametersTypeDef,
        "SelfManagedKafkaParameters": UpdatePipeSourceSelfManagedKafkaParametersTypeDef,
        "SqsQueueParameters": UpdatePipeSourceSqsQueueParametersTypeDef,
    },
    total=False,
)

_RequiredPipeTargetEcsTaskParametersTypeDef = TypedDict(
    "_RequiredPipeTargetEcsTaskParametersTypeDef",
    {
        "TaskDefinitionArn": str,
    },
)
_OptionalPipeTargetEcsTaskParametersTypeDef = TypedDict(
    "_OptionalPipeTargetEcsTaskParametersTypeDef",
    {
        "CapacityProviderStrategy": Sequence[CapacityProviderStrategyItemTypeDef],
        "EnableECSManagedTags": bool,
        "EnableExecuteCommand": bool,
        "Group": str,
        "LaunchType": LaunchTypeType,
        "NetworkConfiguration": NetworkConfigurationTypeDef,
        "Overrides": EcsTaskOverrideTypeDef,
        "PlacementConstraints": Sequence[PlacementConstraintTypeDef],
        "PlacementStrategy": Sequence[PlacementStrategyTypeDef],
        "PlatformVersion": str,
        "PropagateTags": Literal["TASK_DEFINITION"],
        "ReferenceId": str,
        "Tags": Sequence[TagTypeDef],
        "TaskCount": int,
    },
    total=False,
)

class PipeTargetEcsTaskParametersTypeDef(
    _RequiredPipeTargetEcsTaskParametersTypeDef, _OptionalPipeTargetEcsTaskParametersTypeDef
):
    pass

PipeTargetParametersTypeDef = TypedDict(
    "PipeTargetParametersTypeDef",
    {
        "BatchJobParameters": PipeTargetBatchJobParametersTypeDef,
        "CloudWatchLogsParameters": PipeTargetCloudWatchLogsParametersTypeDef,
        "EcsTaskParameters": PipeTargetEcsTaskParametersTypeDef,
        "EventBridgeEventBusParameters": PipeTargetEventBridgeEventBusParametersTypeDef,
        "HttpParameters": PipeTargetHttpParametersTypeDef,
        "InputTemplate": str,
        "KinesisStreamParameters": PipeTargetKinesisStreamParametersTypeDef,
        "LambdaFunctionParameters": PipeTargetLambdaFunctionParametersTypeDef,
        "RedshiftDataParameters": PipeTargetRedshiftDataParametersTypeDef,
        "SageMakerPipelineParameters": PipeTargetSageMakerPipelineParametersTypeDef,
        "SqsQueueParameters": PipeTargetSqsQueueParametersTypeDef,
        "StepFunctionStateMachineParameters": PipeTargetStateMachineParametersTypeDef,
    },
    total=False,
)

_RequiredCreatePipeRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePipeRequestRequestTypeDef",
    {
        "Name": str,
        "RoleArn": str,
        "Source": str,
        "Target": str,
    },
)
_OptionalCreatePipeRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePipeRequestRequestTypeDef",
    {
        "Description": str,
        "DesiredState": RequestedPipeStateType,
        "Enrichment": str,
        "EnrichmentParameters": PipeEnrichmentParametersTypeDef,
        "SourceParameters": PipeSourceParametersTypeDef,
        "Tags": Mapping[str, str],
        "TargetParameters": PipeTargetParametersTypeDef,
    },
    total=False,
)

class CreatePipeRequestRequestTypeDef(
    _RequiredCreatePipeRequestRequestTypeDef, _OptionalCreatePipeRequestRequestTypeDef
):
    pass

DescribePipeResponseTypeDef = TypedDict(
    "DescribePipeResponseTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "CurrentState": PipeStateType,
        "Description": str,
        "DesiredState": RequestedPipeStateDescribeResponseType,
        "Enrichment": str,
        "EnrichmentParameters": PipeEnrichmentParametersTypeDef,
        "LastModifiedTime": datetime,
        "Name": str,
        "RoleArn": str,
        "Source": str,
        "SourceParameters": PipeSourceParametersTypeDef,
        "StateReason": str,
        "Tags": Dict[str, str],
        "Target": str,
        "TargetParameters": PipeTargetParametersTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdatePipeRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePipeRequestRequestTypeDef",
    {
        "Name": str,
        "RoleArn": str,
    },
)
_OptionalUpdatePipeRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePipeRequestRequestTypeDef",
    {
        "Description": str,
        "DesiredState": RequestedPipeStateType,
        "Enrichment": str,
        "EnrichmentParameters": PipeEnrichmentParametersTypeDef,
        "SourceParameters": UpdatePipeSourceParametersTypeDef,
        "Target": str,
        "TargetParameters": PipeTargetParametersTypeDef,
    },
    total=False,
)

class UpdatePipeRequestRequestTypeDef(
    _RequiredUpdatePipeRequestRequestTypeDef, _OptionalUpdatePipeRequestRequestTypeDef
):
    pass
