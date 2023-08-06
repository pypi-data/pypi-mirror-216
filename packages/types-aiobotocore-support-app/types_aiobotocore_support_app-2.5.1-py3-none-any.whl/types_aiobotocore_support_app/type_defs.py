"""
Type annotations for support-app service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/type_defs/)

Usage::

    ```python
    from types_aiobotocore_support_app.type_defs import CreateSlackChannelConfigurationRequestRequestTypeDef

    data: CreateSlackChannelConfigurationRequestRequestTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List

from .literals import AccountTypeType, NotificationSeverityLevelType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CreateSlackChannelConfigurationRequestRequestTypeDef",
    "DeleteSlackChannelConfigurationRequestRequestTypeDef",
    "DeleteSlackWorkspaceConfigurationRequestRequestTypeDef",
    "GetAccountAliasResultTypeDef",
    "ListSlackChannelConfigurationsRequestRequestTypeDef",
    "SlackChannelConfigurationTypeDef",
    "ListSlackWorkspaceConfigurationsRequestRequestTypeDef",
    "SlackWorkspaceConfigurationTypeDef",
    "PutAccountAliasRequestRequestTypeDef",
    "RegisterSlackWorkspaceForOrganizationRequestRequestTypeDef",
    "RegisterSlackWorkspaceForOrganizationResultTypeDef",
    "ResponseMetadataTypeDef",
    "UpdateSlackChannelConfigurationRequestRequestTypeDef",
    "UpdateSlackChannelConfigurationResultTypeDef",
    "ListSlackChannelConfigurationsResultTypeDef",
    "ListSlackWorkspaceConfigurationsResultTypeDef",
)

_RequiredCreateSlackChannelConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSlackChannelConfigurationRequestRequestTypeDef",
    {
        "channelId": str,
        "channelRoleArn": str,
        "notifyOnCaseSeverity": NotificationSeverityLevelType,
        "teamId": str,
    },
)
_OptionalCreateSlackChannelConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSlackChannelConfigurationRequestRequestTypeDef",
    {
        "channelName": str,
        "notifyOnAddCorrespondenceToCase": bool,
        "notifyOnCreateOrReopenCase": bool,
        "notifyOnResolveCase": bool,
    },
    total=False,
)


class CreateSlackChannelConfigurationRequestRequestTypeDef(
    _RequiredCreateSlackChannelConfigurationRequestRequestTypeDef,
    _OptionalCreateSlackChannelConfigurationRequestRequestTypeDef,
):
    pass


DeleteSlackChannelConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteSlackChannelConfigurationRequestRequestTypeDef",
    {
        "channelId": str,
        "teamId": str,
    },
)

DeleteSlackWorkspaceConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteSlackWorkspaceConfigurationRequestRequestTypeDef",
    {
        "teamId": str,
    },
)

GetAccountAliasResultTypeDef = TypedDict(
    "GetAccountAliasResultTypeDef",
    {
        "accountAlias": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSlackChannelConfigurationsRequestRequestTypeDef = TypedDict(
    "ListSlackChannelConfigurationsRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

_RequiredSlackChannelConfigurationTypeDef = TypedDict(
    "_RequiredSlackChannelConfigurationTypeDef",
    {
        "channelId": str,
        "teamId": str,
    },
)
_OptionalSlackChannelConfigurationTypeDef = TypedDict(
    "_OptionalSlackChannelConfigurationTypeDef",
    {
        "channelName": str,
        "channelRoleArn": str,
        "notifyOnAddCorrespondenceToCase": bool,
        "notifyOnCaseSeverity": NotificationSeverityLevelType,
        "notifyOnCreateOrReopenCase": bool,
        "notifyOnResolveCase": bool,
    },
    total=False,
)


class SlackChannelConfigurationTypeDef(
    _RequiredSlackChannelConfigurationTypeDef, _OptionalSlackChannelConfigurationTypeDef
):
    pass


ListSlackWorkspaceConfigurationsRequestRequestTypeDef = TypedDict(
    "ListSlackWorkspaceConfigurationsRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

_RequiredSlackWorkspaceConfigurationTypeDef = TypedDict(
    "_RequiredSlackWorkspaceConfigurationTypeDef",
    {
        "teamId": str,
    },
)
_OptionalSlackWorkspaceConfigurationTypeDef = TypedDict(
    "_OptionalSlackWorkspaceConfigurationTypeDef",
    {
        "allowOrganizationMemberAccount": bool,
        "teamName": str,
    },
    total=False,
)


class SlackWorkspaceConfigurationTypeDef(
    _RequiredSlackWorkspaceConfigurationTypeDef, _OptionalSlackWorkspaceConfigurationTypeDef
):
    pass


PutAccountAliasRequestRequestTypeDef = TypedDict(
    "PutAccountAliasRequestRequestTypeDef",
    {
        "accountAlias": str,
    },
)

RegisterSlackWorkspaceForOrganizationRequestRequestTypeDef = TypedDict(
    "RegisterSlackWorkspaceForOrganizationRequestRequestTypeDef",
    {
        "teamId": str,
    },
)

RegisterSlackWorkspaceForOrganizationResultTypeDef = TypedDict(
    "RegisterSlackWorkspaceForOrganizationResultTypeDef",
    {
        "accountType": AccountTypeType,
        "teamId": str,
        "teamName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
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

_RequiredUpdateSlackChannelConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSlackChannelConfigurationRequestRequestTypeDef",
    {
        "channelId": str,
        "teamId": str,
    },
)
_OptionalUpdateSlackChannelConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSlackChannelConfigurationRequestRequestTypeDef",
    {
        "channelName": str,
        "channelRoleArn": str,
        "notifyOnAddCorrespondenceToCase": bool,
        "notifyOnCaseSeverity": NotificationSeverityLevelType,
        "notifyOnCreateOrReopenCase": bool,
        "notifyOnResolveCase": bool,
    },
    total=False,
)


class UpdateSlackChannelConfigurationRequestRequestTypeDef(
    _RequiredUpdateSlackChannelConfigurationRequestRequestTypeDef,
    _OptionalUpdateSlackChannelConfigurationRequestRequestTypeDef,
):
    pass


UpdateSlackChannelConfigurationResultTypeDef = TypedDict(
    "UpdateSlackChannelConfigurationResultTypeDef",
    {
        "channelId": str,
        "channelName": str,
        "channelRoleArn": str,
        "notifyOnAddCorrespondenceToCase": bool,
        "notifyOnCaseSeverity": NotificationSeverityLevelType,
        "notifyOnCreateOrReopenCase": bool,
        "notifyOnResolveCase": bool,
        "teamId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSlackChannelConfigurationsResultTypeDef = TypedDict(
    "ListSlackChannelConfigurationsResultTypeDef",
    {
        "nextToken": str,
        "slackChannelConfigurations": List[SlackChannelConfigurationTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSlackWorkspaceConfigurationsResultTypeDef = TypedDict(
    "ListSlackWorkspaceConfigurationsResultTypeDef",
    {
        "nextToken": str,
        "slackWorkspaceConfigurations": List[SlackWorkspaceConfigurationTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
