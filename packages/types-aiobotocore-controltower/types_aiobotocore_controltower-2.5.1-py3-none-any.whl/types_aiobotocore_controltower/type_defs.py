"""
Type annotations for controltower service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/type_defs/)

Usage::

    ```python
    from types_aiobotocore_controltower.type_defs import ControlOperationTypeDef

    data: ControlOperationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List

from .literals import ControlOperationStatusType, ControlOperationTypeType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ControlOperationTypeDef",
    "DisableControlInputRequestTypeDef",
    "DisableControlOutputTypeDef",
    "EnableControlInputRequestTypeDef",
    "EnableControlOutputTypeDef",
    "EnabledControlSummaryTypeDef",
    "GetControlOperationInputRequestTypeDef",
    "ListEnabledControlsInputListEnabledControlsPaginateTypeDef",
    "ListEnabledControlsInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "GetControlOperationOutputTypeDef",
    "ListEnabledControlsOutputTypeDef",
)

ControlOperationTypeDef = TypedDict(
    "ControlOperationTypeDef",
    {
        "endTime": datetime,
        "operationType": ControlOperationTypeType,
        "startTime": datetime,
        "status": ControlOperationStatusType,
        "statusMessage": str,
    },
    total=False,
)

DisableControlInputRequestTypeDef = TypedDict(
    "DisableControlInputRequestTypeDef",
    {
        "controlIdentifier": str,
        "targetIdentifier": str,
    },
)

DisableControlOutputTypeDef = TypedDict(
    "DisableControlOutputTypeDef",
    {
        "operationIdentifier": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EnableControlInputRequestTypeDef = TypedDict(
    "EnableControlInputRequestTypeDef",
    {
        "controlIdentifier": str,
        "targetIdentifier": str,
    },
)

EnableControlOutputTypeDef = TypedDict(
    "EnableControlOutputTypeDef",
    {
        "operationIdentifier": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EnabledControlSummaryTypeDef = TypedDict(
    "EnabledControlSummaryTypeDef",
    {
        "controlIdentifier": str,
    },
    total=False,
)

GetControlOperationInputRequestTypeDef = TypedDict(
    "GetControlOperationInputRequestTypeDef",
    {
        "operationIdentifier": str,
    },
)

_RequiredListEnabledControlsInputListEnabledControlsPaginateTypeDef = TypedDict(
    "_RequiredListEnabledControlsInputListEnabledControlsPaginateTypeDef",
    {
        "targetIdentifier": str,
    },
)
_OptionalListEnabledControlsInputListEnabledControlsPaginateTypeDef = TypedDict(
    "_OptionalListEnabledControlsInputListEnabledControlsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListEnabledControlsInputListEnabledControlsPaginateTypeDef(
    _RequiredListEnabledControlsInputListEnabledControlsPaginateTypeDef,
    _OptionalListEnabledControlsInputListEnabledControlsPaginateTypeDef,
):
    pass


_RequiredListEnabledControlsInputRequestTypeDef = TypedDict(
    "_RequiredListEnabledControlsInputRequestTypeDef",
    {
        "targetIdentifier": str,
    },
)
_OptionalListEnabledControlsInputRequestTypeDef = TypedDict(
    "_OptionalListEnabledControlsInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListEnabledControlsInputRequestTypeDef(
    _RequiredListEnabledControlsInputRequestTypeDef, _OptionalListEnabledControlsInputRequestTypeDef
):
    pass


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

GetControlOperationOutputTypeDef = TypedDict(
    "GetControlOperationOutputTypeDef",
    {
        "controlOperation": ControlOperationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEnabledControlsOutputTypeDef = TypedDict(
    "ListEnabledControlsOutputTypeDef",
    {
        "enabledControls": List[EnabledControlSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
