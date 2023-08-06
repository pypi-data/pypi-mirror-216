"""
Type annotations for appstream service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/type_defs/)

Usage::

    ```python
    from mypy_boto3_appstream.type_defs import AccessEndpointTypeDef

    data: AccessEndpointTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ActionType,
    AppBlockBuilderAttributeType,
    AppBlockBuilderStateType,
    AppBlockStateType,
    ApplicationAttributeType,
    AppVisibilityType,
    AuthenticationTypeType,
    CertificateBasedAuthStatusType,
    FleetAttributeType,
    FleetErrorCodeType,
    FleetStateType,
    FleetTypeType,
    ImageBuilderStateChangeReasonCodeType,
    ImageBuilderStateType,
    ImageStateChangeReasonCodeType,
    ImageStateType,
    MessageActionType,
    PackagingTypeType,
    PermissionType,
    PlatformTypeType,
    PreferredProtocolType,
    SessionConnectionStateType,
    SessionStateType,
    StackAttributeType,
    StackErrorCodeType,
    StorageConnectorTypeType,
    StreamViewType,
    UsageReportExecutionErrorCodeType,
    UserStackAssociationErrorCodeType,
    VisibilityTypeType,
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
    "AccessEndpointTypeDef",
    "AppBlockBuilderAppBlockAssociationTypeDef",
    "AppBlockBuilderStateChangeReasonTypeDef",
    "ResourceErrorTypeDef",
    "VpcConfigTypeDef",
    "ErrorDetailsTypeDef",
    "S3LocationTypeDef",
    "ApplicationFleetAssociationTypeDef",
    "ApplicationSettingsResponseTypeDef",
    "ApplicationSettingsTypeDef",
    "AssociateAppBlockBuilderAppBlockRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AssociateApplicationFleetRequestRequestTypeDef",
    "AssociateApplicationToEntitlementRequestRequestTypeDef",
    "AssociateFleetRequestRequestTypeDef",
    "UserStackAssociationTypeDef",
    "CertificateBasedAuthPropertiesTypeDef",
    "ComputeCapacityStatusTypeDef",
    "ComputeCapacityTypeDef",
    "CopyImageRequestRequestTypeDef",
    "CreateAppBlockBuilderStreamingURLRequestRequestTypeDef",
    "ServiceAccountCredentialsTypeDef",
    "EntitlementAttributeTypeDef",
    "DomainJoinInfoTypeDef",
    "CreateImageBuilderStreamingURLRequestRequestTypeDef",
    "StorageConnectorTypeDef",
    "StreamingExperienceSettingsTypeDef",
    "UserSettingTypeDef",
    "CreateStreamingURLRequestRequestTypeDef",
    "CreateUpdatedImageRequestRequestTypeDef",
    "CreateUserRequestRequestTypeDef",
    "DeleteAppBlockBuilderRequestRequestTypeDef",
    "DeleteAppBlockRequestRequestTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteDirectoryConfigRequestRequestTypeDef",
    "DeleteEntitlementRequestRequestTypeDef",
    "DeleteFleetRequestRequestTypeDef",
    "DeleteImageBuilderRequestRequestTypeDef",
    "DeleteImagePermissionsRequestRequestTypeDef",
    "DeleteImageRequestRequestTypeDef",
    "DeleteStackRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DescribeAppBlockBuilderAppBlockAssociationsRequestRequestTypeDef",
    "DescribeAppBlockBuildersRequestRequestTypeDef",
    "DescribeAppBlocksRequestRequestTypeDef",
    "DescribeApplicationFleetAssociationsRequestRequestTypeDef",
    "DescribeApplicationsRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeDirectoryConfigsRequestRequestTypeDef",
    "DescribeEntitlementsRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeFleetsRequestRequestTypeDef",
    "DescribeImageBuildersRequestRequestTypeDef",
    "DescribeImagePermissionsRequestRequestTypeDef",
    "DescribeImagesRequestRequestTypeDef",
    "DescribeSessionsRequestRequestTypeDef",
    "DescribeStacksRequestRequestTypeDef",
    "DescribeUsageReportSubscriptionsRequestRequestTypeDef",
    "DescribeUserStackAssociationsRequestRequestTypeDef",
    "DescribeUsersRequestRequestTypeDef",
    "UserTypeDef",
    "DisableUserRequestRequestTypeDef",
    "DisassociateAppBlockBuilderAppBlockRequestRequestTypeDef",
    "DisassociateApplicationFleetRequestRequestTypeDef",
    "DisassociateApplicationFromEntitlementRequestRequestTypeDef",
    "DisassociateFleetRequestRequestTypeDef",
    "EnableUserRequestRequestTypeDef",
    "EntitledApplicationTypeDef",
    "ExpireSessionRequestRequestTypeDef",
    "FleetErrorTypeDef",
    "ImageBuilderStateChangeReasonTypeDef",
    "NetworkAccessConfigurationTypeDef",
    "ImagePermissionsTypeDef",
    "ImageStateChangeReasonTypeDef",
    "LastReportGenerationExecutionErrorTypeDef",
    "ListAssociatedFleetsRequestRequestTypeDef",
    "ListAssociatedStacksRequestRequestTypeDef",
    "ListEntitledApplicationsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "StackErrorTypeDef",
    "StartAppBlockBuilderRequestRequestTypeDef",
    "StartFleetRequestRequestTypeDef",
    "StartImageBuilderRequestRequestTypeDef",
    "StopAppBlockBuilderRequestRequestTypeDef",
    "StopFleetRequestRequestTypeDef",
    "StopImageBuilderRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "AppBlockBuilderTypeDef",
    "CreateAppBlockBuilderRequestRequestTypeDef",
    "UpdateAppBlockBuilderRequestRequestTypeDef",
    "ApplicationTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "ScriptDetailsTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "AssociateAppBlockBuilderAppBlockResultTypeDef",
    "AssociateApplicationFleetResultTypeDef",
    "CopyImageResponseTypeDef",
    "CreateAppBlockBuilderStreamingURLResultTypeDef",
    "CreateImageBuilderStreamingURLResultTypeDef",
    "CreateStreamingURLResultTypeDef",
    "CreateUsageReportSubscriptionResultTypeDef",
    "DescribeAppBlockBuilderAppBlockAssociationsResultTypeDef",
    "DescribeApplicationFleetAssociationsResultTypeDef",
    "ListAssociatedFleetsResultTypeDef",
    "ListAssociatedStacksResultTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "BatchAssociateUserStackRequestRequestTypeDef",
    "BatchDisassociateUserStackRequestRequestTypeDef",
    "DescribeUserStackAssociationsResultTypeDef",
    "UserStackAssociationErrorTypeDef",
    "CreateDirectoryConfigRequestRequestTypeDef",
    "DirectoryConfigTypeDef",
    "UpdateDirectoryConfigRequestRequestTypeDef",
    "CreateEntitlementRequestRequestTypeDef",
    "EntitlementTypeDef",
    "UpdateEntitlementRequestRequestTypeDef",
    "CreateFleetRequestRequestTypeDef",
    "CreateImageBuilderRequestRequestTypeDef",
    "UpdateFleetRequestRequestTypeDef",
    "CreateStackRequestRequestTypeDef",
    "UpdateStackRequestRequestTypeDef",
    "DescribeDirectoryConfigsRequestDescribeDirectoryConfigsPaginateTypeDef",
    "DescribeFleetsRequestDescribeFleetsPaginateTypeDef",
    "DescribeImageBuildersRequestDescribeImageBuildersPaginateTypeDef",
    "DescribeImagesRequestDescribeImagesPaginateTypeDef",
    "DescribeSessionsRequestDescribeSessionsPaginateTypeDef",
    "DescribeStacksRequestDescribeStacksPaginateTypeDef",
    "DescribeUserStackAssociationsRequestDescribeUserStackAssociationsPaginateTypeDef",
    "DescribeUsersRequestDescribeUsersPaginateTypeDef",
    "ListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef",
    "ListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef",
    "DescribeFleetsRequestFleetStartedWaitTypeDef",
    "DescribeFleetsRequestFleetStoppedWaitTypeDef",
    "DescribeUsersResultTypeDef",
    "ListEntitledApplicationsResultTypeDef",
    "FleetTypeDef",
    "ImageBuilderTypeDef",
    "SessionTypeDef",
    "SharedImagePermissionsTypeDef",
    "UpdateImagePermissionsRequestRequestTypeDef",
    "UsageReportSubscriptionTypeDef",
    "StackTypeDef",
    "CreateAppBlockBuilderResultTypeDef",
    "DescribeAppBlockBuildersResultTypeDef",
    "StartAppBlockBuilderResultTypeDef",
    "StopAppBlockBuilderResultTypeDef",
    "UpdateAppBlockBuilderResultTypeDef",
    "CreateApplicationResultTypeDef",
    "DescribeApplicationsResultTypeDef",
    "ImageTypeDef",
    "UpdateApplicationResultTypeDef",
    "AppBlockTypeDef",
    "CreateAppBlockRequestRequestTypeDef",
    "BatchAssociateUserStackResultTypeDef",
    "BatchDisassociateUserStackResultTypeDef",
    "CreateDirectoryConfigResultTypeDef",
    "DescribeDirectoryConfigsResultTypeDef",
    "UpdateDirectoryConfigResultTypeDef",
    "CreateEntitlementResultTypeDef",
    "DescribeEntitlementsResultTypeDef",
    "UpdateEntitlementResultTypeDef",
    "CreateFleetResultTypeDef",
    "DescribeFleetsResultTypeDef",
    "UpdateFleetResultTypeDef",
    "CreateImageBuilderResultTypeDef",
    "DeleteImageBuilderResultTypeDef",
    "DescribeImageBuildersResultTypeDef",
    "StartImageBuilderResultTypeDef",
    "StopImageBuilderResultTypeDef",
    "DescribeSessionsResultTypeDef",
    "DescribeImagePermissionsResultTypeDef",
    "DescribeUsageReportSubscriptionsResultTypeDef",
    "CreateStackResultTypeDef",
    "DescribeStacksResultTypeDef",
    "UpdateStackResultTypeDef",
    "CreateUpdatedImageResultTypeDef",
    "DeleteImageResultTypeDef",
    "DescribeImagesResultTypeDef",
    "CreateAppBlockResultTypeDef",
    "DescribeAppBlocksResultTypeDef",
)

_RequiredAccessEndpointTypeDef = TypedDict(
    "_RequiredAccessEndpointTypeDef",
    {
        "EndpointType": Literal["STREAMING"],
    },
)
_OptionalAccessEndpointTypeDef = TypedDict(
    "_OptionalAccessEndpointTypeDef",
    {
        "VpceId": str,
    },
    total=False,
)


class AccessEndpointTypeDef(_RequiredAccessEndpointTypeDef, _OptionalAccessEndpointTypeDef):
    pass


AppBlockBuilderAppBlockAssociationTypeDef = TypedDict(
    "AppBlockBuilderAppBlockAssociationTypeDef",
    {
        "AppBlockArn": str,
        "AppBlockBuilderName": str,
    },
)

AppBlockBuilderStateChangeReasonTypeDef = TypedDict(
    "AppBlockBuilderStateChangeReasonTypeDef",
    {
        "Code": Literal["INTERNAL_ERROR"],
        "Message": str,
    },
    total=False,
)

ResourceErrorTypeDef = TypedDict(
    "ResourceErrorTypeDef",
    {
        "ErrorCode": FleetErrorCodeType,
        "ErrorMessage": str,
        "ErrorTimestamp": datetime,
    },
    total=False,
)

VpcConfigTypeDef = TypedDict(
    "VpcConfigTypeDef",
    {
        "SubnetIds": Sequence[str],
        "SecurityGroupIds": Sequence[str],
    },
    total=False,
)

ErrorDetailsTypeDef = TypedDict(
    "ErrorDetailsTypeDef",
    {
        "ErrorCode": str,
        "ErrorMessage": str,
    },
    total=False,
)

_RequiredS3LocationTypeDef = TypedDict(
    "_RequiredS3LocationTypeDef",
    {
        "S3Bucket": str,
    },
)
_OptionalS3LocationTypeDef = TypedDict(
    "_OptionalS3LocationTypeDef",
    {
        "S3Key": str,
    },
    total=False,
)


class S3LocationTypeDef(_RequiredS3LocationTypeDef, _OptionalS3LocationTypeDef):
    pass


ApplicationFleetAssociationTypeDef = TypedDict(
    "ApplicationFleetAssociationTypeDef",
    {
        "FleetName": str,
        "ApplicationArn": str,
    },
)

ApplicationSettingsResponseTypeDef = TypedDict(
    "ApplicationSettingsResponseTypeDef",
    {
        "Enabled": bool,
        "SettingsGroup": str,
        "S3BucketName": str,
    },
    total=False,
)

_RequiredApplicationSettingsTypeDef = TypedDict(
    "_RequiredApplicationSettingsTypeDef",
    {
        "Enabled": bool,
    },
)
_OptionalApplicationSettingsTypeDef = TypedDict(
    "_OptionalApplicationSettingsTypeDef",
    {
        "SettingsGroup": str,
    },
    total=False,
)


class ApplicationSettingsTypeDef(
    _RequiredApplicationSettingsTypeDef, _OptionalApplicationSettingsTypeDef
):
    pass


AssociateAppBlockBuilderAppBlockRequestRequestTypeDef = TypedDict(
    "AssociateAppBlockBuilderAppBlockRequestRequestTypeDef",
    {
        "AppBlockArn": str,
        "AppBlockBuilderName": str,
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

AssociateApplicationFleetRequestRequestTypeDef = TypedDict(
    "AssociateApplicationFleetRequestRequestTypeDef",
    {
        "FleetName": str,
        "ApplicationArn": str,
    },
)

AssociateApplicationToEntitlementRequestRequestTypeDef = TypedDict(
    "AssociateApplicationToEntitlementRequestRequestTypeDef",
    {
        "StackName": str,
        "EntitlementName": str,
        "ApplicationIdentifier": str,
    },
)

AssociateFleetRequestRequestTypeDef = TypedDict(
    "AssociateFleetRequestRequestTypeDef",
    {
        "FleetName": str,
        "StackName": str,
    },
)

_RequiredUserStackAssociationTypeDef = TypedDict(
    "_RequiredUserStackAssociationTypeDef",
    {
        "StackName": str,
        "UserName": str,
        "AuthenticationType": AuthenticationTypeType,
    },
)
_OptionalUserStackAssociationTypeDef = TypedDict(
    "_OptionalUserStackAssociationTypeDef",
    {
        "SendEmailNotification": bool,
    },
    total=False,
)


class UserStackAssociationTypeDef(
    _RequiredUserStackAssociationTypeDef, _OptionalUserStackAssociationTypeDef
):
    pass


CertificateBasedAuthPropertiesTypeDef = TypedDict(
    "CertificateBasedAuthPropertiesTypeDef",
    {
        "Status": CertificateBasedAuthStatusType,
        "CertificateAuthorityArn": str,
    },
    total=False,
)

_RequiredComputeCapacityStatusTypeDef = TypedDict(
    "_RequiredComputeCapacityStatusTypeDef",
    {
        "Desired": int,
    },
)
_OptionalComputeCapacityStatusTypeDef = TypedDict(
    "_OptionalComputeCapacityStatusTypeDef",
    {
        "Running": int,
        "InUse": int,
        "Available": int,
    },
    total=False,
)


class ComputeCapacityStatusTypeDef(
    _RequiredComputeCapacityStatusTypeDef, _OptionalComputeCapacityStatusTypeDef
):
    pass


ComputeCapacityTypeDef = TypedDict(
    "ComputeCapacityTypeDef",
    {
        "DesiredInstances": int,
    },
)

_RequiredCopyImageRequestRequestTypeDef = TypedDict(
    "_RequiredCopyImageRequestRequestTypeDef",
    {
        "SourceImageName": str,
        "DestinationImageName": str,
        "DestinationRegion": str,
    },
)
_OptionalCopyImageRequestRequestTypeDef = TypedDict(
    "_OptionalCopyImageRequestRequestTypeDef",
    {
        "DestinationImageDescription": str,
    },
    total=False,
)


class CopyImageRequestRequestTypeDef(
    _RequiredCopyImageRequestRequestTypeDef, _OptionalCopyImageRequestRequestTypeDef
):
    pass


_RequiredCreateAppBlockBuilderStreamingURLRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAppBlockBuilderStreamingURLRequestRequestTypeDef",
    {
        "AppBlockBuilderName": str,
    },
)
_OptionalCreateAppBlockBuilderStreamingURLRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAppBlockBuilderStreamingURLRequestRequestTypeDef",
    {
        "Validity": int,
    },
    total=False,
)


class CreateAppBlockBuilderStreamingURLRequestRequestTypeDef(
    _RequiredCreateAppBlockBuilderStreamingURLRequestRequestTypeDef,
    _OptionalCreateAppBlockBuilderStreamingURLRequestRequestTypeDef,
):
    pass


ServiceAccountCredentialsTypeDef = TypedDict(
    "ServiceAccountCredentialsTypeDef",
    {
        "AccountName": str,
        "AccountPassword": str,
    },
)

EntitlementAttributeTypeDef = TypedDict(
    "EntitlementAttributeTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)

DomainJoinInfoTypeDef = TypedDict(
    "DomainJoinInfoTypeDef",
    {
        "DirectoryName": str,
        "OrganizationalUnitDistinguishedName": str,
    },
    total=False,
)

_RequiredCreateImageBuilderStreamingURLRequestRequestTypeDef = TypedDict(
    "_RequiredCreateImageBuilderStreamingURLRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateImageBuilderStreamingURLRequestRequestTypeDef = TypedDict(
    "_OptionalCreateImageBuilderStreamingURLRequestRequestTypeDef",
    {
        "Validity": int,
    },
    total=False,
)


class CreateImageBuilderStreamingURLRequestRequestTypeDef(
    _RequiredCreateImageBuilderStreamingURLRequestRequestTypeDef,
    _OptionalCreateImageBuilderStreamingURLRequestRequestTypeDef,
):
    pass


_RequiredStorageConnectorTypeDef = TypedDict(
    "_RequiredStorageConnectorTypeDef",
    {
        "ConnectorType": StorageConnectorTypeType,
    },
)
_OptionalStorageConnectorTypeDef = TypedDict(
    "_OptionalStorageConnectorTypeDef",
    {
        "ResourceIdentifier": str,
        "Domains": Sequence[str],
    },
    total=False,
)


class StorageConnectorTypeDef(_RequiredStorageConnectorTypeDef, _OptionalStorageConnectorTypeDef):
    pass


StreamingExperienceSettingsTypeDef = TypedDict(
    "StreamingExperienceSettingsTypeDef",
    {
        "PreferredProtocol": PreferredProtocolType,
    },
    total=False,
)

UserSettingTypeDef = TypedDict(
    "UserSettingTypeDef",
    {
        "Action": ActionType,
        "Permission": PermissionType,
    },
)

_RequiredCreateStreamingURLRequestRequestTypeDef = TypedDict(
    "_RequiredCreateStreamingURLRequestRequestTypeDef",
    {
        "StackName": str,
        "FleetName": str,
        "UserId": str,
    },
)
_OptionalCreateStreamingURLRequestRequestTypeDef = TypedDict(
    "_OptionalCreateStreamingURLRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "Validity": int,
        "SessionContext": str,
    },
    total=False,
)


class CreateStreamingURLRequestRequestTypeDef(
    _RequiredCreateStreamingURLRequestRequestTypeDef,
    _OptionalCreateStreamingURLRequestRequestTypeDef,
):
    pass


_RequiredCreateUpdatedImageRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUpdatedImageRequestRequestTypeDef",
    {
        "existingImageName": str,
        "newImageName": str,
    },
)
_OptionalCreateUpdatedImageRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUpdatedImageRequestRequestTypeDef",
    {
        "newImageDescription": str,
        "newImageDisplayName": str,
        "newImageTags": Mapping[str, str],
        "dryRun": bool,
    },
    total=False,
)


class CreateUpdatedImageRequestRequestTypeDef(
    _RequiredCreateUpdatedImageRequestRequestTypeDef,
    _OptionalCreateUpdatedImageRequestRequestTypeDef,
):
    pass


_RequiredCreateUserRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUserRequestRequestTypeDef",
    {
        "UserName": str,
        "AuthenticationType": AuthenticationTypeType,
    },
)
_OptionalCreateUserRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUserRequestRequestTypeDef",
    {
        "MessageAction": MessageActionType,
        "FirstName": str,
        "LastName": str,
    },
    total=False,
)


class CreateUserRequestRequestTypeDef(
    _RequiredCreateUserRequestRequestTypeDef, _OptionalCreateUserRequestRequestTypeDef
):
    pass


DeleteAppBlockBuilderRequestRequestTypeDef = TypedDict(
    "DeleteAppBlockBuilderRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteAppBlockRequestRequestTypeDef = TypedDict(
    "DeleteAppBlockRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteApplicationRequestRequestTypeDef = TypedDict(
    "DeleteApplicationRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteDirectoryConfigRequestRequestTypeDef = TypedDict(
    "DeleteDirectoryConfigRequestRequestTypeDef",
    {
        "DirectoryName": str,
    },
)

DeleteEntitlementRequestRequestTypeDef = TypedDict(
    "DeleteEntitlementRequestRequestTypeDef",
    {
        "Name": str,
        "StackName": str,
    },
)

DeleteFleetRequestRequestTypeDef = TypedDict(
    "DeleteFleetRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteImageBuilderRequestRequestTypeDef = TypedDict(
    "DeleteImageBuilderRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteImagePermissionsRequestRequestTypeDef = TypedDict(
    "DeleteImagePermissionsRequestRequestTypeDef",
    {
        "Name": str,
        "SharedAccountId": str,
    },
)

DeleteImageRequestRequestTypeDef = TypedDict(
    "DeleteImageRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteStackRequestRequestTypeDef = TypedDict(
    "DeleteStackRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteUserRequestRequestTypeDef = TypedDict(
    "DeleteUserRequestRequestTypeDef",
    {
        "UserName": str,
        "AuthenticationType": AuthenticationTypeType,
    },
)

DescribeAppBlockBuilderAppBlockAssociationsRequestRequestTypeDef = TypedDict(
    "DescribeAppBlockBuilderAppBlockAssociationsRequestRequestTypeDef",
    {
        "AppBlockArn": str,
        "AppBlockBuilderName": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeAppBlockBuildersRequestRequestTypeDef = TypedDict(
    "DescribeAppBlockBuildersRequestRequestTypeDef",
    {
        "Names": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

DescribeAppBlocksRequestRequestTypeDef = TypedDict(
    "DescribeAppBlocksRequestRequestTypeDef",
    {
        "Arns": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

DescribeApplicationFleetAssociationsRequestRequestTypeDef = TypedDict(
    "DescribeApplicationFleetAssociationsRequestRequestTypeDef",
    {
        "FleetName": str,
        "ApplicationArn": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeApplicationsRequestRequestTypeDef = TypedDict(
    "DescribeApplicationsRequestRequestTypeDef",
    {
        "Arns": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
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

DescribeDirectoryConfigsRequestRequestTypeDef = TypedDict(
    "DescribeDirectoryConfigsRequestRequestTypeDef",
    {
        "DirectoryNames": Sequence[str],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredDescribeEntitlementsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeEntitlementsRequestRequestTypeDef",
    {
        "StackName": str,
    },
)
_OptionalDescribeEntitlementsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeEntitlementsRequestRequestTypeDef",
    {
        "Name": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class DescribeEntitlementsRequestRequestTypeDef(
    _RequiredDescribeEntitlementsRequestRequestTypeDef,
    _OptionalDescribeEntitlementsRequestRequestTypeDef,
):
    pass


WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

DescribeFleetsRequestRequestTypeDef = TypedDict(
    "DescribeFleetsRequestRequestTypeDef",
    {
        "Names": Sequence[str],
        "NextToken": str,
    },
    total=False,
)

DescribeImageBuildersRequestRequestTypeDef = TypedDict(
    "DescribeImageBuildersRequestRequestTypeDef",
    {
        "Names": Sequence[str],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredDescribeImagePermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeImagePermissionsRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalDescribeImagePermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeImagePermissionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "SharedAwsAccountIds": Sequence[str],
        "NextToken": str,
    },
    total=False,
)


class DescribeImagePermissionsRequestRequestTypeDef(
    _RequiredDescribeImagePermissionsRequestRequestTypeDef,
    _OptionalDescribeImagePermissionsRequestRequestTypeDef,
):
    pass


DescribeImagesRequestRequestTypeDef = TypedDict(
    "DescribeImagesRequestRequestTypeDef",
    {
        "Names": Sequence[str],
        "Arns": Sequence[str],
        "Type": VisibilityTypeType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredDescribeSessionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeSessionsRequestRequestTypeDef",
    {
        "StackName": str,
        "FleetName": str,
    },
)
_OptionalDescribeSessionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeSessionsRequestRequestTypeDef",
    {
        "UserId": str,
        "NextToken": str,
        "Limit": int,
        "AuthenticationType": AuthenticationTypeType,
    },
    total=False,
)


class DescribeSessionsRequestRequestTypeDef(
    _RequiredDescribeSessionsRequestRequestTypeDef, _OptionalDescribeSessionsRequestRequestTypeDef
):
    pass


DescribeStacksRequestRequestTypeDef = TypedDict(
    "DescribeStacksRequestRequestTypeDef",
    {
        "Names": Sequence[str],
        "NextToken": str,
    },
    total=False,
)

DescribeUsageReportSubscriptionsRequestRequestTypeDef = TypedDict(
    "DescribeUsageReportSubscriptionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeUserStackAssociationsRequestRequestTypeDef = TypedDict(
    "DescribeUserStackAssociationsRequestRequestTypeDef",
    {
        "StackName": str,
        "UserName": str,
        "AuthenticationType": AuthenticationTypeType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredDescribeUsersRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeUsersRequestRequestTypeDef",
    {
        "AuthenticationType": AuthenticationTypeType,
    },
)
_OptionalDescribeUsersRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeUsersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeUsersRequestRequestTypeDef(
    _RequiredDescribeUsersRequestRequestTypeDef, _OptionalDescribeUsersRequestRequestTypeDef
):
    pass


_RequiredUserTypeDef = TypedDict(
    "_RequiredUserTypeDef",
    {
        "AuthenticationType": AuthenticationTypeType,
    },
)
_OptionalUserTypeDef = TypedDict(
    "_OptionalUserTypeDef",
    {
        "Arn": str,
        "UserName": str,
        "Enabled": bool,
        "Status": str,
        "FirstName": str,
        "LastName": str,
        "CreatedTime": datetime,
    },
    total=False,
)


class UserTypeDef(_RequiredUserTypeDef, _OptionalUserTypeDef):
    pass


DisableUserRequestRequestTypeDef = TypedDict(
    "DisableUserRequestRequestTypeDef",
    {
        "UserName": str,
        "AuthenticationType": AuthenticationTypeType,
    },
)

DisassociateAppBlockBuilderAppBlockRequestRequestTypeDef = TypedDict(
    "DisassociateAppBlockBuilderAppBlockRequestRequestTypeDef",
    {
        "AppBlockArn": str,
        "AppBlockBuilderName": str,
    },
)

DisassociateApplicationFleetRequestRequestTypeDef = TypedDict(
    "DisassociateApplicationFleetRequestRequestTypeDef",
    {
        "FleetName": str,
        "ApplicationArn": str,
    },
)

DisassociateApplicationFromEntitlementRequestRequestTypeDef = TypedDict(
    "DisassociateApplicationFromEntitlementRequestRequestTypeDef",
    {
        "StackName": str,
        "EntitlementName": str,
        "ApplicationIdentifier": str,
    },
)

DisassociateFleetRequestRequestTypeDef = TypedDict(
    "DisassociateFleetRequestRequestTypeDef",
    {
        "FleetName": str,
        "StackName": str,
    },
)

EnableUserRequestRequestTypeDef = TypedDict(
    "EnableUserRequestRequestTypeDef",
    {
        "UserName": str,
        "AuthenticationType": AuthenticationTypeType,
    },
)

EntitledApplicationTypeDef = TypedDict(
    "EntitledApplicationTypeDef",
    {
        "ApplicationIdentifier": str,
    },
)

ExpireSessionRequestRequestTypeDef = TypedDict(
    "ExpireSessionRequestRequestTypeDef",
    {
        "SessionId": str,
    },
)

FleetErrorTypeDef = TypedDict(
    "FleetErrorTypeDef",
    {
        "ErrorCode": FleetErrorCodeType,
        "ErrorMessage": str,
    },
    total=False,
)

ImageBuilderStateChangeReasonTypeDef = TypedDict(
    "ImageBuilderStateChangeReasonTypeDef",
    {
        "Code": ImageBuilderStateChangeReasonCodeType,
        "Message": str,
    },
    total=False,
)

NetworkAccessConfigurationTypeDef = TypedDict(
    "NetworkAccessConfigurationTypeDef",
    {
        "EniPrivateIpAddress": str,
        "EniId": str,
    },
    total=False,
)

ImagePermissionsTypeDef = TypedDict(
    "ImagePermissionsTypeDef",
    {
        "allowFleet": bool,
        "allowImageBuilder": bool,
    },
    total=False,
)

ImageStateChangeReasonTypeDef = TypedDict(
    "ImageStateChangeReasonTypeDef",
    {
        "Code": ImageStateChangeReasonCodeType,
        "Message": str,
    },
    total=False,
)

LastReportGenerationExecutionErrorTypeDef = TypedDict(
    "LastReportGenerationExecutionErrorTypeDef",
    {
        "ErrorCode": UsageReportExecutionErrorCodeType,
        "ErrorMessage": str,
    },
    total=False,
)

_RequiredListAssociatedFleetsRequestRequestTypeDef = TypedDict(
    "_RequiredListAssociatedFleetsRequestRequestTypeDef",
    {
        "StackName": str,
    },
)
_OptionalListAssociatedFleetsRequestRequestTypeDef = TypedDict(
    "_OptionalListAssociatedFleetsRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListAssociatedFleetsRequestRequestTypeDef(
    _RequiredListAssociatedFleetsRequestRequestTypeDef,
    _OptionalListAssociatedFleetsRequestRequestTypeDef,
):
    pass


_RequiredListAssociatedStacksRequestRequestTypeDef = TypedDict(
    "_RequiredListAssociatedStacksRequestRequestTypeDef",
    {
        "FleetName": str,
    },
)
_OptionalListAssociatedStacksRequestRequestTypeDef = TypedDict(
    "_OptionalListAssociatedStacksRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListAssociatedStacksRequestRequestTypeDef(
    _RequiredListAssociatedStacksRequestRequestTypeDef,
    _OptionalListAssociatedStacksRequestRequestTypeDef,
):
    pass


_RequiredListEntitledApplicationsRequestRequestTypeDef = TypedDict(
    "_RequiredListEntitledApplicationsRequestRequestTypeDef",
    {
        "StackName": str,
        "EntitlementName": str,
    },
)
_OptionalListEntitledApplicationsRequestRequestTypeDef = TypedDict(
    "_OptionalListEntitledApplicationsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListEntitledApplicationsRequestRequestTypeDef(
    _RequiredListEntitledApplicationsRequestRequestTypeDef,
    _OptionalListEntitledApplicationsRequestRequestTypeDef,
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

StackErrorTypeDef = TypedDict(
    "StackErrorTypeDef",
    {
        "ErrorCode": StackErrorCodeType,
        "ErrorMessage": str,
    },
    total=False,
)

StartAppBlockBuilderRequestRequestTypeDef = TypedDict(
    "StartAppBlockBuilderRequestRequestTypeDef",
    {
        "Name": str,
    },
)

StartFleetRequestRequestTypeDef = TypedDict(
    "StartFleetRequestRequestTypeDef",
    {
        "Name": str,
    },
)

_RequiredStartImageBuilderRequestRequestTypeDef = TypedDict(
    "_RequiredStartImageBuilderRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalStartImageBuilderRequestRequestTypeDef = TypedDict(
    "_OptionalStartImageBuilderRequestRequestTypeDef",
    {
        "AppstreamAgentVersion": str,
    },
    total=False,
)


class StartImageBuilderRequestRequestTypeDef(
    _RequiredStartImageBuilderRequestRequestTypeDef, _OptionalStartImageBuilderRequestRequestTypeDef
):
    pass


StopAppBlockBuilderRequestRequestTypeDef = TypedDict(
    "StopAppBlockBuilderRequestRequestTypeDef",
    {
        "Name": str,
    },
)

StopFleetRequestRequestTypeDef = TypedDict(
    "StopFleetRequestRequestTypeDef",
    {
        "Name": str,
    },
)

StopImageBuilderRequestRequestTypeDef = TypedDict(
    "StopImageBuilderRequestRequestTypeDef",
    {
        "Name": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredAppBlockBuilderTypeDef = TypedDict(
    "_RequiredAppBlockBuilderTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Platform": Literal["WINDOWS_SERVER_2019"],
        "InstanceType": str,
        "VpcConfig": VpcConfigTypeDef,
        "State": AppBlockBuilderStateType,
    },
)
_OptionalAppBlockBuilderTypeDef = TypedDict(
    "_OptionalAppBlockBuilderTypeDef",
    {
        "DisplayName": str,
        "Description": str,
        "EnableDefaultInternetAccess": bool,
        "IamRoleArn": str,
        "CreatedTime": datetime,
        "AppBlockBuilderErrors": List[ResourceErrorTypeDef],
        "StateChangeReason": AppBlockBuilderStateChangeReasonTypeDef,
        "AccessEndpoints": List[AccessEndpointTypeDef],
    },
    total=False,
)


class AppBlockBuilderTypeDef(_RequiredAppBlockBuilderTypeDef, _OptionalAppBlockBuilderTypeDef):
    pass


_RequiredCreateAppBlockBuilderRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAppBlockBuilderRequestRequestTypeDef",
    {
        "Name": str,
        "Platform": Literal["WINDOWS_SERVER_2019"],
        "InstanceType": str,
        "VpcConfig": VpcConfigTypeDef,
    },
)
_OptionalCreateAppBlockBuilderRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAppBlockBuilderRequestRequestTypeDef",
    {
        "Description": str,
        "DisplayName": str,
        "Tags": Mapping[str, str],
        "EnableDefaultInternetAccess": bool,
        "IamRoleArn": str,
        "AccessEndpoints": Sequence[AccessEndpointTypeDef],
    },
    total=False,
)


class CreateAppBlockBuilderRequestRequestTypeDef(
    _RequiredCreateAppBlockBuilderRequestRequestTypeDef,
    _OptionalCreateAppBlockBuilderRequestRequestTypeDef,
):
    pass


_RequiredUpdateAppBlockBuilderRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAppBlockBuilderRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateAppBlockBuilderRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAppBlockBuilderRequestRequestTypeDef",
    {
        "Description": str,
        "DisplayName": str,
        "Platform": PlatformTypeType,
        "InstanceType": str,
        "VpcConfig": VpcConfigTypeDef,
        "EnableDefaultInternetAccess": bool,
        "IamRoleArn": str,
        "AccessEndpoints": Sequence[AccessEndpointTypeDef],
        "AttributesToDelete": Sequence[AppBlockBuilderAttributeType],
    },
    total=False,
)


class UpdateAppBlockBuilderRequestRequestTypeDef(
    _RequiredUpdateAppBlockBuilderRequestRequestTypeDef,
    _OptionalUpdateAppBlockBuilderRequestRequestTypeDef,
):
    pass


ApplicationTypeDef = TypedDict(
    "ApplicationTypeDef",
    {
        "Name": str,
        "DisplayName": str,
        "IconURL": str,
        "LaunchPath": str,
        "LaunchParameters": str,
        "Enabled": bool,
        "Metadata": Dict[str, str],
        "WorkingDirectory": str,
        "Description": str,
        "Arn": str,
        "AppBlockArn": str,
        "IconS3Location": S3LocationTypeDef,
        "Platforms": List[PlatformTypeType],
        "InstanceFamilies": List[str],
        "CreatedTime": datetime,
    },
    total=False,
)

_RequiredCreateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateApplicationRequestRequestTypeDef",
    {
        "Name": str,
        "IconS3Location": S3LocationTypeDef,
        "LaunchPath": str,
        "Platforms": Sequence[PlatformTypeType],
        "InstanceFamilies": Sequence[str],
        "AppBlockArn": str,
    },
)
_OptionalCreateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateApplicationRequestRequestTypeDef",
    {
        "DisplayName": str,
        "Description": str,
        "WorkingDirectory": str,
        "LaunchParameters": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateApplicationRequestRequestTypeDef(
    _RequiredCreateApplicationRequestRequestTypeDef, _OptionalCreateApplicationRequestRequestTypeDef
):
    pass


_RequiredScriptDetailsTypeDef = TypedDict(
    "_RequiredScriptDetailsTypeDef",
    {
        "ScriptS3Location": S3LocationTypeDef,
        "ExecutablePath": str,
        "TimeoutInSeconds": int,
    },
)
_OptionalScriptDetailsTypeDef = TypedDict(
    "_OptionalScriptDetailsTypeDef",
    {
        "ExecutableParameters": str,
    },
    total=False,
)


class ScriptDetailsTypeDef(_RequiredScriptDetailsTypeDef, _OptionalScriptDetailsTypeDef):
    pass


_RequiredUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateApplicationRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateApplicationRequestRequestTypeDef",
    {
        "DisplayName": str,
        "Description": str,
        "IconS3Location": S3LocationTypeDef,
        "LaunchPath": str,
        "WorkingDirectory": str,
        "LaunchParameters": str,
        "AppBlockArn": str,
        "AttributesToDelete": Sequence[ApplicationAttributeType],
    },
    total=False,
)


class UpdateApplicationRequestRequestTypeDef(
    _RequiredUpdateApplicationRequestRequestTypeDef, _OptionalUpdateApplicationRequestRequestTypeDef
):
    pass


AssociateAppBlockBuilderAppBlockResultTypeDef = TypedDict(
    "AssociateAppBlockBuilderAppBlockResultTypeDef",
    {
        "AppBlockBuilderAppBlockAssociation": AppBlockBuilderAppBlockAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateApplicationFleetResultTypeDef = TypedDict(
    "AssociateApplicationFleetResultTypeDef",
    {
        "ApplicationFleetAssociation": ApplicationFleetAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CopyImageResponseTypeDef = TypedDict(
    "CopyImageResponseTypeDef",
    {
        "DestinationImageName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAppBlockBuilderStreamingURLResultTypeDef = TypedDict(
    "CreateAppBlockBuilderStreamingURLResultTypeDef",
    {
        "StreamingURL": str,
        "Expires": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateImageBuilderStreamingURLResultTypeDef = TypedDict(
    "CreateImageBuilderStreamingURLResultTypeDef",
    {
        "StreamingURL": str,
        "Expires": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateStreamingURLResultTypeDef = TypedDict(
    "CreateStreamingURLResultTypeDef",
    {
        "StreamingURL": str,
        "Expires": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateUsageReportSubscriptionResultTypeDef = TypedDict(
    "CreateUsageReportSubscriptionResultTypeDef",
    {
        "S3BucketName": str,
        "Schedule": Literal["DAILY"],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppBlockBuilderAppBlockAssociationsResultTypeDef = TypedDict(
    "DescribeAppBlockBuilderAppBlockAssociationsResultTypeDef",
    {
        "AppBlockBuilderAppBlockAssociations": List[AppBlockBuilderAppBlockAssociationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeApplicationFleetAssociationsResultTypeDef = TypedDict(
    "DescribeApplicationFleetAssociationsResultTypeDef",
    {
        "ApplicationFleetAssociations": List[ApplicationFleetAssociationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssociatedFleetsResultTypeDef = TypedDict(
    "ListAssociatedFleetsResultTypeDef",
    {
        "Names": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssociatedStacksResultTypeDef = TypedDict(
    "ListAssociatedStacksResultTypeDef",
    {
        "Names": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchAssociateUserStackRequestRequestTypeDef = TypedDict(
    "BatchAssociateUserStackRequestRequestTypeDef",
    {
        "UserStackAssociations": Sequence[UserStackAssociationTypeDef],
    },
)

BatchDisassociateUserStackRequestRequestTypeDef = TypedDict(
    "BatchDisassociateUserStackRequestRequestTypeDef",
    {
        "UserStackAssociations": Sequence[UserStackAssociationTypeDef],
    },
)

DescribeUserStackAssociationsResultTypeDef = TypedDict(
    "DescribeUserStackAssociationsResultTypeDef",
    {
        "UserStackAssociations": List[UserStackAssociationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UserStackAssociationErrorTypeDef = TypedDict(
    "UserStackAssociationErrorTypeDef",
    {
        "UserStackAssociation": UserStackAssociationTypeDef,
        "ErrorCode": UserStackAssociationErrorCodeType,
        "ErrorMessage": str,
    },
    total=False,
)

_RequiredCreateDirectoryConfigRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDirectoryConfigRequestRequestTypeDef",
    {
        "DirectoryName": str,
        "OrganizationalUnitDistinguishedNames": Sequence[str],
    },
)
_OptionalCreateDirectoryConfigRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDirectoryConfigRequestRequestTypeDef",
    {
        "ServiceAccountCredentials": ServiceAccountCredentialsTypeDef,
        "CertificateBasedAuthProperties": CertificateBasedAuthPropertiesTypeDef,
    },
    total=False,
)


class CreateDirectoryConfigRequestRequestTypeDef(
    _RequiredCreateDirectoryConfigRequestRequestTypeDef,
    _OptionalCreateDirectoryConfigRequestRequestTypeDef,
):
    pass


_RequiredDirectoryConfigTypeDef = TypedDict(
    "_RequiredDirectoryConfigTypeDef",
    {
        "DirectoryName": str,
    },
)
_OptionalDirectoryConfigTypeDef = TypedDict(
    "_OptionalDirectoryConfigTypeDef",
    {
        "OrganizationalUnitDistinguishedNames": List[str],
        "ServiceAccountCredentials": ServiceAccountCredentialsTypeDef,
        "CreatedTime": datetime,
        "CertificateBasedAuthProperties": CertificateBasedAuthPropertiesTypeDef,
    },
    total=False,
)


class DirectoryConfigTypeDef(_RequiredDirectoryConfigTypeDef, _OptionalDirectoryConfigTypeDef):
    pass


_RequiredUpdateDirectoryConfigRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDirectoryConfigRequestRequestTypeDef",
    {
        "DirectoryName": str,
    },
)
_OptionalUpdateDirectoryConfigRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDirectoryConfigRequestRequestTypeDef",
    {
        "OrganizationalUnitDistinguishedNames": Sequence[str],
        "ServiceAccountCredentials": ServiceAccountCredentialsTypeDef,
        "CertificateBasedAuthProperties": CertificateBasedAuthPropertiesTypeDef,
    },
    total=False,
)


class UpdateDirectoryConfigRequestRequestTypeDef(
    _RequiredUpdateDirectoryConfigRequestRequestTypeDef,
    _OptionalUpdateDirectoryConfigRequestRequestTypeDef,
):
    pass


_RequiredCreateEntitlementRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEntitlementRequestRequestTypeDef",
    {
        "Name": str,
        "StackName": str,
        "AppVisibility": AppVisibilityType,
        "Attributes": Sequence[EntitlementAttributeTypeDef],
    },
)
_OptionalCreateEntitlementRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEntitlementRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class CreateEntitlementRequestRequestTypeDef(
    _RequiredCreateEntitlementRequestRequestTypeDef, _OptionalCreateEntitlementRequestRequestTypeDef
):
    pass


_RequiredEntitlementTypeDef = TypedDict(
    "_RequiredEntitlementTypeDef",
    {
        "Name": str,
        "StackName": str,
        "AppVisibility": AppVisibilityType,
        "Attributes": List[EntitlementAttributeTypeDef],
    },
)
_OptionalEntitlementTypeDef = TypedDict(
    "_OptionalEntitlementTypeDef",
    {
        "Description": str,
        "CreatedTime": datetime,
        "LastModifiedTime": datetime,
    },
    total=False,
)


class EntitlementTypeDef(_RequiredEntitlementTypeDef, _OptionalEntitlementTypeDef):
    pass


_RequiredUpdateEntitlementRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateEntitlementRequestRequestTypeDef",
    {
        "Name": str,
        "StackName": str,
    },
)
_OptionalUpdateEntitlementRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateEntitlementRequestRequestTypeDef",
    {
        "Description": str,
        "AppVisibility": AppVisibilityType,
        "Attributes": Sequence[EntitlementAttributeTypeDef],
    },
    total=False,
)


class UpdateEntitlementRequestRequestTypeDef(
    _RequiredUpdateEntitlementRequestRequestTypeDef, _OptionalUpdateEntitlementRequestRequestTypeDef
):
    pass


_RequiredCreateFleetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFleetRequestRequestTypeDef",
    {
        "Name": str,
        "InstanceType": str,
    },
)
_OptionalCreateFleetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFleetRequestRequestTypeDef",
    {
        "ImageName": str,
        "ImageArn": str,
        "FleetType": FleetTypeType,
        "ComputeCapacity": ComputeCapacityTypeDef,
        "VpcConfig": VpcConfigTypeDef,
        "MaxUserDurationInSeconds": int,
        "DisconnectTimeoutInSeconds": int,
        "Description": str,
        "DisplayName": str,
        "EnableDefaultInternetAccess": bool,
        "DomainJoinInfo": DomainJoinInfoTypeDef,
        "Tags": Mapping[str, str],
        "IdleDisconnectTimeoutInSeconds": int,
        "IamRoleArn": str,
        "StreamView": StreamViewType,
        "Platform": PlatformTypeType,
        "MaxConcurrentSessions": int,
        "UsbDeviceFilterStrings": Sequence[str],
        "SessionScriptS3Location": S3LocationTypeDef,
    },
    total=False,
)


class CreateFleetRequestRequestTypeDef(
    _RequiredCreateFleetRequestRequestTypeDef, _OptionalCreateFleetRequestRequestTypeDef
):
    pass


_RequiredCreateImageBuilderRequestRequestTypeDef = TypedDict(
    "_RequiredCreateImageBuilderRequestRequestTypeDef",
    {
        "Name": str,
        "InstanceType": str,
    },
)
_OptionalCreateImageBuilderRequestRequestTypeDef = TypedDict(
    "_OptionalCreateImageBuilderRequestRequestTypeDef",
    {
        "ImageName": str,
        "ImageArn": str,
        "Description": str,
        "DisplayName": str,
        "VpcConfig": VpcConfigTypeDef,
        "IamRoleArn": str,
        "EnableDefaultInternetAccess": bool,
        "DomainJoinInfo": DomainJoinInfoTypeDef,
        "AppstreamAgentVersion": str,
        "Tags": Mapping[str, str],
        "AccessEndpoints": Sequence[AccessEndpointTypeDef],
    },
    total=False,
)


class CreateImageBuilderRequestRequestTypeDef(
    _RequiredCreateImageBuilderRequestRequestTypeDef,
    _OptionalCreateImageBuilderRequestRequestTypeDef,
):
    pass


UpdateFleetRequestRequestTypeDef = TypedDict(
    "UpdateFleetRequestRequestTypeDef",
    {
        "ImageName": str,
        "ImageArn": str,
        "Name": str,
        "InstanceType": str,
        "ComputeCapacity": ComputeCapacityTypeDef,
        "VpcConfig": VpcConfigTypeDef,
        "MaxUserDurationInSeconds": int,
        "DisconnectTimeoutInSeconds": int,
        "DeleteVpcConfig": bool,
        "Description": str,
        "DisplayName": str,
        "EnableDefaultInternetAccess": bool,
        "DomainJoinInfo": DomainJoinInfoTypeDef,
        "IdleDisconnectTimeoutInSeconds": int,
        "AttributesToDelete": Sequence[FleetAttributeType],
        "IamRoleArn": str,
        "StreamView": StreamViewType,
        "Platform": PlatformTypeType,
        "MaxConcurrentSessions": int,
        "UsbDeviceFilterStrings": Sequence[str],
        "SessionScriptS3Location": S3LocationTypeDef,
    },
    total=False,
)

_RequiredCreateStackRequestRequestTypeDef = TypedDict(
    "_RequiredCreateStackRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateStackRequestRequestTypeDef = TypedDict(
    "_OptionalCreateStackRequestRequestTypeDef",
    {
        "Description": str,
        "DisplayName": str,
        "StorageConnectors": Sequence[StorageConnectorTypeDef],
        "RedirectURL": str,
        "FeedbackURL": str,
        "UserSettings": Sequence[UserSettingTypeDef],
        "ApplicationSettings": ApplicationSettingsTypeDef,
        "Tags": Mapping[str, str],
        "AccessEndpoints": Sequence[AccessEndpointTypeDef],
        "EmbedHostDomains": Sequence[str],
        "StreamingExperienceSettings": StreamingExperienceSettingsTypeDef,
    },
    total=False,
)


class CreateStackRequestRequestTypeDef(
    _RequiredCreateStackRequestRequestTypeDef, _OptionalCreateStackRequestRequestTypeDef
):
    pass


_RequiredUpdateStackRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateStackRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateStackRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateStackRequestRequestTypeDef",
    {
        "DisplayName": str,
        "Description": str,
        "StorageConnectors": Sequence[StorageConnectorTypeDef],
        "DeleteStorageConnectors": bool,
        "RedirectURL": str,
        "FeedbackURL": str,
        "AttributesToDelete": Sequence[StackAttributeType],
        "UserSettings": Sequence[UserSettingTypeDef],
        "ApplicationSettings": ApplicationSettingsTypeDef,
        "AccessEndpoints": Sequence[AccessEndpointTypeDef],
        "EmbedHostDomains": Sequence[str],
        "StreamingExperienceSettings": StreamingExperienceSettingsTypeDef,
    },
    total=False,
)


class UpdateStackRequestRequestTypeDef(
    _RequiredUpdateStackRequestRequestTypeDef, _OptionalUpdateStackRequestRequestTypeDef
):
    pass


DescribeDirectoryConfigsRequestDescribeDirectoryConfigsPaginateTypeDef = TypedDict(
    "DescribeDirectoryConfigsRequestDescribeDirectoryConfigsPaginateTypeDef",
    {
        "DirectoryNames": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeFleetsRequestDescribeFleetsPaginateTypeDef = TypedDict(
    "DescribeFleetsRequestDescribeFleetsPaginateTypeDef",
    {
        "Names": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeImageBuildersRequestDescribeImageBuildersPaginateTypeDef = TypedDict(
    "DescribeImageBuildersRequestDescribeImageBuildersPaginateTypeDef",
    {
        "Names": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeImagesRequestDescribeImagesPaginateTypeDef = TypedDict(
    "DescribeImagesRequestDescribeImagesPaginateTypeDef",
    {
        "Names": Sequence[str],
        "Arns": Sequence[str],
        "Type": VisibilityTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeSessionsRequestDescribeSessionsPaginateTypeDef = TypedDict(
    "_RequiredDescribeSessionsRequestDescribeSessionsPaginateTypeDef",
    {
        "StackName": str,
        "FleetName": str,
    },
)
_OptionalDescribeSessionsRequestDescribeSessionsPaginateTypeDef = TypedDict(
    "_OptionalDescribeSessionsRequestDescribeSessionsPaginateTypeDef",
    {
        "UserId": str,
        "AuthenticationType": AuthenticationTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeSessionsRequestDescribeSessionsPaginateTypeDef(
    _RequiredDescribeSessionsRequestDescribeSessionsPaginateTypeDef,
    _OptionalDescribeSessionsRequestDescribeSessionsPaginateTypeDef,
):
    pass


DescribeStacksRequestDescribeStacksPaginateTypeDef = TypedDict(
    "DescribeStacksRequestDescribeStacksPaginateTypeDef",
    {
        "Names": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeUserStackAssociationsRequestDescribeUserStackAssociationsPaginateTypeDef = TypedDict(
    "DescribeUserStackAssociationsRequestDescribeUserStackAssociationsPaginateTypeDef",
    {
        "StackName": str,
        "UserName": str,
        "AuthenticationType": AuthenticationTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeUsersRequestDescribeUsersPaginateTypeDef = TypedDict(
    "_RequiredDescribeUsersRequestDescribeUsersPaginateTypeDef",
    {
        "AuthenticationType": AuthenticationTypeType,
    },
)
_OptionalDescribeUsersRequestDescribeUsersPaginateTypeDef = TypedDict(
    "_OptionalDescribeUsersRequestDescribeUsersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeUsersRequestDescribeUsersPaginateTypeDef(
    _RequiredDescribeUsersRequestDescribeUsersPaginateTypeDef,
    _OptionalDescribeUsersRequestDescribeUsersPaginateTypeDef,
):
    pass


_RequiredListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef = TypedDict(
    "_RequiredListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef",
    {
        "StackName": str,
    },
)
_OptionalListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef = TypedDict(
    "_OptionalListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef(
    _RequiredListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef,
    _OptionalListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef,
):
    pass


_RequiredListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef = TypedDict(
    "_RequiredListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef",
    {
        "FleetName": str,
    },
)
_OptionalListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef = TypedDict(
    "_OptionalListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef(
    _RequiredListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef,
    _OptionalListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef,
):
    pass


DescribeFleetsRequestFleetStartedWaitTypeDef = TypedDict(
    "DescribeFleetsRequestFleetStartedWaitTypeDef",
    {
        "Names": Sequence[str],
        "NextToken": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeFleetsRequestFleetStoppedWaitTypeDef = TypedDict(
    "DescribeFleetsRequestFleetStoppedWaitTypeDef",
    {
        "Names": Sequence[str],
        "NextToken": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeUsersResultTypeDef = TypedDict(
    "DescribeUsersResultTypeDef",
    {
        "Users": List[UserTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEntitledApplicationsResultTypeDef = TypedDict(
    "ListEntitledApplicationsResultTypeDef",
    {
        "EntitledApplications": List[EntitledApplicationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredFleetTypeDef = TypedDict(
    "_RequiredFleetTypeDef",
    {
        "Arn": str,
        "Name": str,
        "InstanceType": str,
        "ComputeCapacityStatus": ComputeCapacityStatusTypeDef,
        "State": FleetStateType,
    },
)
_OptionalFleetTypeDef = TypedDict(
    "_OptionalFleetTypeDef",
    {
        "DisplayName": str,
        "Description": str,
        "ImageName": str,
        "ImageArn": str,
        "FleetType": FleetTypeType,
        "MaxUserDurationInSeconds": int,
        "DisconnectTimeoutInSeconds": int,
        "VpcConfig": VpcConfigTypeDef,
        "CreatedTime": datetime,
        "FleetErrors": List[FleetErrorTypeDef],
        "EnableDefaultInternetAccess": bool,
        "DomainJoinInfo": DomainJoinInfoTypeDef,
        "IdleDisconnectTimeoutInSeconds": int,
        "IamRoleArn": str,
        "StreamView": StreamViewType,
        "Platform": PlatformTypeType,
        "MaxConcurrentSessions": int,
        "UsbDeviceFilterStrings": List[str],
        "SessionScriptS3Location": S3LocationTypeDef,
    },
    total=False,
)


class FleetTypeDef(_RequiredFleetTypeDef, _OptionalFleetTypeDef):
    pass


_RequiredImageBuilderTypeDef = TypedDict(
    "_RequiredImageBuilderTypeDef",
    {
        "Name": str,
    },
)
_OptionalImageBuilderTypeDef = TypedDict(
    "_OptionalImageBuilderTypeDef",
    {
        "Arn": str,
        "ImageArn": str,
        "Description": str,
        "DisplayName": str,
        "VpcConfig": VpcConfigTypeDef,
        "InstanceType": str,
        "Platform": PlatformTypeType,
        "IamRoleArn": str,
        "State": ImageBuilderStateType,
        "StateChangeReason": ImageBuilderStateChangeReasonTypeDef,
        "CreatedTime": datetime,
        "EnableDefaultInternetAccess": bool,
        "DomainJoinInfo": DomainJoinInfoTypeDef,
        "NetworkAccessConfiguration": NetworkAccessConfigurationTypeDef,
        "ImageBuilderErrors": List[ResourceErrorTypeDef],
        "AppstreamAgentVersion": str,
        "AccessEndpoints": List[AccessEndpointTypeDef],
    },
    total=False,
)


class ImageBuilderTypeDef(_RequiredImageBuilderTypeDef, _OptionalImageBuilderTypeDef):
    pass


_RequiredSessionTypeDef = TypedDict(
    "_RequiredSessionTypeDef",
    {
        "Id": str,
        "UserId": str,
        "StackName": str,
        "FleetName": str,
        "State": SessionStateType,
    },
)
_OptionalSessionTypeDef = TypedDict(
    "_OptionalSessionTypeDef",
    {
        "ConnectionState": SessionConnectionStateType,
        "StartTime": datetime,
        "MaxExpirationTime": datetime,
        "AuthenticationType": AuthenticationTypeType,
        "NetworkAccessConfiguration": NetworkAccessConfigurationTypeDef,
    },
    total=False,
)


class SessionTypeDef(_RequiredSessionTypeDef, _OptionalSessionTypeDef):
    pass


SharedImagePermissionsTypeDef = TypedDict(
    "SharedImagePermissionsTypeDef",
    {
        "sharedAccountId": str,
        "imagePermissions": ImagePermissionsTypeDef,
    },
)

UpdateImagePermissionsRequestRequestTypeDef = TypedDict(
    "UpdateImagePermissionsRequestRequestTypeDef",
    {
        "Name": str,
        "SharedAccountId": str,
        "ImagePermissions": ImagePermissionsTypeDef,
    },
)

UsageReportSubscriptionTypeDef = TypedDict(
    "UsageReportSubscriptionTypeDef",
    {
        "S3BucketName": str,
        "Schedule": Literal["DAILY"],
        "LastGeneratedReportDate": datetime,
        "SubscriptionErrors": List[LastReportGenerationExecutionErrorTypeDef],
    },
    total=False,
)

_RequiredStackTypeDef = TypedDict(
    "_RequiredStackTypeDef",
    {
        "Name": str,
    },
)
_OptionalStackTypeDef = TypedDict(
    "_OptionalStackTypeDef",
    {
        "Arn": str,
        "Description": str,
        "DisplayName": str,
        "CreatedTime": datetime,
        "StorageConnectors": List[StorageConnectorTypeDef],
        "RedirectURL": str,
        "FeedbackURL": str,
        "StackErrors": List[StackErrorTypeDef],
        "UserSettings": List[UserSettingTypeDef],
        "ApplicationSettings": ApplicationSettingsResponseTypeDef,
        "AccessEndpoints": List[AccessEndpointTypeDef],
        "EmbedHostDomains": List[str],
        "StreamingExperienceSettings": StreamingExperienceSettingsTypeDef,
    },
    total=False,
)


class StackTypeDef(_RequiredStackTypeDef, _OptionalStackTypeDef):
    pass


CreateAppBlockBuilderResultTypeDef = TypedDict(
    "CreateAppBlockBuilderResultTypeDef",
    {
        "AppBlockBuilder": AppBlockBuilderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppBlockBuildersResultTypeDef = TypedDict(
    "DescribeAppBlockBuildersResultTypeDef",
    {
        "AppBlockBuilders": List[AppBlockBuilderTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartAppBlockBuilderResultTypeDef = TypedDict(
    "StartAppBlockBuilderResultTypeDef",
    {
        "AppBlockBuilder": AppBlockBuilderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopAppBlockBuilderResultTypeDef = TypedDict(
    "StopAppBlockBuilderResultTypeDef",
    {
        "AppBlockBuilder": AppBlockBuilderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAppBlockBuilderResultTypeDef = TypedDict(
    "UpdateAppBlockBuilderResultTypeDef",
    {
        "AppBlockBuilder": AppBlockBuilderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateApplicationResultTypeDef = TypedDict(
    "CreateApplicationResultTypeDef",
    {
        "Application": ApplicationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeApplicationsResultTypeDef = TypedDict(
    "DescribeApplicationsResultTypeDef",
    {
        "Applications": List[ApplicationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredImageTypeDef = TypedDict(
    "_RequiredImageTypeDef",
    {
        "Name": str,
    },
)
_OptionalImageTypeDef = TypedDict(
    "_OptionalImageTypeDef",
    {
        "Arn": str,
        "BaseImageArn": str,
        "DisplayName": str,
        "State": ImageStateType,
        "Visibility": VisibilityTypeType,
        "ImageBuilderSupported": bool,
        "ImageBuilderName": str,
        "Platform": PlatformTypeType,
        "Description": str,
        "StateChangeReason": ImageStateChangeReasonTypeDef,
        "Applications": List[ApplicationTypeDef],
        "CreatedTime": datetime,
        "PublicBaseImageReleasedDate": datetime,
        "AppstreamAgentVersion": str,
        "ImagePermissions": ImagePermissionsTypeDef,
        "ImageErrors": List[ResourceErrorTypeDef],
    },
    total=False,
)


class ImageTypeDef(_RequiredImageTypeDef, _OptionalImageTypeDef):
    pass


UpdateApplicationResultTypeDef = TypedDict(
    "UpdateApplicationResultTypeDef",
    {
        "Application": ApplicationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAppBlockTypeDef = TypedDict(
    "_RequiredAppBlockTypeDef",
    {
        "Name": str,
        "Arn": str,
    },
)
_OptionalAppBlockTypeDef = TypedDict(
    "_OptionalAppBlockTypeDef",
    {
        "Description": str,
        "DisplayName": str,
        "SourceS3Location": S3LocationTypeDef,
        "SetupScriptDetails": ScriptDetailsTypeDef,
        "CreatedTime": datetime,
        "PostSetupScriptDetails": ScriptDetailsTypeDef,
        "PackagingType": PackagingTypeType,
        "State": AppBlockStateType,
        "AppBlockErrors": List[ErrorDetailsTypeDef],
    },
    total=False,
)


class AppBlockTypeDef(_RequiredAppBlockTypeDef, _OptionalAppBlockTypeDef):
    pass


_RequiredCreateAppBlockRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAppBlockRequestRequestTypeDef",
    {
        "Name": str,
        "SourceS3Location": S3LocationTypeDef,
    },
)
_OptionalCreateAppBlockRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAppBlockRequestRequestTypeDef",
    {
        "Description": str,
        "DisplayName": str,
        "SetupScriptDetails": ScriptDetailsTypeDef,
        "Tags": Mapping[str, str],
        "PostSetupScriptDetails": ScriptDetailsTypeDef,
        "PackagingType": PackagingTypeType,
    },
    total=False,
)


class CreateAppBlockRequestRequestTypeDef(
    _RequiredCreateAppBlockRequestRequestTypeDef, _OptionalCreateAppBlockRequestRequestTypeDef
):
    pass


BatchAssociateUserStackResultTypeDef = TypedDict(
    "BatchAssociateUserStackResultTypeDef",
    {
        "errors": List[UserStackAssociationErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDisassociateUserStackResultTypeDef = TypedDict(
    "BatchDisassociateUserStackResultTypeDef",
    {
        "errors": List[UserStackAssociationErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDirectoryConfigResultTypeDef = TypedDict(
    "CreateDirectoryConfigResultTypeDef",
    {
        "DirectoryConfig": DirectoryConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDirectoryConfigsResultTypeDef = TypedDict(
    "DescribeDirectoryConfigsResultTypeDef",
    {
        "DirectoryConfigs": List[DirectoryConfigTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDirectoryConfigResultTypeDef = TypedDict(
    "UpdateDirectoryConfigResultTypeDef",
    {
        "DirectoryConfig": DirectoryConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEntitlementResultTypeDef = TypedDict(
    "CreateEntitlementResultTypeDef",
    {
        "Entitlement": EntitlementTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEntitlementsResultTypeDef = TypedDict(
    "DescribeEntitlementsResultTypeDef",
    {
        "Entitlements": List[EntitlementTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEntitlementResultTypeDef = TypedDict(
    "UpdateEntitlementResultTypeDef",
    {
        "Entitlement": EntitlementTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFleetResultTypeDef = TypedDict(
    "CreateFleetResultTypeDef",
    {
        "Fleet": FleetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFleetsResultTypeDef = TypedDict(
    "DescribeFleetsResultTypeDef",
    {
        "Fleets": List[FleetTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFleetResultTypeDef = TypedDict(
    "UpdateFleetResultTypeDef",
    {
        "Fleet": FleetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateImageBuilderResultTypeDef = TypedDict(
    "CreateImageBuilderResultTypeDef",
    {
        "ImageBuilder": ImageBuilderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteImageBuilderResultTypeDef = TypedDict(
    "DeleteImageBuilderResultTypeDef",
    {
        "ImageBuilder": ImageBuilderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeImageBuildersResultTypeDef = TypedDict(
    "DescribeImageBuildersResultTypeDef",
    {
        "ImageBuilders": List[ImageBuilderTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartImageBuilderResultTypeDef = TypedDict(
    "StartImageBuilderResultTypeDef",
    {
        "ImageBuilder": ImageBuilderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopImageBuilderResultTypeDef = TypedDict(
    "StopImageBuilderResultTypeDef",
    {
        "ImageBuilder": ImageBuilderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSessionsResultTypeDef = TypedDict(
    "DescribeSessionsResultTypeDef",
    {
        "Sessions": List[SessionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeImagePermissionsResultTypeDef = TypedDict(
    "DescribeImagePermissionsResultTypeDef",
    {
        "Name": str,
        "SharedImagePermissionsList": List[SharedImagePermissionsTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeUsageReportSubscriptionsResultTypeDef = TypedDict(
    "DescribeUsageReportSubscriptionsResultTypeDef",
    {
        "UsageReportSubscriptions": List[UsageReportSubscriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateStackResultTypeDef = TypedDict(
    "CreateStackResultTypeDef",
    {
        "Stack": StackTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeStacksResultTypeDef = TypedDict(
    "DescribeStacksResultTypeDef",
    {
        "Stacks": List[StackTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateStackResultTypeDef = TypedDict(
    "UpdateStackResultTypeDef",
    {
        "Stack": StackTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateUpdatedImageResultTypeDef = TypedDict(
    "CreateUpdatedImageResultTypeDef",
    {
        "image": ImageTypeDef,
        "canUpdateImage": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteImageResultTypeDef = TypedDict(
    "DeleteImageResultTypeDef",
    {
        "Image": ImageTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeImagesResultTypeDef = TypedDict(
    "DescribeImagesResultTypeDef",
    {
        "Images": List[ImageTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAppBlockResultTypeDef = TypedDict(
    "CreateAppBlockResultTypeDef",
    {
        "AppBlock": AppBlockTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppBlocksResultTypeDef = TypedDict(
    "DescribeAppBlocksResultTypeDef",
    {
        "AppBlocks": List[AppBlockTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
