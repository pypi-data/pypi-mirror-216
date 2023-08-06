"""
Main interface for controltower service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_controltower import (
        Client,
        ControlTowerClient,
        ListEnabledControlsPaginator,
    )

    session = get_session()
    async with session.create_client("controltower") as client:
        client: ControlTowerClient
        ...


    list_enabled_controls_paginator: ListEnabledControlsPaginator = client.get_paginator("list_enabled_controls")
    ```
"""
from .client import ControlTowerClient
from .paginator import ListEnabledControlsPaginator

Client = ControlTowerClient

__all__ = ("Client", "ControlTowerClient", "ListEnabledControlsPaginator")
