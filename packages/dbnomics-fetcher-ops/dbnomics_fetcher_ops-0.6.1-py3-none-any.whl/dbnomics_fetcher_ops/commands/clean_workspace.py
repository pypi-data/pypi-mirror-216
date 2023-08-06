from pathlib import Path

import daiquiri
import typer
from humanfriendly import format_path

from dbnomics_fetcher_ops.app_args import get_app_args
from dbnomics_fetcher_ops.model.errors import FetcherDefNotFound
from dbnomics_fetcher_ops.model.pipeline_repo.gitlab import GitLabPipelineRepo
from dbnomics_fetcher_ops.services.clean_pipeline_workspaces import (
    DEFAULT_KEEP_FAILED_COUNT,
    DEFAULT_KEEP_SUCCESS_COUNT,
    clean_fetcher_workspace_pipeline_directories,
)

logger = daiquiri.getLogger(__name__)


def clean_workspace(
    workspace_dir: Path = typer.Argument(
        ...,
        envvar="WORKSPACE_DIR",
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        help="Workspace directory of a fetcher",
    ),
    keep_failed_count: int = typer.Option(
        DEFAULT_KEEP_FAILED_COUNT,
        "--failed",
        help="keep this number of failed pipeline directories in workspace",
    ),
    keep_success_count: int = typer.Option(
        DEFAULT_KEEP_SUCCESS_COUNT,
        "--success",
        help="keep this number of success pipeline directories in workspace",
    ),
):
    """Cleanup the workspaces of DBnomics fetcher pipelines.

    Workspaces are directories where jobs of the fetcher pipeline store data while running.

    This CLI tool cleans those directories to avoid filling the disk by keeping the workspaces of
    the N latest failed jobs, and the M latest successful pipelines.
    """
    app_args = get_app_args()
    pipeline_repo = GitLabPipelineRepo.from_app_args(app_args)

    try:
        clean_fetcher_workspace_pipeline_directories(
            workspace_dir,
            dry_run=app_args.dry_run,
            fetcher_metadata=app_args.fetcher_metadata,
            keep_failed_count=keep_failed_count,
            keep_success_count=keep_success_count,
            pipeline_repo=pipeline_repo,
        )
    except FetcherDefNotFound as exc:
        logger.warning(
            "The provider %r corresponding to the workspace directory %r was not found in fetcher metadata",
            exc.provider_slug,
            format_path(str(workspace_dir)),
        )
