"""
Type annotations for arc-zonal-shift service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/type_defs/)

Usage::

    ```python
    from types_aiobotocore_arc_zonal_shift.type_defs import CancelZonalShiftRequestRequestTypeDef

    data: CancelZonalShiftRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List

from .literals import AppliedStatusType, ZonalShiftStatusType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "CancelZonalShiftRequestRequestTypeDef",
    "GetManagedResourceRequestRequestTypeDef",
    "ZonalShiftInResourceTypeDef",
    "ListManagedResourcesRequestListManagedResourcesPaginateTypeDef",
    "ListManagedResourcesRequestRequestTypeDef",
    "ManagedResourceSummaryTypeDef",
    "ListZonalShiftsRequestListZonalShiftsPaginateTypeDef",
    "ListZonalShiftsRequestRequestTypeDef",
    "ZonalShiftSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "StartZonalShiftRequestRequestTypeDef",
    "UpdateZonalShiftRequestRequestTypeDef",
    "ZonalShiftTypeDef",
    "GetManagedResourceResponseTypeDef",
    "ListManagedResourcesResponseTypeDef",
    "ListZonalShiftsResponseTypeDef",
)

CancelZonalShiftRequestRequestTypeDef = TypedDict(
    "CancelZonalShiftRequestRequestTypeDef",
    {
        "zonalShiftId": str,
    },
)

GetManagedResourceRequestRequestTypeDef = TypedDict(
    "GetManagedResourceRequestRequestTypeDef",
    {
        "resourceIdentifier": str,
    },
)

ZonalShiftInResourceTypeDef = TypedDict(
    "ZonalShiftInResourceTypeDef",
    {
        "appliedStatus": AppliedStatusType,
        "awayFrom": str,
        "comment": str,
        "expiryTime": datetime,
        "resourceIdentifier": str,
        "startTime": datetime,
        "zonalShiftId": str,
    },
)

ListManagedResourcesRequestListManagedResourcesPaginateTypeDef = TypedDict(
    "ListManagedResourcesRequestListManagedResourcesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListManagedResourcesRequestRequestTypeDef = TypedDict(
    "ListManagedResourcesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredManagedResourceSummaryTypeDef = TypedDict(
    "_RequiredManagedResourceSummaryTypeDef",
    {
        "availabilityZones": List[str],
    },
)
_OptionalManagedResourceSummaryTypeDef = TypedDict(
    "_OptionalManagedResourceSummaryTypeDef",
    {
        "arn": str,
        "name": str,
    },
    total=False,
)

class ManagedResourceSummaryTypeDef(
    _RequiredManagedResourceSummaryTypeDef, _OptionalManagedResourceSummaryTypeDef
):
    pass

ListZonalShiftsRequestListZonalShiftsPaginateTypeDef = TypedDict(
    "ListZonalShiftsRequestListZonalShiftsPaginateTypeDef",
    {
        "status": ZonalShiftStatusType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListZonalShiftsRequestRequestTypeDef = TypedDict(
    "ListZonalShiftsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "status": ZonalShiftStatusType,
    },
    total=False,
)

ZonalShiftSummaryTypeDef = TypedDict(
    "ZonalShiftSummaryTypeDef",
    {
        "awayFrom": str,
        "comment": str,
        "expiryTime": datetime,
        "resourceIdentifier": str,
        "startTime": datetime,
        "status": ZonalShiftStatusType,
        "zonalShiftId": str,
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

StartZonalShiftRequestRequestTypeDef = TypedDict(
    "StartZonalShiftRequestRequestTypeDef",
    {
        "awayFrom": str,
        "comment": str,
        "expiresIn": str,
        "resourceIdentifier": str,
    },
)

_RequiredUpdateZonalShiftRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateZonalShiftRequestRequestTypeDef",
    {
        "zonalShiftId": str,
    },
)
_OptionalUpdateZonalShiftRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateZonalShiftRequestRequestTypeDef",
    {
        "comment": str,
        "expiresIn": str,
    },
    total=False,
)

class UpdateZonalShiftRequestRequestTypeDef(
    _RequiredUpdateZonalShiftRequestRequestTypeDef, _OptionalUpdateZonalShiftRequestRequestTypeDef
):
    pass

ZonalShiftTypeDef = TypedDict(
    "ZonalShiftTypeDef",
    {
        "awayFrom": str,
        "comment": str,
        "expiryTime": datetime,
        "resourceIdentifier": str,
        "startTime": datetime,
        "status": ZonalShiftStatusType,
        "zonalShiftId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetManagedResourceResponseTypeDef = TypedDict(
    "GetManagedResourceResponseTypeDef",
    {
        "appliedWeights": Dict[str, float],
        "arn": str,
        "name": str,
        "zonalShifts": List[ZonalShiftInResourceTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListManagedResourcesResponseTypeDef = TypedDict(
    "ListManagedResourcesResponseTypeDef",
    {
        "items": List[ManagedResourceSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListZonalShiftsResponseTypeDef = TypedDict(
    "ListZonalShiftsResponseTypeDef",
    {
        "items": List[ZonalShiftSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
