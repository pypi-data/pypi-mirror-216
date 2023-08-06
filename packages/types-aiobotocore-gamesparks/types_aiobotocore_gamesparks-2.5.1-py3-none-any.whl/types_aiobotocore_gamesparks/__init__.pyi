"""
Main interface for gamesparks service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_gamesparks import (
        Client,
        GameSparksClient,
        ListExtensionVersionsPaginator,
        ListExtensionsPaginator,
        ListGamesPaginator,
        ListGeneratedCodeJobsPaginator,
        ListSnapshotsPaginator,
        ListStageDeploymentsPaginator,
        ListStagesPaginator,
    )

    session = get_session()
    async with session.create_client("gamesparks") as client:
        client: GameSparksClient
        ...


    list_extension_versions_paginator: ListExtensionVersionsPaginator = client.get_paginator("list_extension_versions")
    list_extensions_paginator: ListExtensionsPaginator = client.get_paginator("list_extensions")
    list_games_paginator: ListGamesPaginator = client.get_paginator("list_games")
    list_generated_code_jobs_paginator: ListGeneratedCodeJobsPaginator = client.get_paginator("list_generated_code_jobs")
    list_snapshots_paginator: ListSnapshotsPaginator = client.get_paginator("list_snapshots")
    list_stage_deployments_paginator: ListStageDeploymentsPaginator = client.get_paginator("list_stage_deployments")
    list_stages_paginator: ListStagesPaginator = client.get_paginator("list_stages")
    ```
"""
from .client import GameSparksClient
from .paginator import (
    ListExtensionsPaginator,
    ListExtensionVersionsPaginator,
    ListGamesPaginator,
    ListGeneratedCodeJobsPaginator,
    ListSnapshotsPaginator,
    ListStageDeploymentsPaginator,
    ListStagesPaginator,
)

Client = GameSparksClient

__all__ = (
    "Client",
    "GameSparksClient",
    "ListExtensionVersionsPaginator",
    "ListExtensionsPaginator",
    "ListGamesPaginator",
    "ListGeneratedCodeJobsPaginator",
    "ListSnapshotsPaginator",
    "ListStageDeploymentsPaginator",
    "ListStagesPaginator",
)
