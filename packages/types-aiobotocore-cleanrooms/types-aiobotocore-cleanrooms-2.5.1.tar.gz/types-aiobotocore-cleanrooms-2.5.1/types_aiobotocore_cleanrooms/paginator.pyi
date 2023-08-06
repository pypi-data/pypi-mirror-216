"""
Type annotations for cleanrooms service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cleanrooms.client import CleanRoomsServiceClient
    from types_aiobotocore_cleanrooms.paginator import (
        ListCollaborationsPaginator,
        ListConfiguredTableAssociationsPaginator,
        ListConfiguredTablesPaginator,
        ListMembersPaginator,
        ListMembershipsPaginator,
        ListProtectedQueriesPaginator,
        ListSchemasPaginator,
    )

    session = get_session()
    with session.create_client("cleanrooms") as client:
        client: CleanRoomsServiceClient

        list_collaborations_paginator: ListCollaborationsPaginator = client.get_paginator("list_collaborations")
        list_configured_table_associations_paginator: ListConfiguredTableAssociationsPaginator = client.get_paginator("list_configured_table_associations")
        list_configured_tables_paginator: ListConfiguredTablesPaginator = client.get_paginator("list_configured_tables")
        list_members_paginator: ListMembersPaginator = client.get_paginator("list_members")
        list_memberships_paginator: ListMembershipsPaginator = client.get_paginator("list_memberships")
        list_protected_queries_paginator: ListProtectedQueriesPaginator = client.get_paginator("list_protected_queries")
        list_schemas_paginator: ListSchemasPaginator = client.get_paginator("list_schemas")
    ```
"""
import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import FilterableMemberStatusType, MembershipStatusType, ProtectedQueryStatusType
from .type_defs import (
    ListCollaborationsOutputTypeDef,
    ListConfiguredTableAssociationsOutputTypeDef,
    ListConfiguredTablesOutputTypeDef,
    ListMembershipsOutputTypeDef,
    ListMembersOutputTypeDef,
    ListProtectedQueriesOutputTypeDef,
    ListSchemasOutputTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "ListCollaborationsPaginator",
    "ListConfiguredTableAssociationsPaginator",
    "ListConfiguredTablesPaginator",
    "ListMembersPaginator",
    "ListMembershipsPaginator",
    "ListProtectedQueriesPaginator",
    "ListSchemasPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListCollaborationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Paginator.ListCollaborations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listcollaborationspaginator)
    """

    def paginate(
        self,
        *,
        memberStatus: FilterableMemberStatusType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListCollaborationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Paginator.ListCollaborations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listcollaborationspaginator)
        """

class ListConfiguredTableAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Paginator.ListConfiguredTableAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listconfiguredtableassociationspaginator)
    """

    def paginate(
        self, *, membershipIdentifier: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListConfiguredTableAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Paginator.ListConfiguredTableAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listconfiguredtableassociationspaginator)
        """

class ListConfiguredTablesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Paginator.ListConfiguredTables)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listconfiguredtablespaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListConfiguredTablesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Paginator.ListConfiguredTables.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listconfiguredtablespaginator)
        """

class ListMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Paginator.ListMembers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listmemberspaginator)
    """

    def paginate(
        self, *, collaborationIdentifier: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListMembersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Paginator.ListMembers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listmemberspaginator)
        """

class ListMembershipsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Paginator.ListMemberships)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listmembershipspaginator)
    """

    def paginate(
        self,
        *,
        status: MembershipStatusType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListMembershipsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Paginator.ListMemberships.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listmembershipspaginator)
        """

class ListProtectedQueriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Paginator.ListProtectedQueries)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listprotectedqueriespaginator)
    """

    def paginate(
        self,
        *,
        membershipIdentifier: str,
        status: ProtectedQueryStatusType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListProtectedQueriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Paginator.ListProtectedQueries.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listprotectedqueriespaginator)
        """

class ListSchemasPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Paginator.ListSchemas)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listschemaspaginator)
    """

    def paginate(
        self,
        *,
        collaborationIdentifier: str,
        schemaType: Literal["TABLE"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListSchemasOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Paginator.ListSchemas.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/paginators/#listschemaspaginator)
        """
