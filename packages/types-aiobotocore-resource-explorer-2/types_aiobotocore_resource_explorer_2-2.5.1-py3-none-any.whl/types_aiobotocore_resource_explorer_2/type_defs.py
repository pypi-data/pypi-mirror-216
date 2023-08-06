"""
Type annotations for resource-explorer-2 service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_explorer_2/type_defs/)

Usage::

    ```python
    from types_aiobotocore_resource_explorer_2.type_defs import AssociateDefaultViewInputRequestTypeDef

    data: AssociateDefaultViewInputRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence

from .literals import IndexStateType, IndexTypeType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AssociateDefaultViewInputRequestTypeDef",
    "AssociateDefaultViewOutputTypeDef",
    "BatchGetViewErrorTypeDef",
    "BatchGetViewInputRequestTypeDef",
    "CreateIndexInputRequestTypeDef",
    "CreateIndexOutputTypeDef",
    "IncludedPropertyTypeDef",
    "SearchFilterTypeDef",
    "DeleteIndexInputRequestTypeDef",
    "DeleteIndexOutputTypeDef",
    "DeleteViewInputRequestTypeDef",
    "DeleteViewOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetDefaultViewOutputTypeDef",
    "GetIndexOutputTypeDef",
    "GetViewInputRequestTypeDef",
    "IndexTypeDef",
    "ListIndexesInputListIndexesPaginateTypeDef",
    "ListIndexesInputRequestTypeDef",
    "ListSupportedResourceTypesInputListSupportedResourceTypesPaginateTypeDef",
    "ListSupportedResourceTypesInputRequestTypeDef",
    "SupportedResourceTypeTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListViewsInputListViewsPaginateTypeDef",
    "ListViewsInputRequestTypeDef",
    "ListViewsOutputTypeDef",
    "PaginatorConfigTypeDef",
    "ResourceCountTypeDef",
    "ResourcePropertyTypeDef",
    "ResponseMetadataTypeDef",
    "SearchInputRequestTypeDef",
    "SearchInputSearchPaginateTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateIndexTypeInputRequestTypeDef",
    "UpdateIndexTypeOutputTypeDef",
    "CreateViewInputRequestTypeDef",
    "UpdateViewInputRequestTypeDef",
    "ViewTypeDef",
    "ListIndexesOutputTypeDef",
    "ListSupportedResourceTypesOutputTypeDef",
    "ResourceTypeDef",
    "BatchGetViewOutputTypeDef",
    "CreateViewOutputTypeDef",
    "GetViewOutputTypeDef",
    "UpdateViewOutputTypeDef",
    "SearchOutputTypeDef",
)

AssociateDefaultViewInputRequestTypeDef = TypedDict(
    "AssociateDefaultViewInputRequestTypeDef",
    {
        "ViewArn": str,
    },
)

AssociateDefaultViewOutputTypeDef = TypedDict(
    "AssociateDefaultViewOutputTypeDef",
    {
        "ViewArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchGetViewErrorTypeDef = TypedDict(
    "BatchGetViewErrorTypeDef",
    {
        "ErrorMessage": str,
        "ViewArn": str,
    },
)

BatchGetViewInputRequestTypeDef = TypedDict(
    "BatchGetViewInputRequestTypeDef",
    {
        "ViewArns": Sequence[str],
    },
    total=False,
)

CreateIndexInputRequestTypeDef = TypedDict(
    "CreateIndexInputRequestTypeDef",
    {
        "ClientToken": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)

CreateIndexOutputTypeDef = TypedDict(
    "CreateIndexOutputTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "State": IndexStateType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

IncludedPropertyTypeDef = TypedDict(
    "IncludedPropertyTypeDef",
    {
        "Name": str,
    },
)

SearchFilterTypeDef = TypedDict(
    "SearchFilterTypeDef",
    {
        "FilterString": str,
    },
)

DeleteIndexInputRequestTypeDef = TypedDict(
    "DeleteIndexInputRequestTypeDef",
    {
        "Arn": str,
    },
)

DeleteIndexOutputTypeDef = TypedDict(
    "DeleteIndexOutputTypeDef",
    {
        "Arn": str,
        "LastUpdatedAt": datetime,
        "State": IndexStateType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteViewInputRequestTypeDef = TypedDict(
    "DeleteViewInputRequestTypeDef",
    {
        "ViewArn": str,
    },
)

DeleteViewOutputTypeDef = TypedDict(
    "DeleteViewOutputTypeDef",
    {
        "ViewArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetDefaultViewOutputTypeDef = TypedDict(
    "GetDefaultViewOutputTypeDef",
    {
        "ViewArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetIndexOutputTypeDef = TypedDict(
    "GetIndexOutputTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "LastUpdatedAt": datetime,
        "ReplicatingFrom": List[str],
        "ReplicatingTo": List[str],
        "State": IndexStateType,
        "Tags": Dict[str, str],
        "Type": IndexTypeType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetViewInputRequestTypeDef = TypedDict(
    "GetViewInputRequestTypeDef",
    {
        "ViewArn": str,
    },
)

IndexTypeDef = TypedDict(
    "IndexTypeDef",
    {
        "Arn": str,
        "Region": str,
        "Type": IndexTypeType,
    },
    total=False,
)

ListIndexesInputListIndexesPaginateTypeDef = TypedDict(
    "ListIndexesInputListIndexesPaginateTypeDef",
    {
        "Regions": Sequence[str],
        "Type": IndexTypeType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListIndexesInputRequestTypeDef = TypedDict(
    "ListIndexesInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Regions": Sequence[str],
        "Type": IndexTypeType,
    },
    total=False,
)

ListSupportedResourceTypesInputListSupportedResourceTypesPaginateTypeDef = TypedDict(
    "ListSupportedResourceTypesInputListSupportedResourceTypesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListSupportedResourceTypesInputRequestTypeDef = TypedDict(
    "ListSupportedResourceTypesInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

SupportedResourceTypeTypeDef = TypedDict(
    "SupportedResourceTypeTypeDef",
    {
        "ResourceType": str,
        "Service": str,
    },
    total=False,
)

ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListViewsInputListViewsPaginateTypeDef = TypedDict(
    "ListViewsInputListViewsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListViewsInputRequestTypeDef = TypedDict(
    "ListViewsInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListViewsOutputTypeDef = TypedDict(
    "ListViewsOutputTypeDef",
    {
        "NextToken": str,
        "Views": List[str],
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

ResourceCountTypeDef = TypedDict(
    "ResourceCountTypeDef",
    {
        "Complete": bool,
        "TotalResources": int,
    },
    total=False,
)

ResourcePropertyTypeDef = TypedDict(
    "ResourcePropertyTypeDef",
    {
        "Data": Dict[str, Any],
        "LastReportedAt": datetime,
        "Name": str,
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

_RequiredSearchInputRequestTypeDef = TypedDict(
    "_RequiredSearchInputRequestTypeDef",
    {
        "QueryString": str,
    },
)
_OptionalSearchInputRequestTypeDef = TypedDict(
    "_OptionalSearchInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "ViewArn": str,
    },
    total=False,
)


class SearchInputRequestTypeDef(
    _RequiredSearchInputRequestTypeDef, _OptionalSearchInputRequestTypeDef
):
    pass


_RequiredSearchInputSearchPaginateTypeDef = TypedDict(
    "_RequiredSearchInputSearchPaginateTypeDef",
    {
        "QueryString": str,
    },
)
_OptionalSearchInputSearchPaginateTypeDef = TypedDict(
    "_OptionalSearchInputSearchPaginateTypeDef",
    {
        "ViewArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class SearchInputSearchPaginateTypeDef(
    _RequiredSearchInputSearchPaginateTypeDef, _OptionalSearchInputSearchPaginateTypeDef
):
    pass


_RequiredTagResourceInputRequestTypeDef = TypedDict(
    "_RequiredTagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalTagResourceInputRequestTypeDef = TypedDict(
    "_OptionalTagResourceInputRequestTypeDef",
    {
        "Tags": Mapping[str, str],
    },
    total=False,
)


class TagResourceInputRequestTypeDef(
    _RequiredTagResourceInputRequestTypeDef, _OptionalTagResourceInputRequestTypeDef
):
    pass


UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

UpdateIndexTypeInputRequestTypeDef = TypedDict(
    "UpdateIndexTypeInputRequestTypeDef",
    {
        "Arn": str,
        "Type": IndexTypeType,
    },
)

UpdateIndexTypeOutputTypeDef = TypedDict(
    "UpdateIndexTypeOutputTypeDef",
    {
        "Arn": str,
        "LastUpdatedAt": datetime,
        "State": IndexStateType,
        "Type": IndexTypeType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateViewInputRequestTypeDef = TypedDict(
    "_RequiredCreateViewInputRequestTypeDef",
    {
        "ViewName": str,
    },
)
_OptionalCreateViewInputRequestTypeDef = TypedDict(
    "_OptionalCreateViewInputRequestTypeDef",
    {
        "ClientToken": str,
        "Filters": SearchFilterTypeDef,
        "IncludedProperties": Sequence[IncludedPropertyTypeDef],
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateViewInputRequestTypeDef(
    _RequiredCreateViewInputRequestTypeDef, _OptionalCreateViewInputRequestTypeDef
):
    pass


_RequiredUpdateViewInputRequestTypeDef = TypedDict(
    "_RequiredUpdateViewInputRequestTypeDef",
    {
        "ViewArn": str,
    },
)
_OptionalUpdateViewInputRequestTypeDef = TypedDict(
    "_OptionalUpdateViewInputRequestTypeDef",
    {
        "Filters": SearchFilterTypeDef,
        "IncludedProperties": Sequence[IncludedPropertyTypeDef],
    },
    total=False,
)


class UpdateViewInputRequestTypeDef(
    _RequiredUpdateViewInputRequestTypeDef, _OptionalUpdateViewInputRequestTypeDef
):
    pass


ViewTypeDef = TypedDict(
    "ViewTypeDef",
    {
        "Filters": SearchFilterTypeDef,
        "IncludedProperties": List[IncludedPropertyTypeDef],
        "LastUpdatedAt": datetime,
        "Owner": str,
        "Scope": str,
        "ViewArn": str,
    },
    total=False,
)

ListIndexesOutputTypeDef = TypedDict(
    "ListIndexesOutputTypeDef",
    {
        "Indexes": List[IndexTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSupportedResourceTypesOutputTypeDef = TypedDict(
    "ListSupportedResourceTypesOutputTypeDef",
    {
        "NextToken": str,
        "ResourceTypes": List[SupportedResourceTypeTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "Arn": str,
        "LastReportedAt": datetime,
        "OwningAccountId": str,
        "Properties": List[ResourcePropertyTypeDef],
        "Region": str,
        "ResourceType": str,
        "Service": str,
    },
    total=False,
)

BatchGetViewOutputTypeDef = TypedDict(
    "BatchGetViewOutputTypeDef",
    {
        "Errors": List[BatchGetViewErrorTypeDef],
        "Views": List[ViewTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateViewOutputTypeDef = TypedDict(
    "CreateViewOutputTypeDef",
    {
        "View": ViewTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetViewOutputTypeDef = TypedDict(
    "GetViewOutputTypeDef",
    {
        "Tags": Dict[str, str],
        "View": ViewTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateViewOutputTypeDef = TypedDict(
    "UpdateViewOutputTypeDef",
    {
        "View": ViewTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SearchOutputTypeDef = TypedDict(
    "SearchOutputTypeDef",
    {
        "Count": ResourceCountTypeDef,
        "NextToken": str,
        "Resources": List[ResourceTypeDef],
        "ViewArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
