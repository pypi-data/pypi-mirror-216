"""
Main interface for arc-zonal-shift service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_arc_zonal_shift import (
        ARCZonalShiftClient,
        Client,
        ListManagedResourcesPaginator,
        ListZonalShiftsPaginator,
    )

    session = get_session()
    async with session.create_client("arc-zonal-shift") as client:
        client: ARCZonalShiftClient
        ...


    list_managed_resources_paginator: ListManagedResourcesPaginator = client.get_paginator("list_managed_resources")
    list_zonal_shifts_paginator: ListZonalShiftsPaginator = client.get_paginator("list_zonal_shifts")
    ```
"""
from .client import ARCZonalShiftClient
from .paginator import ListManagedResourcesPaginator, ListZonalShiftsPaginator

Client = ARCZonalShiftClient


__all__ = (
    "ARCZonalShiftClient",
    "Client",
    "ListManagedResourcesPaginator",
    "ListZonalShiftsPaginator",
)
