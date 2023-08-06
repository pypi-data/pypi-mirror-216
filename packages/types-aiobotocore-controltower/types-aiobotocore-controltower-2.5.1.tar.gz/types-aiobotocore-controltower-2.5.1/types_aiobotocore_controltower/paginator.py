"""
Type annotations for controltower service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_controltower.client import ControlTowerClient
    from types_aiobotocore_controltower.paginator import (
        ListEnabledControlsPaginator,
    )

    session = get_session()
    with session.create_client("controltower") as client:
        client: ControlTowerClient

        list_enabled_controls_paginator: ListEnabledControlsPaginator = client.get_paginator("list_enabled_controls")
    ```
"""
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListEnabledControlsOutputTypeDef, PaginatorConfigTypeDef

__all__ = ("ListEnabledControlsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListEnabledControlsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Paginator.ListEnabledControls)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/paginators/#listenabledcontrolspaginator)
    """

    def paginate(
        self, *, targetIdentifier: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListEnabledControlsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Paginator.ListEnabledControls.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/paginators/#listenabledcontrolspaginator)
        """
