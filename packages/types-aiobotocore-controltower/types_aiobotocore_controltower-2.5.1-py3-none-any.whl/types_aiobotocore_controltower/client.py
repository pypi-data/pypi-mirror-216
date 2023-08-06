"""
Type annotations for controltower service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_controltower.client import ControlTowerClient

    session = get_session()
    async with session.create_client("controltower") as client:
        client: ControlTowerClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListEnabledControlsPaginator
from .type_defs import (
    DisableControlOutputTypeDef,
    EnableControlOutputTypeDef,
    GetControlOperationOutputTypeDef,
    ListEnabledControlsOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ControlTowerClient",)


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
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ControlTowerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ControlTowerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#close)
        """

    async def disable_control(
        self, *, controlIdentifier: str, targetIdentifier: str
    ) -> DisableControlOutputTypeDef:
        """
        This API call turns off a control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.disable_control)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#disable_control)
        """

    async def enable_control(
        self, *, controlIdentifier: str, targetIdentifier: str
    ) -> EnableControlOutputTypeDef:
        """
        This API call activates a control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.enable_control)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#enable_control)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#generate_presigned_url)
        """

    async def get_control_operation(
        self, *, operationIdentifier: str
    ) -> GetControlOperationOutputTypeDef:
        """
        Returns the status of a particular `EnableControl` or `DisableControl`
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.get_control_operation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#get_control_operation)
        """

    async def list_enabled_controls(
        self, *, targetIdentifier: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListEnabledControlsOutputTypeDef:
        """
        Lists the controls enabled by AWS Control Tower on the specified organizational
        unit and the accounts it contains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.list_enabled_controls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#list_enabled_controls)
        """

    def get_paginator(
        self, operation_name: Literal["list_enabled_controls"]
    ) -> ListEnabledControlsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#get_paginator)
        """

    async def __aenter__(self) -> "ControlTowerClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/)
        """
