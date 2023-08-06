"""
Type annotations for privatenetworks service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_privatenetworks.client import Private5GClient
    from mypy_boto3_privatenetworks.paginator import (
        ListDeviceIdentifiersPaginator,
        ListNetworkResourcesPaginator,
        ListNetworkSitesPaginator,
        ListNetworksPaginator,
        ListOrdersPaginator,
    )

    session = Session()
    client: Private5GClient = session.client("privatenetworks")

    list_device_identifiers_paginator: ListDeviceIdentifiersPaginator = client.get_paginator("list_device_identifiers")
    list_network_resources_paginator: ListNetworkResourcesPaginator = client.get_paginator("list_network_resources")
    list_network_sites_paginator: ListNetworkSitesPaginator = client.get_paginator("list_network_sites")
    list_networks_paginator: ListNetworksPaginator = client.get_paginator("list_networks")
    list_orders_paginator: ListOrdersPaginator = client.get_paginator("list_orders")
    ```
"""
import sys
from typing import Generic, Iterator, Mapping, Sequence, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import (
    DeviceIdentifierFilterKeysType,
    NetworkResourceFilterKeysType,
    OrderFilterKeysType,
)
from .type_defs import (
    ListDeviceIdentifiersResponseTypeDef,
    ListNetworkResourcesResponseTypeDef,
    ListNetworkSitesResponseTypeDef,
    ListNetworksResponseTypeDef,
    ListOrdersResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ListDeviceIdentifiersPaginator",
    "ListNetworkResourcesPaginator",
    "ListNetworkSitesPaginator",
    "ListNetworksPaginator",
    "ListOrdersPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDeviceIdentifiersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks.html#Private5G.Paginator.ListDeviceIdentifiers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listdeviceidentifierspaginator)
    """

    def paginate(
        self,
        *,
        networkArn: str,
        filters: Mapping[DeviceIdentifierFilterKeysType, Sequence[str]] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDeviceIdentifiersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks.html#Private5G.Paginator.ListDeviceIdentifiers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listdeviceidentifierspaginator)
        """


class ListNetworkResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks.html#Private5G.Paginator.ListNetworkResources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listnetworkresourcespaginator)
    """

    def paginate(
        self,
        *,
        networkArn: str,
        filters: Mapping[NetworkResourceFilterKeysType, Sequence[str]] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListNetworkResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks.html#Private5G.Paginator.ListNetworkResources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listnetworkresourcespaginator)
        """


class ListNetworkSitesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks.html#Private5G.Paginator.ListNetworkSites)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listnetworksitespaginator)
    """

    def paginate(
        self,
        *,
        networkArn: str,
        filters: Mapping[Literal["STATUS"], Sequence[str]] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListNetworkSitesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks.html#Private5G.Paginator.ListNetworkSites.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listnetworksitespaginator)
        """


class ListNetworksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks.html#Private5G.Paginator.ListNetworks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listnetworkspaginator)
    """

    def paginate(
        self,
        *,
        filters: Mapping[Literal["STATUS"], Sequence[str]] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks.html#Private5G.Paginator.ListNetworks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listnetworkspaginator)
        """


class ListOrdersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks.html#Private5G.Paginator.ListOrders)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listorderspaginator)
    """

    def paginate(
        self,
        *,
        networkArn: str,
        filters: Mapping[OrderFilterKeysType, Sequence[str]] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOrdersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/privatenetworks.html#Private5G.Paginator.ListOrders.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_privatenetworks/paginators/#listorderspaginator)
        """
