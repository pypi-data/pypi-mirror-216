"""
Type annotations for gamesparks service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_gamesparks.client import GameSparksClient

    session = get_session()
    async with session.create_client("gamesparks") as client:
        client: GameSparksClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListExtensionsPaginator,
    ListExtensionVersionsPaginator,
    ListGamesPaginator,
    ListGeneratedCodeJobsPaginator,
    ListSnapshotsPaginator,
    ListStageDeploymentsPaginator,
    ListStagesPaginator,
)
from .type_defs import (
    CreateGameResultTypeDef,
    CreateSnapshotResultTypeDef,
    CreateStageResultTypeDef,
    DisconnectPlayerResultTypeDef,
    ExportSnapshotResultTypeDef,
    GeneratorTypeDef,
    GetExtensionResultTypeDef,
    GetExtensionVersionResultTypeDef,
    GetGameConfigurationResultTypeDef,
    GetGameResultTypeDef,
    GetGeneratedCodeJobResultTypeDef,
    GetPlayerConnectionStatusResultTypeDef,
    GetSnapshotResultTypeDef,
    GetStageDeploymentResultTypeDef,
    GetStageResultTypeDef,
    ImportGameConfigurationResultTypeDef,
    ImportGameConfigurationSourceTypeDef,
    ListExtensionsResultTypeDef,
    ListExtensionVersionsResultTypeDef,
    ListGamesResultTypeDef,
    ListGeneratedCodeJobsResultTypeDef,
    ListSnapshotsResultTypeDef,
    ListStageDeploymentsResultTypeDef,
    ListStagesResultTypeDef,
    ListTagsForResourceResultTypeDef,
    SectionModificationTypeDef,
    StartGeneratedCodeJobResultTypeDef,
    StartStageDeploymentResultTypeDef,
    UpdateGameConfigurationResultTypeDef,
    UpdateGameResultTypeDef,
    UpdateSnapshotResultTypeDef,
    UpdateStageResultTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("GameSparksClient",)

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

class GameSparksClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GameSparksClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#can_paginate)
        """
    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#close)
        """
    async def create_game(
        self,
        *,
        GameName: str,
        ClientToken: str = ...,
        Description: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateGameResultTypeDef:
        """
        Creates a new game with an empty configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.create_game)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#create_game)
        """
    async def create_snapshot(
        self, *, GameName: str, Description: str = ...
    ) -> CreateSnapshotResultTypeDef:
        """
        Creates a snapshot of the game configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.create_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#create_snapshot)
        """
    async def create_stage(
        self,
        *,
        GameName: str,
        Role: str,
        StageName: str,
        ClientToken: str = ...,
        Description: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateStageResultTypeDef:
        """
        Creates a new stage for stage-by-stage game development and deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.create_stage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#create_stage)
        """
    async def delete_game(self, *, GameName: str) -> Dict[str, Any]:
        """
        Deletes a game.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.delete_game)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#delete_game)
        """
    async def delete_stage(self, *, GameName: str, StageName: str) -> Dict[str, Any]:
        """
        Deletes a stage from a game, along with the associated game runtime.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.delete_stage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#delete_stage)
        """
    async def disconnect_player(
        self, *, GameName: str, PlayerId: str, StageName: str
    ) -> DisconnectPlayerResultTypeDef:
        """
        Disconnects a player from the game runtime.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.disconnect_player)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#disconnect_player)
        """
    async def export_snapshot(
        self, *, GameName: str, SnapshotId: str
    ) -> ExportSnapshotResultTypeDef:
        """
        Exports a game configuration snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.export_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#export_snapshot)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#generate_presigned_url)
        """
    async def get_extension(self, *, Name: str, Namespace: str) -> GetExtensionResultTypeDef:
        """
        Gets details about a specified extension.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.get_extension)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#get_extension)
        """
    async def get_extension_version(
        self, *, ExtensionVersion: str, Name: str, Namespace: str
    ) -> GetExtensionVersionResultTypeDef:
        """
        Gets details about a specified extension version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.get_extension_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#get_extension_version)
        """
    async def get_game(self, *, GameName: str) -> GetGameResultTypeDef:
        """
        Gets details about a game.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.get_game)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#get_game)
        """
    async def get_game_configuration(
        self, *, GameName: str, Sections: Sequence[str] = ...
    ) -> GetGameConfigurationResultTypeDef:
        """
        Gets the configuration of the game.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.get_game_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#get_game_configuration)
        """
    async def get_generated_code_job(
        self, *, GameName: str, JobId: str, SnapshotId: str
    ) -> GetGeneratedCodeJobResultTypeDef:
        """
        Gets details about a job that is generating code for a snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.get_generated_code_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#get_generated_code_job)
        """
    async def get_player_connection_status(
        self, *, GameName: str, PlayerId: str, StageName: str
    ) -> GetPlayerConnectionStatusResultTypeDef:
        """
        Gets the status of a player's connection to the game runtime.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.get_player_connection_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#get_player_connection_status)
        """
    async def get_snapshot(
        self, *, GameName: str, SnapshotId: str, Sections: Sequence[str] = ...
    ) -> GetSnapshotResultTypeDef:
        """
        Gets a copy of the game configuration in a snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.get_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#get_snapshot)
        """
    async def get_stage(self, *, GameName: str, StageName: str) -> GetStageResultTypeDef:
        """
        Gets information about a stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.get_stage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#get_stage)
        """
    async def get_stage_deployment(
        self, *, GameName: str, StageName: str, DeploymentId: str = ...
    ) -> GetStageDeploymentResultTypeDef:
        """
        Gets information about a stage deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.get_stage_deployment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#get_stage_deployment)
        """
    async def import_game_configuration(
        self, *, GameName: str, ImportSource: ImportGameConfigurationSourceTypeDef
    ) -> ImportGameConfigurationResultTypeDef:
        """
        Imports a game configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.import_game_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#import_game_configuration)
        """
    async def list_extension_versions(
        self, *, Name: str, Namespace: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListExtensionVersionsResultTypeDef:
        """
        Gets a paginated list of available versions for the extension.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.list_extension_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#list_extension_versions)
        """
    async def list_extensions(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListExtensionsResultTypeDef:
        """
        Gets a paginated list of available extensions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.list_extensions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#list_extensions)
        """
    async def list_games(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListGamesResultTypeDef:
        """
        Gets a paginated list of games.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.list_games)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#list_games)
        """
    async def list_generated_code_jobs(
        self, *, GameName: str, SnapshotId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListGeneratedCodeJobsResultTypeDef:
        """
        Gets a paginated list of code generation jobs for a snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.list_generated_code_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#list_generated_code_jobs)
        """
    async def list_snapshots(
        self, *, GameName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListSnapshotsResultTypeDef:
        """
        Gets a paginated list of snapshot summaries from the game.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.list_snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#list_snapshots)
        """
    async def list_stage_deployments(
        self, *, GameName: str, StageName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListStageDeploymentsResultTypeDef:
        """
        Gets a paginated list of stage deployment summaries from the game.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.list_stage_deployments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#list_stage_deployments)
        """
    async def list_stages(
        self, *, GameName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListStagesResultTypeDef:
        """
        Gets a paginated list of stage summaries from the game.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.list_stages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#list_stages)
        """
    async def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResultTypeDef:
        """
        Lists the tags associated with a GameSparks resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#list_tags_for_resource)
        """
    async def start_generated_code_job(
        self, *, GameName: str, Generator: GeneratorTypeDef, SnapshotId: str
    ) -> StartGeneratedCodeJobResultTypeDef:
        """
        Starts an asynchronous process that generates client code for system-defined and
        custom messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.start_generated_code_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#start_generated_code_job)
        """
    async def start_stage_deployment(
        self, *, GameName: str, SnapshotId: str, StageName: str, ClientToken: str = ...
    ) -> StartStageDeploymentResultTypeDef:
        """
        Deploys a snapshot to the stage and creates a new game runtime.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.start_stage_deployment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#start_stage_deployment)
        """
    async def tag_resource(self, *, ResourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds tags to a GameSparks resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#tag_resource)
        """
    async def untag_resource(self, *, ResourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from a GameSparks resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#untag_resource)
        """
    async def update_game(
        self, *, GameName: str, Description: str = ...
    ) -> UpdateGameResultTypeDef:
        """
        Updates details of the game.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.update_game)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#update_game)
        """
    async def update_game_configuration(
        self, *, GameName: str, Modifications: Sequence[SectionModificationTypeDef]
    ) -> UpdateGameConfigurationResultTypeDef:
        """
        Updates one or more sections of the game configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.update_game_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#update_game_configuration)
        """
    async def update_snapshot(
        self, *, GameName: str, SnapshotId: str, Description: str = ...
    ) -> UpdateSnapshotResultTypeDef:
        """
        Updates the metadata of a GameSparks snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.update_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#update_snapshot)
        """
    async def update_stage(
        self, *, GameName: str, StageName: str, Description: str = ..., Role: str = ...
    ) -> UpdateStageResultTypeDef:
        """
        Updates the metadata of a stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.update_stage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#update_stage)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_extension_versions"]
    ) -> ListExtensionVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_extensions"]) -> ListExtensionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_games"]) -> ListGamesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_generated_code_jobs"]
    ) -> ListGeneratedCodeJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_snapshots"]) -> ListSnapshotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_stage_deployments"]
    ) -> ListStageDeploymentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_stages"]) -> ListStagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/#get_paginator)
        """
    async def __aenter__(self) -> "GameSparksClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamesparks.html#GameSparks.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/client/)
        """
