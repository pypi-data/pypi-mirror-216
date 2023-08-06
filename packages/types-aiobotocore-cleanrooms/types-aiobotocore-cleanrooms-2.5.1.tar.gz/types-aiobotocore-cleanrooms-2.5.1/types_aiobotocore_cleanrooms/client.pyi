"""
Type annotations for cleanrooms service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cleanrooms.client import CleanRoomsServiceClient

    session = get_session()
    async with session.create_client("cleanrooms") as client:
        client: CleanRoomsServiceClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AnalysisRuleTypeType,
    CollaborationQueryLogStatusType,
    ConfiguredTableAnalysisRuleTypeType,
    FilterableMemberStatusType,
    MemberAbilityType,
    MembershipQueryLogStatusType,
    MembershipStatusType,
    ProtectedQueryStatusType,
)
from .paginator import (
    ListCollaborationsPaginator,
    ListConfiguredTableAssociationsPaginator,
    ListConfiguredTablesPaginator,
    ListMembershipsPaginator,
    ListMembersPaginator,
    ListProtectedQueriesPaginator,
    ListSchemasPaginator,
)
from .type_defs import (
    BatchGetSchemaOutputTypeDef,
    ConfiguredTableAnalysisRulePolicyTypeDef,
    CreateCollaborationOutputTypeDef,
    CreateConfiguredTableAnalysisRuleOutputTypeDef,
    CreateConfiguredTableAssociationOutputTypeDef,
    CreateConfiguredTableOutputTypeDef,
    CreateMembershipOutputTypeDef,
    DataEncryptionMetadataTypeDef,
    GetCollaborationOutputTypeDef,
    GetConfiguredTableAnalysisRuleOutputTypeDef,
    GetConfiguredTableAssociationOutputTypeDef,
    GetConfiguredTableOutputTypeDef,
    GetMembershipOutputTypeDef,
    GetProtectedQueryOutputTypeDef,
    GetSchemaAnalysisRuleOutputTypeDef,
    GetSchemaOutputTypeDef,
    ListCollaborationsOutputTypeDef,
    ListConfiguredTableAssociationsOutputTypeDef,
    ListConfiguredTablesOutputTypeDef,
    ListMembershipsOutputTypeDef,
    ListMembersOutputTypeDef,
    ListProtectedQueriesOutputTypeDef,
    ListSchemasOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    MemberSpecificationTypeDef,
    ProtectedQueryResultConfigurationTypeDef,
    ProtectedQuerySQLParametersTypeDef,
    StartProtectedQueryOutputTypeDef,
    TableReferenceTypeDef,
    UpdateCollaborationOutputTypeDef,
    UpdateConfiguredTableAnalysisRuleOutputTypeDef,
    UpdateConfiguredTableAssociationOutputTypeDef,
    UpdateConfiguredTableOutputTypeDef,
    UpdateMembershipOutputTypeDef,
    UpdateProtectedQueryOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("CleanRoomsServiceClient",)

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

class CleanRoomsServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CleanRoomsServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#exceptions)
        """
    async def batch_get_schema(
        self, *, collaborationIdentifier: str, names: Sequence[str]
    ) -> BatchGetSchemaOutputTypeDef:
        """
        Retrieves multiple schemas by their identifiers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.batch_get_schema)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#batch_get_schema)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#can_paginate)
        """
    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#close)
        """
    async def create_collaboration(
        self,
        *,
        members: Sequence[MemberSpecificationTypeDef],
        name: str,
        description: str,
        creatorMemberAbilities: Sequence[MemberAbilityType],
        creatorDisplayName: str,
        queryLogStatus: CollaborationQueryLogStatusType,
        dataEncryptionMetadata: DataEncryptionMetadataTypeDef = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateCollaborationOutputTypeDef:
        """
        Creates a new collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.create_collaboration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#create_collaboration)
        """
    async def create_configured_table(
        self,
        *,
        name: str,
        tableReference: TableReferenceTypeDef,
        allowedColumns: Sequence[str],
        analysisMethod: Literal["DIRECT_QUERY"],
        description: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateConfiguredTableOutputTypeDef:
        """
        Creates a new configured table resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.create_configured_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#create_configured_table)
        """
    async def create_configured_table_analysis_rule(
        self,
        *,
        configuredTableIdentifier: str,
        analysisRuleType: ConfiguredTableAnalysisRuleTypeType,
        analysisRulePolicy: ConfiguredTableAnalysisRulePolicyTypeDef
    ) -> CreateConfiguredTableAnalysisRuleOutputTypeDef:
        """
        Creates a new analysis rule for a configured table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.create_configured_table_analysis_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#create_configured_table_analysis_rule)
        """
    async def create_configured_table_association(
        self,
        *,
        name: str,
        membershipIdentifier: str,
        configuredTableIdentifier: str,
        roleArn: str,
        description: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateConfiguredTableAssociationOutputTypeDef:
        """
        Creates a configured table association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.create_configured_table_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#create_configured_table_association)
        """
    async def create_membership(
        self,
        *,
        collaborationIdentifier: str,
        queryLogStatus: MembershipQueryLogStatusType,
        tags: Mapping[str, str] = ...
    ) -> CreateMembershipOutputTypeDef:
        """
        Creates a membership for a specific collaboration identifier and joins the
        collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.create_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#create_membership)
        """
    async def delete_collaboration(self, *, collaborationIdentifier: str) -> Dict[str, Any]:
        """
        Deletes a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.delete_collaboration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#delete_collaboration)
        """
    async def delete_configured_table(self, *, configuredTableIdentifier: str) -> Dict[str, Any]:
        """
        Deletes a configured table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.delete_configured_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#delete_configured_table)
        """
    async def delete_configured_table_analysis_rule(
        self,
        *,
        configuredTableIdentifier: str,
        analysisRuleType: ConfiguredTableAnalysisRuleTypeType
    ) -> Dict[str, Any]:
        """
        Deletes a configured table analysis rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.delete_configured_table_analysis_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#delete_configured_table_analysis_rule)
        """
    async def delete_configured_table_association(
        self, *, configuredTableAssociationIdentifier: str, membershipIdentifier: str
    ) -> Dict[str, Any]:
        """
        Deletes a configured table association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.delete_configured_table_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#delete_configured_table_association)
        """
    async def delete_member(
        self, *, collaborationIdentifier: str, accountId: str
    ) -> Dict[str, Any]:
        """
        Removes the specified member from a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.delete_member)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#delete_member)
        """
    async def delete_membership(self, *, membershipIdentifier: str) -> Dict[str, Any]:
        """
        Deletes a specified membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.delete_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#delete_membership)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#generate_presigned_url)
        """
    async def get_collaboration(
        self, *, collaborationIdentifier: str
    ) -> GetCollaborationOutputTypeDef:
        """
        Returns metadata about a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_collaboration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_collaboration)
        """
    async def get_configured_table(
        self, *, configuredTableIdentifier: str
    ) -> GetConfiguredTableOutputTypeDef:
        """
        Retrieves a configured table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_configured_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_configured_table)
        """
    async def get_configured_table_analysis_rule(
        self,
        *,
        configuredTableIdentifier: str,
        analysisRuleType: ConfiguredTableAnalysisRuleTypeType
    ) -> GetConfiguredTableAnalysisRuleOutputTypeDef:
        """
        Retrieves a configured table analysis rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_configured_table_analysis_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_configured_table_analysis_rule)
        """
    async def get_configured_table_association(
        self, *, configuredTableAssociationIdentifier: str, membershipIdentifier: str
    ) -> GetConfiguredTableAssociationOutputTypeDef:
        """
        Retrieves a configured table association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_configured_table_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_configured_table_association)
        """
    async def get_membership(self, *, membershipIdentifier: str) -> GetMembershipOutputTypeDef:
        """
        Retrieves a specified membership for an identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_membership)
        """
    async def get_protected_query(
        self, *, membershipIdentifier: str, protectedQueryIdentifier: str
    ) -> GetProtectedQueryOutputTypeDef:
        """
        Returns query processing metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_protected_query)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_protected_query)
        """
    async def get_schema(
        self, *, collaborationIdentifier: str, name: str
    ) -> GetSchemaOutputTypeDef:
        """
        Retrieves the schema for a relation within a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_schema)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_schema)
        """
    async def get_schema_analysis_rule(
        self, *, collaborationIdentifier: str, name: str, type: AnalysisRuleTypeType
    ) -> GetSchemaAnalysisRuleOutputTypeDef:
        """
        Retrieves a schema analysis rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_schema_analysis_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_schema_analysis_rule)
        """
    async def list_collaborations(
        self,
        *,
        nextToken: str = ...,
        maxResults: int = ...,
        memberStatus: FilterableMemberStatusType = ...
    ) -> ListCollaborationsOutputTypeDef:
        """
        Lists collaborations the caller owns, is active in, or has been invited to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_collaborations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_collaborations)
        """
    async def list_configured_table_associations(
        self, *, membershipIdentifier: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListConfiguredTableAssociationsOutputTypeDef:
        """
        Lists configured table associations for a membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_configured_table_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_configured_table_associations)
        """
    async def list_configured_tables(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListConfiguredTablesOutputTypeDef:
        """
        Lists configured tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_configured_tables)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_configured_tables)
        """
    async def list_members(
        self, *, collaborationIdentifier: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListMembersOutputTypeDef:
        """
        Lists all members within a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_members)
        """
    async def list_memberships(
        self, *, nextToken: str = ..., maxResults: int = ..., status: MembershipStatusType = ...
    ) -> ListMembershipsOutputTypeDef:
        """
        Lists all memberships resources within the caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_memberships)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_memberships)
        """
    async def list_protected_queries(
        self,
        *,
        membershipIdentifier: str,
        status: ProtectedQueryStatusType = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListProtectedQueriesOutputTypeDef:
        """
        Lists protected queries, sorted by the most recent query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_protected_queries)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_protected_queries)
        """
    async def list_schemas(
        self,
        *,
        collaborationIdentifier: str,
        schemaType: Literal["TABLE"] = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListSchemasOutputTypeDef:
        """
        Lists the schemas for relations within a collaboration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_schemas)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_schemas)
        """
    async def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceOutputTypeDef:
        """
        Lists all of the tags that have been added to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#list_tags_for_resource)
        """
    async def start_protected_query(
        self,
        *,
        type: Literal["SQL"],
        membershipIdentifier: str,
        sqlParameters: ProtectedQuerySQLParametersTypeDef,
        resultConfiguration: ProtectedQueryResultConfigurationTypeDef
    ) -> StartProtectedQueryOutputTypeDef:
        """
        Creates a protected query that is started by AWS Clean Rooms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.start_protected_query)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#start_protected_query)
        """
    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Tags a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#tag_resource)
        """
    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes a tag or list of tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#untag_resource)
        """
    async def update_collaboration(
        self, *, collaborationIdentifier: str, name: str = ..., description: str = ...
    ) -> UpdateCollaborationOutputTypeDef:
        """
        Updates collaboration metadata and can only be called by the collaboration
        owner.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.update_collaboration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#update_collaboration)
        """
    async def update_configured_table(
        self, *, configuredTableIdentifier: str, name: str = ..., description: str = ...
    ) -> UpdateConfiguredTableOutputTypeDef:
        """
        Updates a configured table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.update_configured_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#update_configured_table)
        """
    async def update_configured_table_analysis_rule(
        self,
        *,
        configuredTableIdentifier: str,
        analysisRuleType: ConfiguredTableAnalysisRuleTypeType,
        analysisRulePolicy: ConfiguredTableAnalysisRulePolicyTypeDef
    ) -> UpdateConfiguredTableAnalysisRuleOutputTypeDef:
        """
        Updates a configured table analysis rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.update_configured_table_analysis_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#update_configured_table_analysis_rule)
        """
    async def update_configured_table_association(
        self,
        *,
        configuredTableAssociationIdentifier: str,
        membershipIdentifier: str,
        description: str = ...,
        roleArn: str = ...
    ) -> UpdateConfiguredTableAssociationOutputTypeDef:
        """
        Updates a configured table association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.update_configured_table_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#update_configured_table_association)
        """
    async def update_membership(
        self, *, membershipIdentifier: str, queryLogStatus: MembershipQueryLogStatusType = ...
    ) -> UpdateMembershipOutputTypeDef:
        """
        Updates a membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.update_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#update_membership)
        """
    async def update_protected_query(
        self,
        *,
        membershipIdentifier: str,
        protectedQueryIdentifier: str,
        targetStatus: Literal["CANCELLED"]
    ) -> UpdateProtectedQueryOutputTypeDef:
        """
        Updates the processing of a currently running query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.update_protected_query)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#update_protected_query)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_collaborations"]
    ) -> ListCollaborationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_configured_table_associations"]
    ) -> ListConfiguredTableAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_configured_tables"]
    ) -> ListConfiguredTablesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_members"]) -> ListMembersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_memberships"]
    ) -> ListMembershipsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_protected_queries"]
    ) -> ListProtectedQueriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_schemas"]) -> ListSchemasPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/#get_paginator)
        """
    async def __aenter__(self) -> "CleanRoomsServiceClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanrooms.html#CleanRoomsService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/client/)
        """
