"""Run fetcher pipeline, the CLI command."""

from typing import Optional

import typer

from dbnomics_fetcher_ops.app_args import get_app_args
from dbnomics_fetcher_ops.services.run_fetcher_pipeline import run_fetcher_pipeline


def run(
    json_data_from_git: bool = typer.Option(False, envvar="JSON_DATA_FROM_GIT"),
    json_data_pipeline_id: Optional[int] = typer.Option(None, envvar="JSON_DATA_PIPELINE_ID"),
    provider_slug: str = typer.Option(..., envvar="PROVIDER_SLUG"),
    source_data_from_git: bool = typer.Option(False, envvar="SOURCE_DATA_FROM_GIT"),
    source_data_pipeline_id: Optional[int] = typer.Option(None, envvar="SOURCE_DATA_PIPELINE_ID"),
    start_from: Optional[str] = typer.Option(None, envvar="START_FROM"),
):
    """Run a pipeline for a fetcher, with options."""
    app_args = get_app_args()
    if app_args.gitlab_private_token is None:
        raise typer.BadParameter("GitLab private token must be given")

    run_fetcher_pipeline(
        provider_slug,
        debug_gitlab=app_args.debug_gitlab,
        dry_run=app_args.dry_run,
        fetcher_metadata=app_args.fetcher_metadata,
        gitlab_private_token=app_args.gitlab_private_token,
        json_data_from_git=json_data_from_git,
        json_data_pipeline_id=json_data_pipeline_id,
        source_data_from_git=source_data_from_git,
        source_data_pipeline_id=source_data_pipeline_id,
        start_from=start_from,
    )
