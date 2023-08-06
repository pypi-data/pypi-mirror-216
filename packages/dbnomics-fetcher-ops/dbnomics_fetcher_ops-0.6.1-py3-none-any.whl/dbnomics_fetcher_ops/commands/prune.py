"""Prune CLI command."""

from typing import Optional

import typer

from dbnomics_fetcher_ops.app_args import AppArgs, get_app_args
from dbnomics_fetcher_ops.services.prune_fetcher import PruneService


def prune(
    json_data_deploy_key: Optional[str] = typer.Option(
        None, help="Delete the deploy key with this title in the json-data project"
    ),
    provider_slug: Optional[str] = typer.Option(
        None,
        envvar="PROVIDER_SLUG",
        help="Delete GitLab objects for this provider only, otherwise process all providers",
    ),
    source_data_deploy_key: Optional[str] = typer.Option(
        None, help="Delete the deploy key with this title in the source-data project"
    ),
):
    """Prune GitLab objects from fetcher, source-data or json-data projects."""
    app_args = get_app_args()
    if app_args.gitlab_private_token is None:
        raise typer.BadParameter("GitLab private token must be given")

    if all(v is None for v in [json_data_deploy_key, source_data_deploy_key]):
        raise typer.BadParameter("Please specify at least one GitLab object to prune (e.g. --source-data-deploy-key)")

    prune_service = PruneService(
        debug_gitlab=app_args.debug_gitlab,
        dry_run=app_args.dry_run,
        fetcher_metadata=app_args.fetcher_metadata,
        gitlab_private_token=app_args.gitlab_private_token,
        json_data_deploy_key=json_data_deploy_key,
        source_data_deploy_key=source_data_deploy_key,
    )

    provider_slugs = [provider_slug] if provider_slug is not None else load_provider_slugs(app_args)
    for provider_slug in provider_slugs:
        prune_service.prune_fetcher(provider_slug)


def load_provider_slugs(app_args: AppArgs) -> list[str]:
    return [fetcher.provider_slug for fetcher in app_args.fetcher_metadata.fetchers]
