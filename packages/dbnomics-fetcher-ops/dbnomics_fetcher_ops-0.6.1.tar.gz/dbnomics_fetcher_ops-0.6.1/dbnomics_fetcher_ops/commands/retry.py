"""Retry CLI command."""

from typing import Optional

import typer

from dbnomics_fetcher_ops.app_args import AppArgs, get_app_args
from dbnomics_fetcher_ops.services.retry_fetcher_pipeline_job import RetryFetcherPipelineJobsService


def retry(
    all_providers: bool = typer.Option(False, help="Retry jobs for all the providers"),
    job_names: list[str] = typer.Option(..., "--job", help="Name of the job to retry"),
    provider_slug: Optional[str] = typer.Option(
        None,
        envvar="PROVIDER_SLUG",
        help="Delete GitLab objects for this provider only, otherwise process all providers",
    ),
):
    """Retry failed jobs of the latest pipeline of a fetcher."""
    app_args = get_app_args()
    if app_args.gitlab_private_token is None:
        raise typer.BadParameter("GitLab private token must be given")

    if (provider_slug is None) == (not all_providers):
        raise typer.BadParameter("Use one of the options: --all-providers, --provider-slug")

    retry_service = RetryFetcherPipelineJobsService(
        debug_gitlab=app_args.debug_gitlab,
        dry_run=app_args.dry_run,
        fetcher_metadata=app_args.fetcher_metadata,
        gitlab_private_token=app_args.gitlab_private_token,
    )

    provider_slugs = [provider_slug] if provider_slug is not None else load_provider_slugs(app_args)
    for provider_slug in provider_slugs:
        retry_service.retry_pipeline_jobs(job_names, provider_slug=provider_slug)


def load_provider_slugs(app_args: AppArgs) -> list[str]:
    return [fetcher.provider_slug for fetcher in app_args.fetcher_metadata.fetchers]
