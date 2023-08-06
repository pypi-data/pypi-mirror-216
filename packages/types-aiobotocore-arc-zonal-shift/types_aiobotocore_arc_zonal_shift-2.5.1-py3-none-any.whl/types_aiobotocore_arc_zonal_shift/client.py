"""
Type annotations for arc-zonal-shift service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_arc_zonal_shift.client import ARCZonalShiftClient

    session = get_session()
    async with session.create_client("arc-zonal-shift") as client:
        client: ARCZonalShiftClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import ZonalShiftStatusType
from .paginator import ListManagedResourcesPaginator, ListZonalShiftsPaginator
from .type_defs import (
    GetManagedResourceResponseTypeDef,
    ListManagedResourcesResponseTypeDef,
    ListZonalShiftsResponseTypeDef,
    ZonalShiftTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ARCZonalShiftClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ARCZonalShiftClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ARCZonalShiftClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#can_paginate)
        """

    async def cancel_zonal_shift(self, *, zonalShiftId: str) -> ZonalShiftTypeDef:
        """
        Cancel a zonal shift in Amazon Route 53 Application Recovery Controller that
        you've started for a resource in your AWS account in an AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client.cancel_zonal_shift)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#cancel_zonal_shift)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#close)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#generate_presigned_url)
        """

    async def get_managed_resource(
        self, *, resourceIdentifier: str
    ) -> GetManagedResourceResponseTypeDef:
        """
        Get information about a resource that's been registered for zonal shifts with
        Amazon Route 53 Application Recovery Controller in this AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client.get_managed_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#get_managed_resource)
        """

    async def list_managed_resources(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListManagedResourcesResponseTypeDef:
        """
        Lists all the resources in your AWS account in this AWS Region that are managed
        for zonal shifts in Amazon Route 53 Application Recovery Controller, and
        information about them.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client.list_managed_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#list_managed_resources)
        """

    async def list_zonal_shifts(
        self, *, maxResults: int = ..., nextToken: str = ..., status: ZonalShiftStatusType = ...
    ) -> ListZonalShiftsResponseTypeDef:
        """
        Lists all the active zonal shifts in Amazon Route 53 Application Recovery
        Controller in your AWS account in this AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client.list_zonal_shifts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#list_zonal_shifts)
        """

    async def start_zonal_shift(
        self, *, awayFrom: str, comment: str, expiresIn: str, resourceIdentifier: str
    ) -> ZonalShiftTypeDef:
        """
        You start a zonal shift to temporarily move load balancer traffic away from an
        Availability Zone in a AWS Region, to help your application recover immediately,
        for example, from a developer's bad code deployment or from an AWS
        infrastructure failure in a single Availability Zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client.start_zonal_shift)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#start_zonal_shift)
        """

    async def update_zonal_shift(
        self, *, zonalShiftId: str, comment: str = ..., expiresIn: str = ...
    ) -> ZonalShiftTypeDef:
        """
        Update an active zonal shift in Amazon Route 53 Application Recovery Controller
        in your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client.update_zonal_shift)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#update_zonal_shift)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_managed_resources"]
    ) -> ListManagedResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_zonal_shifts"]
    ) -> ListZonalShiftsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#get_paginator)
        """

    async def __aenter__(self) -> "ARCZonalShiftClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/)
        """
