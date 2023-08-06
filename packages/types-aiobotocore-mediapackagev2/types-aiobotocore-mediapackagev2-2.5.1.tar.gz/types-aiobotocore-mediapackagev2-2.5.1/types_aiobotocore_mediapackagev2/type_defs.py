"""
Type annotations for mediapackagev2 service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackagev2/type_defs/)

Usage::

    ```python
    from types_aiobotocore_mediapackagev2.type_defs import ChannelGroupListConfigurationTypeDef

    data: ChannelGroupListConfigurationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    CmafEncryptionMethodType,
    ContainerTypeType,
    DrmSystemType,
    PresetSpeke20AudioType,
    PresetSpeke20VideoType,
    ScteFilterType,
    TsEncryptionMethodType,
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
    "ChannelGroupListConfigurationTypeDef",
    "ChannelListConfigurationTypeDef",
    "CreateChannelGroupRequestRequestTypeDef",
    "CreateChannelGroupResponseTypeDef",
    "CreateChannelRequestRequestTypeDef",
    "IngestEndpointTypeDef",
    "ScteHlsTypeDef",
    "DeleteChannelGroupRequestRequestTypeDef",
    "DeleteChannelPolicyRequestRequestTypeDef",
    "DeleteChannelRequestRequestTypeDef",
    "DeleteOriginEndpointPolicyRequestRequestTypeDef",
    "DeleteOriginEndpointRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionContractConfigurationTypeDef",
    "EncryptionMethodTypeDef",
    "GetChannelGroupRequestRequestTypeDef",
    "GetChannelGroupResponseTypeDef",
    "GetChannelPolicyRequestRequestTypeDef",
    "GetChannelPolicyResponseTypeDef",
    "GetChannelRequestRequestTypeDef",
    "GetOriginEndpointPolicyRequestRequestTypeDef",
    "GetOriginEndpointPolicyResponseTypeDef",
    "GetOriginEndpointRequestRequestTypeDef",
    "ListChannelGroupsRequestListChannelGroupsPaginateTypeDef",
    "ListChannelGroupsRequestRequestTypeDef",
    "ListChannelsRequestListChannelsPaginateTypeDef",
    "ListChannelsRequestRequestTypeDef",
    "ListHlsManifestConfigurationTypeDef",
    "ListLowLatencyHlsManifestConfigurationTypeDef",
    "ListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef",
    "ListOriginEndpointsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutChannelPolicyRequestRequestTypeDef",
    "PutOriginEndpointPolicyRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ScteTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateChannelGroupRequestRequestTypeDef",
    "UpdateChannelGroupResponseTypeDef",
    "UpdateChannelRequestRequestTypeDef",
    "ListChannelGroupsResponseTypeDef",
    "ListChannelsResponseTypeDef",
    "CreateChannelResponseTypeDef",
    "GetChannelResponseTypeDef",
    "UpdateChannelResponseTypeDef",
    "CreateHlsManifestConfigurationTypeDef",
    "CreateLowLatencyHlsManifestConfigurationTypeDef",
    "GetHlsManifestConfigurationTypeDef",
    "GetLowLatencyHlsManifestConfigurationTypeDef",
    "SpekeKeyProviderTypeDef",
    "OriginEndpointListConfigurationTypeDef",
    "EncryptionTypeDef",
    "ListOriginEndpointsResponseTypeDef",
    "SegmentTypeDef",
    "CreateOriginEndpointRequestRequestTypeDef",
    "CreateOriginEndpointResponseTypeDef",
    "GetOriginEndpointResponseTypeDef",
    "UpdateOriginEndpointRequestRequestTypeDef",
    "UpdateOriginEndpointResponseTypeDef",
)

_RequiredChannelGroupListConfigurationTypeDef = TypedDict(
    "_RequiredChannelGroupListConfigurationTypeDef",
    {
        "ChannelGroupName": str,
        "Arn": str,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
    },
)
_OptionalChannelGroupListConfigurationTypeDef = TypedDict(
    "_OptionalChannelGroupListConfigurationTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class ChannelGroupListConfigurationTypeDef(
    _RequiredChannelGroupListConfigurationTypeDef, _OptionalChannelGroupListConfigurationTypeDef
):
    pass


_RequiredChannelListConfigurationTypeDef = TypedDict(
    "_RequiredChannelListConfigurationTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ChannelGroupName": str,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
    },
)
_OptionalChannelListConfigurationTypeDef = TypedDict(
    "_OptionalChannelListConfigurationTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class ChannelListConfigurationTypeDef(
    _RequiredChannelListConfigurationTypeDef, _OptionalChannelListConfigurationTypeDef
):
    pass


_RequiredCreateChannelGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateChannelGroupRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
    },
)
_OptionalCreateChannelGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateChannelGroupRequestRequestTypeDef",
    {
        "ClientToken": str,
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateChannelGroupRequestRequestTypeDef(
    _RequiredCreateChannelGroupRequestRequestTypeDef,
    _OptionalCreateChannelGroupRequestRequestTypeDef,
):
    pass


CreateChannelGroupResponseTypeDef = TypedDict(
    "CreateChannelGroupResponseTypeDef",
    {
        "ChannelGroupName": str,
        "Arn": str,
        "EgressDomain": str,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateChannelRequestRequestTypeDef = TypedDict(
    "_RequiredCreateChannelRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
    },
)
_OptionalCreateChannelRequestRequestTypeDef = TypedDict(
    "_OptionalCreateChannelRequestRequestTypeDef",
    {
        "ClientToken": str,
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateChannelRequestRequestTypeDef(
    _RequiredCreateChannelRequestRequestTypeDef, _OptionalCreateChannelRequestRequestTypeDef
):
    pass


IngestEndpointTypeDef = TypedDict(
    "IngestEndpointTypeDef",
    {
        "Id": str,
        "Url": str,
    },
    total=False,
)

ScteHlsTypeDef = TypedDict(
    "ScteHlsTypeDef",
    {
        "AdMarkerHls": Literal["DATERANGE"],
    },
    total=False,
)

DeleteChannelGroupRequestRequestTypeDef = TypedDict(
    "DeleteChannelGroupRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
    },
)

DeleteChannelPolicyRequestRequestTypeDef = TypedDict(
    "DeleteChannelPolicyRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
    },
)

DeleteChannelRequestRequestTypeDef = TypedDict(
    "DeleteChannelRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
    },
)

DeleteOriginEndpointPolicyRequestRequestTypeDef = TypedDict(
    "DeleteOriginEndpointPolicyRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
    },
)

DeleteOriginEndpointRequestRequestTypeDef = TypedDict(
    "DeleteOriginEndpointRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EncryptionContractConfigurationTypeDef = TypedDict(
    "EncryptionContractConfigurationTypeDef",
    {
        "PresetSpeke20Audio": PresetSpeke20AudioType,
        "PresetSpeke20Video": PresetSpeke20VideoType,
    },
)

EncryptionMethodTypeDef = TypedDict(
    "EncryptionMethodTypeDef",
    {
        "TsEncryptionMethod": TsEncryptionMethodType,
        "CmafEncryptionMethod": CmafEncryptionMethodType,
    },
    total=False,
)

GetChannelGroupRequestRequestTypeDef = TypedDict(
    "GetChannelGroupRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
    },
)

GetChannelGroupResponseTypeDef = TypedDict(
    "GetChannelGroupResponseTypeDef",
    {
        "ChannelGroupName": str,
        "Arn": str,
        "EgressDomain": str,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetChannelPolicyRequestRequestTypeDef = TypedDict(
    "GetChannelPolicyRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
    },
)

GetChannelPolicyResponseTypeDef = TypedDict(
    "GetChannelPolicyResponseTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "Policy": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetChannelRequestRequestTypeDef = TypedDict(
    "GetChannelRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
    },
)

GetOriginEndpointPolicyRequestRequestTypeDef = TypedDict(
    "GetOriginEndpointPolicyRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
    },
)

GetOriginEndpointPolicyResponseTypeDef = TypedDict(
    "GetOriginEndpointPolicyResponseTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
        "Policy": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetOriginEndpointRequestRequestTypeDef = TypedDict(
    "GetOriginEndpointRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
    },
)

ListChannelGroupsRequestListChannelGroupsPaginateTypeDef = TypedDict(
    "ListChannelGroupsRequestListChannelGroupsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListChannelGroupsRequestRequestTypeDef = TypedDict(
    "ListChannelGroupsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListChannelsRequestListChannelsPaginateTypeDef = TypedDict(
    "_RequiredListChannelsRequestListChannelsPaginateTypeDef",
    {
        "ChannelGroupName": str,
    },
)
_OptionalListChannelsRequestListChannelsPaginateTypeDef = TypedDict(
    "_OptionalListChannelsRequestListChannelsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListChannelsRequestListChannelsPaginateTypeDef(
    _RequiredListChannelsRequestListChannelsPaginateTypeDef,
    _OptionalListChannelsRequestListChannelsPaginateTypeDef,
):
    pass


_RequiredListChannelsRequestRequestTypeDef = TypedDict(
    "_RequiredListChannelsRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
    },
)
_OptionalListChannelsRequestRequestTypeDef = TypedDict(
    "_OptionalListChannelsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListChannelsRequestRequestTypeDef(
    _RequiredListChannelsRequestRequestTypeDef, _OptionalListChannelsRequestRequestTypeDef
):
    pass


_RequiredListHlsManifestConfigurationTypeDef = TypedDict(
    "_RequiredListHlsManifestConfigurationTypeDef",
    {
        "ManifestName": str,
    },
)
_OptionalListHlsManifestConfigurationTypeDef = TypedDict(
    "_OptionalListHlsManifestConfigurationTypeDef",
    {
        "ChildManifestName": str,
        "Url": str,
    },
    total=False,
)


class ListHlsManifestConfigurationTypeDef(
    _RequiredListHlsManifestConfigurationTypeDef, _OptionalListHlsManifestConfigurationTypeDef
):
    pass


_RequiredListLowLatencyHlsManifestConfigurationTypeDef = TypedDict(
    "_RequiredListLowLatencyHlsManifestConfigurationTypeDef",
    {
        "ManifestName": str,
    },
)
_OptionalListLowLatencyHlsManifestConfigurationTypeDef = TypedDict(
    "_OptionalListLowLatencyHlsManifestConfigurationTypeDef",
    {
        "ChildManifestName": str,
        "Url": str,
    },
    total=False,
)


class ListLowLatencyHlsManifestConfigurationTypeDef(
    _RequiredListLowLatencyHlsManifestConfigurationTypeDef,
    _OptionalListLowLatencyHlsManifestConfigurationTypeDef,
):
    pass


_RequiredListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef = TypedDict(
    "_RequiredListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
    },
)
_OptionalListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef = TypedDict(
    "_OptionalListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef(
    _RequiredListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef,
    _OptionalListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef,
):
    pass


_RequiredListOriginEndpointsRequestRequestTypeDef = TypedDict(
    "_RequiredListOriginEndpointsRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
    },
)
_OptionalListOriginEndpointsRequestRequestTypeDef = TypedDict(
    "_OptionalListOriginEndpointsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListOriginEndpointsRequestRequestTypeDef(
    _RequiredListOriginEndpointsRequestRequestTypeDef,
    _OptionalListOriginEndpointsRequestRequestTypeDef,
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
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

PutChannelPolicyRequestRequestTypeDef = TypedDict(
    "PutChannelPolicyRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "Policy": str,
    },
)

PutOriginEndpointPolicyRequestRequestTypeDef = TypedDict(
    "PutOriginEndpointPolicyRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
        "Policy": str,
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

ScteTypeDef = TypedDict(
    "ScteTypeDef",
    {
        "ScteFilter": Sequence[ScteFilterType],
    },
    total=False,
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

_RequiredUpdateChannelGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateChannelGroupRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
    },
)
_OptionalUpdateChannelGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateChannelGroupRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class UpdateChannelGroupRequestRequestTypeDef(
    _RequiredUpdateChannelGroupRequestRequestTypeDef,
    _OptionalUpdateChannelGroupRequestRequestTypeDef,
):
    pass


UpdateChannelGroupResponseTypeDef = TypedDict(
    "UpdateChannelGroupResponseTypeDef",
    {
        "ChannelGroupName": str,
        "Arn": str,
        "EgressDomain": str,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateChannelRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateChannelRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
    },
)
_OptionalUpdateChannelRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateChannelRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class UpdateChannelRequestRequestTypeDef(
    _RequiredUpdateChannelRequestRequestTypeDef, _OptionalUpdateChannelRequestRequestTypeDef
):
    pass


ListChannelGroupsResponseTypeDef = TypedDict(
    "ListChannelGroupsResponseTypeDef",
    {
        "Items": List[ChannelGroupListConfigurationTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListChannelsResponseTypeDef = TypedDict(
    "ListChannelsResponseTypeDef",
    {
        "Items": List[ChannelListConfigurationTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateChannelResponseTypeDef = TypedDict(
    "CreateChannelResponseTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ChannelGroupName": str,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": str,
        "IngestEndpoints": List[IngestEndpointTypeDef],
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetChannelResponseTypeDef = TypedDict(
    "GetChannelResponseTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ChannelGroupName": str,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": str,
        "IngestEndpoints": List[IngestEndpointTypeDef],
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateChannelResponseTypeDef = TypedDict(
    "UpdateChannelResponseTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ChannelGroupName": str,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": str,
        "IngestEndpoints": List[IngestEndpointTypeDef],
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateHlsManifestConfigurationTypeDef = TypedDict(
    "_RequiredCreateHlsManifestConfigurationTypeDef",
    {
        "ManifestName": str,
    },
)
_OptionalCreateHlsManifestConfigurationTypeDef = TypedDict(
    "_OptionalCreateHlsManifestConfigurationTypeDef",
    {
        "ChildManifestName": str,
        "ScteHls": ScteHlsTypeDef,
        "ManifestWindowSeconds": int,
        "ProgramDateTimeIntervalSeconds": int,
    },
    total=False,
)


class CreateHlsManifestConfigurationTypeDef(
    _RequiredCreateHlsManifestConfigurationTypeDef, _OptionalCreateHlsManifestConfigurationTypeDef
):
    pass


_RequiredCreateLowLatencyHlsManifestConfigurationTypeDef = TypedDict(
    "_RequiredCreateLowLatencyHlsManifestConfigurationTypeDef",
    {
        "ManifestName": str,
    },
)
_OptionalCreateLowLatencyHlsManifestConfigurationTypeDef = TypedDict(
    "_OptionalCreateLowLatencyHlsManifestConfigurationTypeDef",
    {
        "ChildManifestName": str,
        "ScteHls": ScteHlsTypeDef,
        "ManifestWindowSeconds": int,
        "ProgramDateTimeIntervalSeconds": int,
    },
    total=False,
)


class CreateLowLatencyHlsManifestConfigurationTypeDef(
    _RequiredCreateLowLatencyHlsManifestConfigurationTypeDef,
    _OptionalCreateLowLatencyHlsManifestConfigurationTypeDef,
):
    pass


_RequiredGetHlsManifestConfigurationTypeDef = TypedDict(
    "_RequiredGetHlsManifestConfigurationTypeDef",
    {
        "ManifestName": str,
        "Url": str,
    },
)
_OptionalGetHlsManifestConfigurationTypeDef = TypedDict(
    "_OptionalGetHlsManifestConfigurationTypeDef",
    {
        "ChildManifestName": str,
        "ManifestWindowSeconds": int,
        "ProgramDateTimeIntervalSeconds": int,
        "ScteHls": ScteHlsTypeDef,
    },
    total=False,
)


class GetHlsManifestConfigurationTypeDef(
    _RequiredGetHlsManifestConfigurationTypeDef, _OptionalGetHlsManifestConfigurationTypeDef
):
    pass


_RequiredGetLowLatencyHlsManifestConfigurationTypeDef = TypedDict(
    "_RequiredGetLowLatencyHlsManifestConfigurationTypeDef",
    {
        "ManifestName": str,
        "Url": str,
    },
)
_OptionalGetLowLatencyHlsManifestConfigurationTypeDef = TypedDict(
    "_OptionalGetLowLatencyHlsManifestConfigurationTypeDef",
    {
        "ChildManifestName": str,
        "ManifestWindowSeconds": int,
        "ProgramDateTimeIntervalSeconds": int,
        "ScteHls": ScteHlsTypeDef,
    },
    total=False,
)


class GetLowLatencyHlsManifestConfigurationTypeDef(
    _RequiredGetLowLatencyHlsManifestConfigurationTypeDef,
    _OptionalGetLowLatencyHlsManifestConfigurationTypeDef,
):
    pass


SpekeKeyProviderTypeDef = TypedDict(
    "SpekeKeyProviderTypeDef",
    {
        "EncryptionContractConfiguration": EncryptionContractConfigurationTypeDef,
        "ResourceId": str,
        "DrmSystems": Sequence[DrmSystemType],
        "RoleArn": str,
        "Url": str,
    },
)

_RequiredOriginEndpointListConfigurationTypeDef = TypedDict(
    "_RequiredOriginEndpointListConfigurationTypeDef",
    {
        "Arn": str,
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
        "ContainerType": ContainerTypeType,
    },
)
_OptionalOriginEndpointListConfigurationTypeDef = TypedDict(
    "_OptionalOriginEndpointListConfigurationTypeDef",
    {
        "Description": str,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "HlsManifests": List[ListHlsManifestConfigurationTypeDef],
        "LowLatencyHlsManifests": List[ListLowLatencyHlsManifestConfigurationTypeDef],
    },
    total=False,
)


class OriginEndpointListConfigurationTypeDef(
    _RequiredOriginEndpointListConfigurationTypeDef, _OptionalOriginEndpointListConfigurationTypeDef
):
    pass


_RequiredEncryptionTypeDef = TypedDict(
    "_RequiredEncryptionTypeDef",
    {
        "EncryptionMethod": EncryptionMethodTypeDef,
        "SpekeKeyProvider": SpekeKeyProviderTypeDef,
    },
)
_OptionalEncryptionTypeDef = TypedDict(
    "_OptionalEncryptionTypeDef",
    {
        "ConstantInitializationVector": str,
        "KeyRotationIntervalSeconds": int,
    },
    total=False,
)


class EncryptionTypeDef(_RequiredEncryptionTypeDef, _OptionalEncryptionTypeDef):
    pass


ListOriginEndpointsResponseTypeDef = TypedDict(
    "ListOriginEndpointsResponseTypeDef",
    {
        "Items": List[OriginEndpointListConfigurationTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SegmentTypeDef = TypedDict(
    "SegmentTypeDef",
    {
        "SegmentDurationSeconds": int,
        "SegmentName": str,
        "TsUseAudioRenditionGroup": bool,
        "IncludeIframeOnlyStreams": bool,
        "TsIncludeDvbSubtitles": bool,
        "Scte": ScteTypeDef,
        "Encryption": EncryptionTypeDef,
    },
    total=False,
)

_RequiredCreateOriginEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredCreateOriginEndpointRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
        "ContainerType": ContainerTypeType,
    },
)
_OptionalCreateOriginEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalCreateOriginEndpointRequestRequestTypeDef",
    {
        "Segment": SegmentTypeDef,
        "ClientToken": str,
        "Description": str,
        "StartoverWindowSeconds": int,
        "HlsManifests": Sequence[CreateHlsManifestConfigurationTypeDef],
        "LowLatencyHlsManifests": Sequence[CreateLowLatencyHlsManifestConfigurationTypeDef],
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateOriginEndpointRequestRequestTypeDef(
    _RequiredCreateOriginEndpointRequestRequestTypeDef,
    _OptionalCreateOriginEndpointRequestRequestTypeDef,
):
    pass


CreateOriginEndpointResponseTypeDef = TypedDict(
    "CreateOriginEndpointResponseTypeDef",
    {
        "Arn": str,
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
        "ContainerType": ContainerTypeType,
        "Segment": SegmentTypeDef,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": str,
        "StartoverWindowSeconds": int,
        "HlsManifests": List[GetHlsManifestConfigurationTypeDef],
        "LowLatencyHlsManifests": List[GetLowLatencyHlsManifestConfigurationTypeDef],
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetOriginEndpointResponseTypeDef = TypedDict(
    "GetOriginEndpointResponseTypeDef",
    {
        "Arn": str,
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
        "ContainerType": ContainerTypeType,
        "Segment": SegmentTypeDef,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": str,
        "StartoverWindowSeconds": int,
        "HlsManifests": List[GetHlsManifestConfigurationTypeDef],
        "LowLatencyHlsManifests": List[GetLowLatencyHlsManifestConfigurationTypeDef],
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateOriginEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateOriginEndpointRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
        "ContainerType": ContainerTypeType,
    },
)
_OptionalUpdateOriginEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateOriginEndpointRequestRequestTypeDef",
    {
        "Segment": SegmentTypeDef,
        "Description": str,
        "StartoverWindowSeconds": int,
        "HlsManifests": Sequence[CreateHlsManifestConfigurationTypeDef],
        "LowLatencyHlsManifests": Sequence[CreateLowLatencyHlsManifestConfigurationTypeDef],
    },
    total=False,
)


class UpdateOriginEndpointRequestRequestTypeDef(
    _RequiredUpdateOriginEndpointRequestRequestTypeDef,
    _OptionalUpdateOriginEndpointRequestRequestTypeDef,
):
    pass


UpdateOriginEndpointResponseTypeDef = TypedDict(
    "UpdateOriginEndpointResponseTypeDef",
    {
        "Arn": str,
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
        "ContainerType": ContainerTypeType,
        "Segment": SegmentTypeDef,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": str,
        "StartoverWindowSeconds": int,
        "HlsManifests": List[GetHlsManifestConfigurationTypeDef],
        "LowLatencyHlsManifests": List[GetLowLatencyHlsManifestConfigurationTypeDef],
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
