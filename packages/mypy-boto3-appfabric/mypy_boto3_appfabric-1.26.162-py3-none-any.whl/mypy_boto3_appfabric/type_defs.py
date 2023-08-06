"""
Type annotations for appfabric service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/type_defs/)

Usage::

    ```python
    from mypy_boto3_appfabric.type_defs import ApiKeyCredentialTypeDef

    data: ApiKeyCredentialTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    AppAuthorizationStatusType,
    AuthTypeType,
    FormatType,
    IngestionDestinationStatusType,
    IngestionStateType,
    PersonaType,
    ResultStatusType,
    SchemaType,
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
    "ApiKeyCredentialTypeDef",
    "TenantTypeDef",
    "AppBundleSummaryTypeDef",
    "AppBundleTypeDef",
    "AuditLogProcessingConfigurationTypeDef",
    "AuthRequestTypeDef",
    "BatchGetUserAccessTasksRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "TagTypeDef",
    "IngestionTypeDef",
    "Oauth2CredentialTypeDef",
    "DeleteAppAuthorizationRequestRequestTypeDef",
    "DeleteAppBundleRequestRequestTypeDef",
    "DeleteIngestionDestinationRequestRequestTypeDef",
    "DeleteIngestionRequestRequestTypeDef",
    "FirehoseStreamTypeDef",
    "S3BucketTypeDef",
    "GetAppAuthorizationRequestRequestTypeDef",
    "GetAppBundleRequestRequestTypeDef",
    "GetIngestionDestinationRequestRequestTypeDef",
    "GetIngestionRequestRequestTypeDef",
    "IngestionDestinationSummaryTypeDef",
    "IngestionSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "ListAppAuthorizationsRequestRequestTypeDef",
    "ListAppBundlesRequestRequestTypeDef",
    "ListIngestionDestinationsRequestRequestTypeDef",
    "ListIngestionsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "StartIngestionRequestRequestTypeDef",
    "StartUserAccessTasksRequestRequestTypeDef",
    "StopIngestionRequestRequestTypeDef",
    "TaskErrorTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "AppAuthorizationSummaryTypeDef",
    "AppAuthorizationTypeDef",
    "ProcessingConfigurationTypeDef",
    "ConnectAppAuthorizationRequestRequestTypeDef",
    "CreateAppBundleResponseTypeDef",
    "GetAppBundleResponseTypeDef",
    "ListAppBundlesResponseTypeDef",
    "CreateAppBundleRequestRequestTypeDef",
    "CreateIngestionRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateIngestionResponseTypeDef",
    "GetIngestionResponseTypeDef",
    "CredentialTypeDef",
    "DestinationTypeDef",
    "ListIngestionDestinationsResponseTypeDef",
    "ListIngestionsResponseTypeDef",
    "ListAppAuthorizationsRequestListAppAuthorizationsPaginateTypeDef",
    "ListAppBundlesRequestListAppBundlesPaginateTypeDef",
    "ListIngestionDestinationsRequestListIngestionDestinationsPaginateTypeDef",
    "ListIngestionsRequestListIngestionsPaginateTypeDef",
    "UserAccessResultItemTypeDef",
    "UserAccessTaskItemTypeDef",
    "ConnectAppAuthorizationResponseTypeDef",
    "ListAppAuthorizationsResponseTypeDef",
    "CreateAppAuthorizationResponseTypeDef",
    "GetAppAuthorizationResponseTypeDef",
    "UpdateAppAuthorizationResponseTypeDef",
    "CreateAppAuthorizationRequestRequestTypeDef",
    "UpdateAppAuthorizationRequestRequestTypeDef",
    "AuditLogDestinationConfigurationTypeDef",
    "BatchGetUserAccessTasksResponseTypeDef",
    "StartUserAccessTasksResponseTypeDef",
    "DestinationConfigurationTypeDef",
    "CreateIngestionDestinationRequestRequestTypeDef",
    "IngestionDestinationTypeDef",
    "UpdateIngestionDestinationRequestRequestTypeDef",
    "CreateIngestionDestinationResponseTypeDef",
    "GetIngestionDestinationResponseTypeDef",
    "UpdateIngestionDestinationResponseTypeDef",
)

ApiKeyCredentialTypeDef = TypedDict(
    "ApiKeyCredentialTypeDef",
    {
        "apiKey": str,
    },
)

TenantTypeDef = TypedDict(
    "TenantTypeDef",
    {
        "tenantIdentifier": str,
        "tenantDisplayName": str,
    },
)

AppBundleSummaryTypeDef = TypedDict(
    "AppBundleSummaryTypeDef",
    {
        "arn": str,
    },
)

_RequiredAppBundleTypeDef = TypedDict(
    "_RequiredAppBundleTypeDef",
    {
        "arn": str,
    },
)
_OptionalAppBundleTypeDef = TypedDict(
    "_OptionalAppBundleTypeDef",
    {
        "customerManagedKeyArn": str,
    },
    total=False,
)


class AppBundleTypeDef(_RequiredAppBundleTypeDef, _OptionalAppBundleTypeDef):
    pass


AuditLogProcessingConfigurationTypeDef = TypedDict(
    "AuditLogProcessingConfigurationTypeDef",
    {
        "schema": SchemaType,
        "format": FormatType,
    },
)

AuthRequestTypeDef = TypedDict(
    "AuthRequestTypeDef",
    {
        "redirectUri": str,
        "code": str,
    },
)

BatchGetUserAccessTasksRequestRequestTypeDef = TypedDict(
    "BatchGetUserAccessTasksRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
        "taskIdList": Sequence[str],
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

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
)

IngestionTypeDef = TypedDict(
    "IngestionTypeDef",
    {
        "arn": str,
        "appBundleArn": str,
        "app": str,
        "tenantId": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "state": IngestionStateType,
        "ingestionType": Literal["auditLog"],
    },
)

Oauth2CredentialTypeDef = TypedDict(
    "Oauth2CredentialTypeDef",
    {
        "clientId": str,
        "clientSecret": str,
    },
)

DeleteAppAuthorizationRequestRequestTypeDef = TypedDict(
    "DeleteAppAuthorizationRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
        "appAuthorizationIdentifier": str,
    },
)

DeleteAppBundleRequestRequestTypeDef = TypedDict(
    "DeleteAppBundleRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
    },
)

DeleteIngestionDestinationRequestRequestTypeDef = TypedDict(
    "DeleteIngestionDestinationRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
        "ingestionIdentifier": str,
        "ingestionDestinationIdentifier": str,
    },
)

DeleteIngestionRequestRequestTypeDef = TypedDict(
    "DeleteIngestionRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
        "ingestionIdentifier": str,
    },
)

FirehoseStreamTypeDef = TypedDict(
    "FirehoseStreamTypeDef",
    {
        "streamName": str,
    },
)

_RequiredS3BucketTypeDef = TypedDict(
    "_RequiredS3BucketTypeDef",
    {
        "bucketName": str,
    },
)
_OptionalS3BucketTypeDef = TypedDict(
    "_OptionalS3BucketTypeDef",
    {
        "prefix": str,
    },
    total=False,
)


class S3BucketTypeDef(_RequiredS3BucketTypeDef, _OptionalS3BucketTypeDef):
    pass


GetAppAuthorizationRequestRequestTypeDef = TypedDict(
    "GetAppAuthorizationRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
        "appAuthorizationIdentifier": str,
    },
)

GetAppBundleRequestRequestTypeDef = TypedDict(
    "GetAppBundleRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
    },
)

GetIngestionDestinationRequestRequestTypeDef = TypedDict(
    "GetIngestionDestinationRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
        "ingestionIdentifier": str,
        "ingestionDestinationIdentifier": str,
    },
)

GetIngestionRequestRequestTypeDef = TypedDict(
    "GetIngestionRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
        "ingestionIdentifier": str,
    },
)

IngestionDestinationSummaryTypeDef = TypedDict(
    "IngestionDestinationSummaryTypeDef",
    {
        "arn": str,
    },
)

IngestionSummaryTypeDef = TypedDict(
    "IngestionSummaryTypeDef",
    {
        "arn": str,
        "app": str,
        "tenantId": str,
        "state": IngestionStateType,
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

_RequiredListAppAuthorizationsRequestRequestTypeDef = TypedDict(
    "_RequiredListAppAuthorizationsRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
    },
)
_OptionalListAppAuthorizationsRequestRequestTypeDef = TypedDict(
    "_OptionalListAppAuthorizationsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListAppAuthorizationsRequestRequestTypeDef(
    _RequiredListAppAuthorizationsRequestRequestTypeDef,
    _OptionalListAppAuthorizationsRequestRequestTypeDef,
):
    pass


ListAppBundlesRequestRequestTypeDef = TypedDict(
    "ListAppBundlesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredListIngestionDestinationsRequestRequestTypeDef = TypedDict(
    "_RequiredListIngestionDestinationsRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
        "ingestionIdentifier": str,
    },
)
_OptionalListIngestionDestinationsRequestRequestTypeDef = TypedDict(
    "_OptionalListIngestionDestinationsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListIngestionDestinationsRequestRequestTypeDef(
    _RequiredListIngestionDestinationsRequestRequestTypeDef,
    _OptionalListIngestionDestinationsRequestRequestTypeDef,
):
    pass


_RequiredListIngestionsRequestRequestTypeDef = TypedDict(
    "_RequiredListIngestionsRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
    },
)
_OptionalListIngestionsRequestRequestTypeDef = TypedDict(
    "_OptionalListIngestionsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListIngestionsRequestRequestTypeDef(
    _RequiredListIngestionsRequestRequestTypeDef, _OptionalListIngestionsRequestRequestTypeDef
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

StartIngestionRequestRequestTypeDef = TypedDict(
    "StartIngestionRequestRequestTypeDef",
    {
        "ingestionIdentifier": str,
        "appBundleIdentifier": str,
    },
)

StartUserAccessTasksRequestRequestTypeDef = TypedDict(
    "StartUserAccessTasksRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
        "email": str,
    },
)

StopIngestionRequestRequestTypeDef = TypedDict(
    "StopIngestionRequestRequestTypeDef",
    {
        "ingestionIdentifier": str,
        "appBundleIdentifier": str,
    },
)

TaskErrorTypeDef = TypedDict(
    "TaskErrorTypeDef",
    {
        "errorCode": str,
        "errorMessage": str,
    },
    total=False,
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

AppAuthorizationSummaryTypeDef = TypedDict(
    "AppAuthorizationSummaryTypeDef",
    {
        "appAuthorizationArn": str,
        "appBundleArn": str,
        "app": str,
        "tenant": TenantTypeDef,
        "status": AppAuthorizationStatusType,
        "updatedAt": datetime,
    },
)

_RequiredAppAuthorizationTypeDef = TypedDict(
    "_RequiredAppAuthorizationTypeDef",
    {
        "appAuthorizationArn": str,
        "appBundleArn": str,
        "app": str,
        "tenant": TenantTypeDef,
        "authType": AuthTypeType,
        "status": AppAuthorizationStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
    },
)
_OptionalAppAuthorizationTypeDef = TypedDict(
    "_OptionalAppAuthorizationTypeDef",
    {
        "persona": PersonaType,
        "authUrl": str,
    },
    total=False,
)


class AppAuthorizationTypeDef(_RequiredAppAuthorizationTypeDef, _OptionalAppAuthorizationTypeDef):
    pass


ProcessingConfigurationTypeDef = TypedDict(
    "ProcessingConfigurationTypeDef",
    {
        "auditLog": AuditLogProcessingConfigurationTypeDef,
    },
    total=False,
)

_RequiredConnectAppAuthorizationRequestRequestTypeDef = TypedDict(
    "_RequiredConnectAppAuthorizationRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
        "appAuthorizationIdentifier": str,
    },
)
_OptionalConnectAppAuthorizationRequestRequestTypeDef = TypedDict(
    "_OptionalConnectAppAuthorizationRequestRequestTypeDef",
    {
        "authRequest": AuthRequestTypeDef,
    },
    total=False,
)


class ConnectAppAuthorizationRequestRequestTypeDef(
    _RequiredConnectAppAuthorizationRequestRequestTypeDef,
    _OptionalConnectAppAuthorizationRequestRequestTypeDef,
):
    pass


CreateAppBundleResponseTypeDef = TypedDict(
    "CreateAppBundleResponseTypeDef",
    {
        "appBundle": AppBundleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAppBundleResponseTypeDef = TypedDict(
    "GetAppBundleResponseTypeDef",
    {
        "appBundle": AppBundleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppBundlesResponseTypeDef = TypedDict(
    "ListAppBundlesResponseTypeDef",
    {
        "appBundleSummaryList": List[AppBundleSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAppBundleRequestRequestTypeDef = TypedDict(
    "CreateAppBundleRequestRequestTypeDef",
    {
        "clientToken": str,
        "customerManagedKeyIdentifier": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)

_RequiredCreateIngestionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateIngestionRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
        "app": str,
        "tenantId": str,
        "ingestionType": Literal["auditLog"],
    },
)
_OptionalCreateIngestionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateIngestionRequestRequestTypeDef",
    {
        "clientToken": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateIngestionRequestRequestTypeDef(
    _RequiredCreateIngestionRequestRequestTypeDef, _OptionalCreateIngestionRequestRequestTypeDef
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)

CreateIngestionResponseTypeDef = TypedDict(
    "CreateIngestionResponseTypeDef",
    {
        "ingestion": IngestionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetIngestionResponseTypeDef = TypedDict(
    "GetIngestionResponseTypeDef",
    {
        "ingestion": IngestionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CredentialTypeDef = TypedDict(
    "CredentialTypeDef",
    {
        "oauth2Credential": Oauth2CredentialTypeDef,
        "apiKeyCredential": ApiKeyCredentialTypeDef,
    },
    total=False,
)

DestinationTypeDef = TypedDict(
    "DestinationTypeDef",
    {
        "s3Bucket": S3BucketTypeDef,
        "firehoseStream": FirehoseStreamTypeDef,
    },
    total=False,
)

ListIngestionDestinationsResponseTypeDef = TypedDict(
    "ListIngestionDestinationsResponseTypeDef",
    {
        "ingestionDestinations": List[IngestionDestinationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListIngestionsResponseTypeDef = TypedDict(
    "ListIngestionsResponseTypeDef",
    {
        "ingestions": List[IngestionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListAppAuthorizationsRequestListAppAuthorizationsPaginateTypeDef = TypedDict(
    "_RequiredListAppAuthorizationsRequestListAppAuthorizationsPaginateTypeDef",
    {
        "appBundleIdentifier": str,
    },
)
_OptionalListAppAuthorizationsRequestListAppAuthorizationsPaginateTypeDef = TypedDict(
    "_OptionalListAppAuthorizationsRequestListAppAuthorizationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAppAuthorizationsRequestListAppAuthorizationsPaginateTypeDef(
    _RequiredListAppAuthorizationsRequestListAppAuthorizationsPaginateTypeDef,
    _OptionalListAppAuthorizationsRequestListAppAuthorizationsPaginateTypeDef,
):
    pass


ListAppBundlesRequestListAppBundlesPaginateTypeDef = TypedDict(
    "ListAppBundlesRequestListAppBundlesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListIngestionDestinationsRequestListIngestionDestinationsPaginateTypeDef = TypedDict(
    "_RequiredListIngestionDestinationsRequestListIngestionDestinationsPaginateTypeDef",
    {
        "appBundleIdentifier": str,
        "ingestionIdentifier": str,
    },
)
_OptionalListIngestionDestinationsRequestListIngestionDestinationsPaginateTypeDef = TypedDict(
    "_OptionalListIngestionDestinationsRequestListIngestionDestinationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListIngestionDestinationsRequestListIngestionDestinationsPaginateTypeDef(
    _RequiredListIngestionDestinationsRequestListIngestionDestinationsPaginateTypeDef,
    _OptionalListIngestionDestinationsRequestListIngestionDestinationsPaginateTypeDef,
):
    pass


_RequiredListIngestionsRequestListIngestionsPaginateTypeDef = TypedDict(
    "_RequiredListIngestionsRequestListIngestionsPaginateTypeDef",
    {
        "appBundleIdentifier": str,
    },
)
_OptionalListIngestionsRequestListIngestionsPaginateTypeDef = TypedDict(
    "_OptionalListIngestionsRequestListIngestionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListIngestionsRequestListIngestionsPaginateTypeDef(
    _RequiredListIngestionsRequestListIngestionsPaginateTypeDef,
    _OptionalListIngestionsRequestListIngestionsPaginateTypeDef,
):
    pass


UserAccessResultItemTypeDef = TypedDict(
    "UserAccessResultItemTypeDef",
    {
        "app": str,
        "tenantId": str,
        "tenantDisplayName": str,
        "taskId": str,
        "resultStatus": ResultStatusType,
        "email": str,
        "userId": str,
        "userFullName": str,
        "userFirstName": str,
        "userLastName": str,
        "userStatus": str,
        "taskError": TaskErrorTypeDef,
    },
    total=False,
)

_RequiredUserAccessTaskItemTypeDef = TypedDict(
    "_RequiredUserAccessTaskItemTypeDef",
    {
        "app": str,
        "tenantId": str,
    },
)
_OptionalUserAccessTaskItemTypeDef = TypedDict(
    "_OptionalUserAccessTaskItemTypeDef",
    {
        "taskId": str,
        "error": TaskErrorTypeDef,
    },
    total=False,
)


class UserAccessTaskItemTypeDef(
    _RequiredUserAccessTaskItemTypeDef, _OptionalUserAccessTaskItemTypeDef
):
    pass


ConnectAppAuthorizationResponseTypeDef = TypedDict(
    "ConnectAppAuthorizationResponseTypeDef",
    {
        "appAuthorizationSummary": AppAuthorizationSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppAuthorizationsResponseTypeDef = TypedDict(
    "ListAppAuthorizationsResponseTypeDef",
    {
        "appAuthorizationSummaryList": List[AppAuthorizationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAppAuthorizationResponseTypeDef = TypedDict(
    "CreateAppAuthorizationResponseTypeDef",
    {
        "appAuthorization": AppAuthorizationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAppAuthorizationResponseTypeDef = TypedDict(
    "GetAppAuthorizationResponseTypeDef",
    {
        "appAuthorization": AppAuthorizationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAppAuthorizationResponseTypeDef = TypedDict(
    "UpdateAppAuthorizationResponseTypeDef",
    {
        "appAuthorization": AppAuthorizationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateAppAuthorizationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAppAuthorizationRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
        "app": str,
        "credential": CredentialTypeDef,
        "tenant": TenantTypeDef,
        "authType": AuthTypeType,
    },
)
_OptionalCreateAppAuthorizationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAppAuthorizationRequestRequestTypeDef",
    {
        "clientToken": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateAppAuthorizationRequestRequestTypeDef(
    _RequiredCreateAppAuthorizationRequestRequestTypeDef,
    _OptionalCreateAppAuthorizationRequestRequestTypeDef,
):
    pass


_RequiredUpdateAppAuthorizationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAppAuthorizationRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
        "appAuthorizationIdentifier": str,
    },
)
_OptionalUpdateAppAuthorizationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAppAuthorizationRequestRequestTypeDef",
    {
        "credential": CredentialTypeDef,
        "tenant": TenantTypeDef,
    },
    total=False,
)


class UpdateAppAuthorizationRequestRequestTypeDef(
    _RequiredUpdateAppAuthorizationRequestRequestTypeDef,
    _OptionalUpdateAppAuthorizationRequestRequestTypeDef,
):
    pass


AuditLogDestinationConfigurationTypeDef = TypedDict(
    "AuditLogDestinationConfigurationTypeDef",
    {
        "destination": DestinationTypeDef,
    },
)

BatchGetUserAccessTasksResponseTypeDef = TypedDict(
    "BatchGetUserAccessTasksResponseTypeDef",
    {
        "userAccessResultsList": List[UserAccessResultItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartUserAccessTasksResponseTypeDef = TypedDict(
    "StartUserAccessTasksResponseTypeDef",
    {
        "userAccessTasksList": List[UserAccessTaskItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DestinationConfigurationTypeDef = TypedDict(
    "DestinationConfigurationTypeDef",
    {
        "auditLog": AuditLogDestinationConfigurationTypeDef,
    },
    total=False,
)

_RequiredCreateIngestionDestinationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateIngestionDestinationRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
        "ingestionIdentifier": str,
        "processingConfiguration": ProcessingConfigurationTypeDef,
        "destinationConfiguration": DestinationConfigurationTypeDef,
    },
)
_OptionalCreateIngestionDestinationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateIngestionDestinationRequestRequestTypeDef",
    {
        "clientToken": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateIngestionDestinationRequestRequestTypeDef(
    _RequiredCreateIngestionDestinationRequestRequestTypeDef,
    _OptionalCreateIngestionDestinationRequestRequestTypeDef,
):
    pass


_RequiredIngestionDestinationTypeDef = TypedDict(
    "_RequiredIngestionDestinationTypeDef",
    {
        "arn": str,
        "ingestionArn": str,
        "processingConfiguration": ProcessingConfigurationTypeDef,
        "destinationConfiguration": DestinationConfigurationTypeDef,
    },
)
_OptionalIngestionDestinationTypeDef = TypedDict(
    "_OptionalIngestionDestinationTypeDef",
    {
        "status": IngestionDestinationStatusType,
        "statusReason": str,
        "createdAt": datetime,
        "updatedAt": datetime,
    },
    total=False,
)


class IngestionDestinationTypeDef(
    _RequiredIngestionDestinationTypeDef, _OptionalIngestionDestinationTypeDef
):
    pass


UpdateIngestionDestinationRequestRequestTypeDef = TypedDict(
    "UpdateIngestionDestinationRequestRequestTypeDef",
    {
        "appBundleIdentifier": str,
        "ingestionIdentifier": str,
        "ingestionDestinationIdentifier": str,
        "destinationConfiguration": DestinationConfigurationTypeDef,
    },
)

CreateIngestionDestinationResponseTypeDef = TypedDict(
    "CreateIngestionDestinationResponseTypeDef",
    {
        "ingestionDestination": IngestionDestinationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetIngestionDestinationResponseTypeDef = TypedDict(
    "GetIngestionDestinationResponseTypeDef",
    {
        "ingestionDestination": IngestionDestinationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateIngestionDestinationResponseTypeDef = TypedDict(
    "UpdateIngestionDestinationResponseTypeDef",
    {
        "ingestionDestination": IngestionDestinationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
