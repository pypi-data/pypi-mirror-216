"""
Type annotations for securitylake service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/type_defs/)

Usage::

    ```python
    from types_aiobotocore_securitylake.type_defs import AwsIdentityTypeDef

    data: AwsIdentityTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence

from .literals import (
    AccessTypeType,
    AwsLogSourceNameType,
    DataLakeStatusType,
    HttpMethodType,
    SourceCollectionStatusType,
    SubscriberStatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AwsIdentityTypeDef",
    "AwsLogSourceConfigurationTypeDef",
    "AwsLogSourceResourceTypeDef",
    "CreateAwsLogSourceResponseTypeDef",
    "CreateDataLakeExceptionSubscriptionRequestRequestTypeDef",
    "CreateSubscriberNotificationResponseTypeDef",
    "CustomLogSourceAttributesTypeDef",
    "CustomLogSourceCrawlerConfigurationTypeDef",
    "CustomLogSourceProviderTypeDef",
    "DataLakeEncryptionConfigurationTypeDef",
    "DataLakeReplicationConfigurationTypeDef",
    "DataLakeExceptionTypeDef",
    "DataLakeLifecycleExpirationTypeDef",
    "DataLakeLifecycleTransitionTypeDef",
    "DataLakeSourceStatusTypeDef",
    "DataLakeUpdateExceptionTypeDef",
    "DeleteAwsLogSourceResponseTypeDef",
    "DeleteCustomLogSourceRequestRequestTypeDef",
    "DeleteDataLakeRequestRequestTypeDef",
    "DeleteSubscriberNotificationRequestRequestTypeDef",
    "DeleteSubscriberRequestRequestTypeDef",
    "GetDataLakeExceptionSubscriptionResponseTypeDef",
    "GetDataLakeSourcesRequestGetDataLakeSourcesPaginateTypeDef",
    "GetDataLakeSourcesRequestRequestTypeDef",
    "GetSubscriberRequestRequestTypeDef",
    "HttpsNotificationConfigurationTypeDef",
    "ListDataLakeExceptionsRequestListDataLakeExceptionsPaginateTypeDef",
    "ListDataLakeExceptionsRequestRequestTypeDef",
    "ListDataLakesRequestRequestTypeDef",
    "ListSubscribersRequestListSubscribersPaginateTypeDef",
    "ListSubscribersRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "RegisterDataLakeDelegatedAdministratorRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "UpdateDataLakeExceptionSubscriptionRequestRequestTypeDef",
    "UpdateSubscriberNotificationResponseTypeDef",
    "CreateAwsLogSourceRequestRequestTypeDef",
    "DeleteAwsLogSourceRequestRequestTypeDef",
    "DataLakeAutoEnableNewAccountConfigurationTypeDef",
    "CustomLogSourceConfigurationTypeDef",
    "CustomLogSourceResourceTypeDef",
    "ListDataLakeExceptionsResponseTypeDef",
    "DataLakeLifecycleConfigurationTypeDef",
    "DataLakeSourceTypeDef",
    "DataLakeUpdateStatusTypeDef",
    "NotificationConfigurationTypeDef",
    "CreateDataLakeOrganizationConfigurationRequestRequestTypeDef",
    "DeleteDataLakeOrganizationConfigurationRequestRequestTypeDef",
    "GetDataLakeOrganizationConfigurationResponseTypeDef",
    "CreateCustomLogSourceRequestRequestTypeDef",
    "CreateCustomLogSourceResponseTypeDef",
    "LogSourceResourceTypeDef",
    "DataLakeConfigurationTypeDef",
    "GetDataLakeSourcesResponseTypeDef",
    "DataLakeResourceTypeDef",
    "CreateSubscriberNotificationRequestRequestTypeDef",
    "UpdateSubscriberNotificationRequestRequestTypeDef",
    "CreateSubscriberRequestRequestTypeDef",
    "ListLogSourcesRequestListLogSourcesPaginateTypeDef",
    "ListLogSourcesRequestRequestTypeDef",
    "LogSourceTypeDef",
    "SubscriberResourceTypeDef",
    "UpdateSubscriberRequestRequestTypeDef",
    "CreateDataLakeRequestRequestTypeDef",
    "UpdateDataLakeRequestRequestTypeDef",
    "CreateDataLakeResponseTypeDef",
    "ListDataLakesResponseTypeDef",
    "UpdateDataLakeResponseTypeDef",
    "ListLogSourcesResponseTypeDef",
    "CreateSubscriberResponseTypeDef",
    "GetSubscriberResponseTypeDef",
    "ListSubscribersResponseTypeDef",
    "UpdateSubscriberResponseTypeDef",
)

AwsIdentityTypeDef = TypedDict(
    "AwsIdentityTypeDef",
    {
        "externalId": str,
        "principal": str,
    },
)

_RequiredAwsLogSourceConfigurationTypeDef = TypedDict(
    "_RequiredAwsLogSourceConfigurationTypeDef",
    {
        "regions": Sequence[str],
        "sourceName": AwsLogSourceNameType,
    },
)
_OptionalAwsLogSourceConfigurationTypeDef = TypedDict(
    "_OptionalAwsLogSourceConfigurationTypeDef",
    {
        "accounts": Sequence[str],
        "sourceVersion": str,
    },
    total=False,
)

class AwsLogSourceConfigurationTypeDef(
    _RequiredAwsLogSourceConfigurationTypeDef, _OptionalAwsLogSourceConfigurationTypeDef
):
    pass

AwsLogSourceResourceTypeDef = TypedDict(
    "AwsLogSourceResourceTypeDef",
    {
        "sourceName": AwsLogSourceNameType,
        "sourceVersion": str,
    },
    total=False,
)

CreateAwsLogSourceResponseTypeDef = TypedDict(
    "CreateAwsLogSourceResponseTypeDef",
    {
        "failed": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateDataLakeExceptionSubscriptionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDataLakeExceptionSubscriptionRequestRequestTypeDef",
    {
        "notificationEndpoint": str,
        "subscriptionProtocol": str,
    },
)
_OptionalCreateDataLakeExceptionSubscriptionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDataLakeExceptionSubscriptionRequestRequestTypeDef",
    {
        "exceptionTimeToLive": int,
    },
    total=False,
)

class CreateDataLakeExceptionSubscriptionRequestRequestTypeDef(
    _RequiredCreateDataLakeExceptionSubscriptionRequestRequestTypeDef,
    _OptionalCreateDataLakeExceptionSubscriptionRequestRequestTypeDef,
):
    pass

CreateSubscriberNotificationResponseTypeDef = TypedDict(
    "CreateSubscriberNotificationResponseTypeDef",
    {
        "subscriberEndpoint": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CustomLogSourceAttributesTypeDef = TypedDict(
    "CustomLogSourceAttributesTypeDef",
    {
        "crawlerArn": str,
        "databaseArn": str,
        "tableArn": str,
    },
    total=False,
)

CustomLogSourceCrawlerConfigurationTypeDef = TypedDict(
    "CustomLogSourceCrawlerConfigurationTypeDef",
    {
        "roleArn": str,
    },
)

CustomLogSourceProviderTypeDef = TypedDict(
    "CustomLogSourceProviderTypeDef",
    {
        "location": str,
        "roleArn": str,
    },
    total=False,
)

DataLakeEncryptionConfigurationTypeDef = TypedDict(
    "DataLakeEncryptionConfigurationTypeDef",
    {
        "kmsKeyId": str,
    },
    total=False,
)

DataLakeReplicationConfigurationTypeDef = TypedDict(
    "DataLakeReplicationConfigurationTypeDef",
    {
        "regions": Sequence[str],
        "roleArn": str,
    },
    total=False,
)

DataLakeExceptionTypeDef = TypedDict(
    "DataLakeExceptionTypeDef",
    {
        "exception": str,
        "region": str,
        "remediation": str,
        "timestamp": datetime,
    },
    total=False,
)

DataLakeLifecycleExpirationTypeDef = TypedDict(
    "DataLakeLifecycleExpirationTypeDef",
    {
        "days": int,
    },
    total=False,
)

DataLakeLifecycleTransitionTypeDef = TypedDict(
    "DataLakeLifecycleTransitionTypeDef",
    {
        "days": int,
        "storageClass": str,
    },
    total=False,
)

DataLakeSourceStatusTypeDef = TypedDict(
    "DataLakeSourceStatusTypeDef",
    {
        "resource": str,
        "status": SourceCollectionStatusType,
    },
    total=False,
)

DataLakeUpdateExceptionTypeDef = TypedDict(
    "DataLakeUpdateExceptionTypeDef",
    {
        "code": str,
        "reason": str,
    },
    total=False,
)

DeleteAwsLogSourceResponseTypeDef = TypedDict(
    "DeleteAwsLogSourceResponseTypeDef",
    {
        "failed": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeleteCustomLogSourceRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteCustomLogSourceRequestRequestTypeDef",
    {
        "sourceName": str,
    },
)
_OptionalDeleteCustomLogSourceRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteCustomLogSourceRequestRequestTypeDef",
    {
        "sourceVersion": str,
    },
    total=False,
)

class DeleteCustomLogSourceRequestRequestTypeDef(
    _RequiredDeleteCustomLogSourceRequestRequestTypeDef,
    _OptionalDeleteCustomLogSourceRequestRequestTypeDef,
):
    pass

DeleteDataLakeRequestRequestTypeDef = TypedDict(
    "DeleteDataLakeRequestRequestTypeDef",
    {
        "regions": Sequence[str],
    },
)

DeleteSubscriberNotificationRequestRequestTypeDef = TypedDict(
    "DeleteSubscriberNotificationRequestRequestTypeDef",
    {
        "subscriberId": str,
    },
)

DeleteSubscriberRequestRequestTypeDef = TypedDict(
    "DeleteSubscriberRequestRequestTypeDef",
    {
        "subscriberId": str,
    },
)

GetDataLakeExceptionSubscriptionResponseTypeDef = TypedDict(
    "GetDataLakeExceptionSubscriptionResponseTypeDef",
    {
        "exceptionTimeToLive": int,
        "notificationEndpoint": str,
        "subscriptionProtocol": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetDataLakeSourcesRequestGetDataLakeSourcesPaginateTypeDef = TypedDict(
    "GetDataLakeSourcesRequestGetDataLakeSourcesPaginateTypeDef",
    {
        "accounts": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

GetDataLakeSourcesRequestRequestTypeDef = TypedDict(
    "GetDataLakeSourcesRequestRequestTypeDef",
    {
        "accounts": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

GetSubscriberRequestRequestTypeDef = TypedDict(
    "GetSubscriberRequestRequestTypeDef",
    {
        "subscriberId": str,
    },
)

_RequiredHttpsNotificationConfigurationTypeDef = TypedDict(
    "_RequiredHttpsNotificationConfigurationTypeDef",
    {
        "endpoint": str,
        "targetRoleArn": str,
    },
)
_OptionalHttpsNotificationConfigurationTypeDef = TypedDict(
    "_OptionalHttpsNotificationConfigurationTypeDef",
    {
        "authorizationApiKeyName": str,
        "authorizationApiKeyValue": str,
        "httpMethod": HttpMethodType,
    },
    total=False,
)

class HttpsNotificationConfigurationTypeDef(
    _RequiredHttpsNotificationConfigurationTypeDef, _OptionalHttpsNotificationConfigurationTypeDef
):
    pass

ListDataLakeExceptionsRequestListDataLakeExceptionsPaginateTypeDef = TypedDict(
    "ListDataLakeExceptionsRequestListDataLakeExceptionsPaginateTypeDef",
    {
        "regions": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDataLakeExceptionsRequestRequestTypeDef = TypedDict(
    "ListDataLakeExceptionsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "regions": Sequence[str],
    },
    total=False,
)

ListDataLakesRequestRequestTypeDef = TypedDict(
    "ListDataLakesRequestRequestTypeDef",
    {
        "regions": Sequence[str],
    },
    total=False,
)

ListSubscribersRequestListSubscribersPaginateTypeDef = TypedDict(
    "ListSubscribersRequestListSubscribersPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListSubscribersRequestRequestTypeDef = TypedDict(
    "ListSubscribersRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
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

RegisterDataLakeDelegatedAdministratorRequestRequestTypeDef = TypedDict(
    "RegisterDataLakeDelegatedAdministratorRequestRequestTypeDef",
    {
        "accountId": str,
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

_RequiredUpdateDataLakeExceptionSubscriptionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDataLakeExceptionSubscriptionRequestRequestTypeDef",
    {
        "notificationEndpoint": str,
        "subscriptionProtocol": str,
    },
)
_OptionalUpdateDataLakeExceptionSubscriptionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDataLakeExceptionSubscriptionRequestRequestTypeDef",
    {
        "exceptionTimeToLive": int,
    },
    total=False,
)

class UpdateDataLakeExceptionSubscriptionRequestRequestTypeDef(
    _RequiredUpdateDataLakeExceptionSubscriptionRequestRequestTypeDef,
    _OptionalUpdateDataLakeExceptionSubscriptionRequestRequestTypeDef,
):
    pass

UpdateSubscriberNotificationResponseTypeDef = TypedDict(
    "UpdateSubscriberNotificationResponseTypeDef",
    {
        "subscriberEndpoint": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateAwsLogSourceRequestRequestTypeDef = TypedDict(
    "CreateAwsLogSourceRequestRequestTypeDef",
    {
        "sources": Sequence[AwsLogSourceConfigurationTypeDef],
    },
)

DeleteAwsLogSourceRequestRequestTypeDef = TypedDict(
    "DeleteAwsLogSourceRequestRequestTypeDef",
    {
        "sources": Sequence[AwsLogSourceConfigurationTypeDef],
    },
)

DataLakeAutoEnableNewAccountConfigurationTypeDef = TypedDict(
    "DataLakeAutoEnableNewAccountConfigurationTypeDef",
    {
        "region": str,
        "sources": Sequence[AwsLogSourceResourceTypeDef],
    },
)

CustomLogSourceConfigurationTypeDef = TypedDict(
    "CustomLogSourceConfigurationTypeDef",
    {
        "crawlerConfiguration": CustomLogSourceCrawlerConfigurationTypeDef,
        "providerIdentity": AwsIdentityTypeDef,
    },
)

CustomLogSourceResourceTypeDef = TypedDict(
    "CustomLogSourceResourceTypeDef",
    {
        "attributes": CustomLogSourceAttributesTypeDef,
        "provider": CustomLogSourceProviderTypeDef,
        "sourceName": str,
        "sourceVersion": str,
    },
    total=False,
)

ListDataLakeExceptionsResponseTypeDef = TypedDict(
    "ListDataLakeExceptionsResponseTypeDef",
    {
        "exceptions": List[DataLakeExceptionTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DataLakeLifecycleConfigurationTypeDef = TypedDict(
    "DataLakeLifecycleConfigurationTypeDef",
    {
        "expiration": DataLakeLifecycleExpirationTypeDef,
        "transitions": Sequence[DataLakeLifecycleTransitionTypeDef],
    },
    total=False,
)

DataLakeSourceTypeDef = TypedDict(
    "DataLakeSourceTypeDef",
    {
        "account": str,
        "eventClasses": List[str],
        "sourceName": str,
        "sourceStatuses": List[DataLakeSourceStatusTypeDef],
    },
    total=False,
)

DataLakeUpdateStatusTypeDef = TypedDict(
    "DataLakeUpdateStatusTypeDef",
    {
        "exception": DataLakeUpdateExceptionTypeDef,
        "requestId": str,
        "status": DataLakeStatusType,
    },
    total=False,
)

NotificationConfigurationTypeDef = TypedDict(
    "NotificationConfigurationTypeDef",
    {
        "httpsNotificationConfiguration": HttpsNotificationConfigurationTypeDef,
        "sqsNotificationConfiguration": Mapping[str, Any],
    },
    total=False,
)

CreateDataLakeOrganizationConfigurationRequestRequestTypeDef = TypedDict(
    "CreateDataLakeOrganizationConfigurationRequestRequestTypeDef",
    {
        "autoEnableNewAccount": Sequence[DataLakeAutoEnableNewAccountConfigurationTypeDef],
    },
)

DeleteDataLakeOrganizationConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteDataLakeOrganizationConfigurationRequestRequestTypeDef",
    {
        "autoEnableNewAccount": Sequence[DataLakeAutoEnableNewAccountConfigurationTypeDef],
    },
)

GetDataLakeOrganizationConfigurationResponseTypeDef = TypedDict(
    "GetDataLakeOrganizationConfigurationResponseTypeDef",
    {
        "autoEnableNewAccount": List[DataLakeAutoEnableNewAccountConfigurationTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateCustomLogSourceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCustomLogSourceRequestRequestTypeDef",
    {
        "sourceName": str,
    },
)
_OptionalCreateCustomLogSourceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCustomLogSourceRequestRequestTypeDef",
    {
        "configuration": CustomLogSourceConfigurationTypeDef,
        "eventClasses": Sequence[str],
        "sourceVersion": str,
    },
    total=False,
)

class CreateCustomLogSourceRequestRequestTypeDef(
    _RequiredCreateCustomLogSourceRequestRequestTypeDef,
    _OptionalCreateCustomLogSourceRequestRequestTypeDef,
):
    pass

CreateCustomLogSourceResponseTypeDef = TypedDict(
    "CreateCustomLogSourceResponseTypeDef",
    {
        "source": CustomLogSourceResourceTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LogSourceResourceTypeDef = TypedDict(
    "LogSourceResourceTypeDef",
    {
        "awsLogSource": AwsLogSourceResourceTypeDef,
        "customLogSource": CustomLogSourceResourceTypeDef,
    },
    total=False,
)

_RequiredDataLakeConfigurationTypeDef = TypedDict(
    "_RequiredDataLakeConfigurationTypeDef",
    {
        "region": str,
    },
)
_OptionalDataLakeConfigurationTypeDef = TypedDict(
    "_OptionalDataLakeConfigurationTypeDef",
    {
        "encryptionConfiguration": DataLakeEncryptionConfigurationTypeDef,
        "lifecycleConfiguration": DataLakeLifecycleConfigurationTypeDef,
        "replicationConfiguration": DataLakeReplicationConfigurationTypeDef,
    },
    total=False,
)

class DataLakeConfigurationTypeDef(
    _RequiredDataLakeConfigurationTypeDef, _OptionalDataLakeConfigurationTypeDef
):
    pass

GetDataLakeSourcesResponseTypeDef = TypedDict(
    "GetDataLakeSourcesResponseTypeDef",
    {
        "dataLakeArn": str,
        "dataLakeSources": List[DataLakeSourceTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDataLakeResourceTypeDef = TypedDict(
    "_RequiredDataLakeResourceTypeDef",
    {
        "dataLakeArn": str,
        "region": str,
    },
)
_OptionalDataLakeResourceTypeDef = TypedDict(
    "_OptionalDataLakeResourceTypeDef",
    {
        "createStatus": DataLakeStatusType,
        "encryptionConfiguration": DataLakeEncryptionConfigurationTypeDef,
        "lifecycleConfiguration": DataLakeLifecycleConfigurationTypeDef,
        "replicationConfiguration": DataLakeReplicationConfigurationTypeDef,
        "s3BucketArn": str,
        "updateStatus": DataLakeUpdateStatusTypeDef,
    },
    total=False,
)

class DataLakeResourceTypeDef(_RequiredDataLakeResourceTypeDef, _OptionalDataLakeResourceTypeDef):
    pass

CreateSubscriberNotificationRequestRequestTypeDef = TypedDict(
    "CreateSubscriberNotificationRequestRequestTypeDef",
    {
        "configuration": NotificationConfigurationTypeDef,
        "subscriberId": str,
    },
)

UpdateSubscriberNotificationRequestRequestTypeDef = TypedDict(
    "UpdateSubscriberNotificationRequestRequestTypeDef",
    {
        "configuration": NotificationConfigurationTypeDef,
        "subscriberId": str,
    },
)

_RequiredCreateSubscriberRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSubscriberRequestRequestTypeDef",
    {
        "sources": Sequence[LogSourceResourceTypeDef],
        "subscriberIdentity": AwsIdentityTypeDef,
        "subscriberName": str,
    },
)
_OptionalCreateSubscriberRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSubscriberRequestRequestTypeDef",
    {
        "accessTypes": Sequence[AccessTypeType],
        "subscriberDescription": str,
    },
    total=False,
)

class CreateSubscriberRequestRequestTypeDef(
    _RequiredCreateSubscriberRequestRequestTypeDef, _OptionalCreateSubscriberRequestRequestTypeDef
):
    pass

ListLogSourcesRequestListLogSourcesPaginateTypeDef = TypedDict(
    "ListLogSourcesRequestListLogSourcesPaginateTypeDef",
    {
        "accounts": Sequence[str],
        "regions": Sequence[str],
        "sources": Sequence[LogSourceResourceTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListLogSourcesRequestRequestTypeDef = TypedDict(
    "ListLogSourcesRequestRequestTypeDef",
    {
        "accounts": Sequence[str],
        "maxResults": int,
        "nextToken": str,
        "regions": Sequence[str],
        "sources": Sequence[LogSourceResourceTypeDef],
    },
    total=False,
)

LogSourceTypeDef = TypedDict(
    "LogSourceTypeDef",
    {
        "account": str,
        "region": str,
        "sources": List[LogSourceResourceTypeDef],
    },
    total=False,
)

_RequiredSubscriberResourceTypeDef = TypedDict(
    "_RequiredSubscriberResourceTypeDef",
    {
        "sources": List[LogSourceResourceTypeDef],
        "subscriberArn": str,
        "subscriberId": str,
        "subscriberIdentity": AwsIdentityTypeDef,
        "subscriberName": str,
    },
)
_OptionalSubscriberResourceTypeDef = TypedDict(
    "_OptionalSubscriberResourceTypeDef",
    {
        "accessTypes": List[AccessTypeType],
        "createdAt": datetime,
        "resourceShareArn": str,
        "resourceShareName": str,
        "roleArn": str,
        "s3BucketArn": str,
        "subscriberDescription": str,
        "subscriberEndpoint": str,
        "subscriberStatus": SubscriberStatusType,
        "updatedAt": datetime,
    },
    total=False,
)

class SubscriberResourceTypeDef(
    _RequiredSubscriberResourceTypeDef, _OptionalSubscriberResourceTypeDef
):
    pass

_RequiredUpdateSubscriberRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSubscriberRequestRequestTypeDef",
    {
        "subscriberId": str,
    },
)
_OptionalUpdateSubscriberRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSubscriberRequestRequestTypeDef",
    {
        "sources": Sequence[LogSourceResourceTypeDef],
        "subscriberDescription": str,
        "subscriberIdentity": AwsIdentityTypeDef,
        "subscriberName": str,
    },
    total=False,
)

class UpdateSubscriberRequestRequestTypeDef(
    _RequiredUpdateSubscriberRequestRequestTypeDef, _OptionalUpdateSubscriberRequestRequestTypeDef
):
    pass

CreateDataLakeRequestRequestTypeDef = TypedDict(
    "CreateDataLakeRequestRequestTypeDef",
    {
        "configurations": Sequence[DataLakeConfigurationTypeDef],
        "metaStoreManagerRoleArn": str,
    },
)

UpdateDataLakeRequestRequestTypeDef = TypedDict(
    "UpdateDataLakeRequestRequestTypeDef",
    {
        "configurations": Sequence[DataLakeConfigurationTypeDef],
    },
)

CreateDataLakeResponseTypeDef = TypedDict(
    "CreateDataLakeResponseTypeDef",
    {
        "dataLakes": List[DataLakeResourceTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDataLakesResponseTypeDef = TypedDict(
    "ListDataLakesResponseTypeDef",
    {
        "dataLakes": List[DataLakeResourceTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateDataLakeResponseTypeDef = TypedDict(
    "UpdateDataLakeResponseTypeDef",
    {
        "dataLakes": List[DataLakeResourceTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListLogSourcesResponseTypeDef = TypedDict(
    "ListLogSourcesResponseTypeDef",
    {
        "nextToken": str,
        "sources": List[LogSourceTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateSubscriberResponseTypeDef = TypedDict(
    "CreateSubscriberResponseTypeDef",
    {
        "subscriber": SubscriberResourceTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetSubscriberResponseTypeDef = TypedDict(
    "GetSubscriberResponseTypeDef",
    {
        "subscriber": SubscriberResourceTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSubscribersResponseTypeDef = TypedDict(
    "ListSubscribersResponseTypeDef",
    {
        "nextToken": str,
        "subscribers": List[SubscriberResourceTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateSubscriberResponseTypeDef = TypedDict(
    "UpdateSubscriberResponseTypeDef",
    {
        "subscriber": SubscriberResourceTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
