import logging
from pathlib import Path
from typing import Iterator, Optional, Set

import typer

from dbnomics_fetcher_ops.app_args import get_app_args
from dbnomics_fetcher_ops.file_utils import iter_child_directories
from dbnomics_fetcher_ops.model.fetcher_metadata.base import FetcherMetadata
from dbnomics_fetcher_ops.model.fetcher_metadata.gitlab import GitLabFetcherMetadata
from dbnomics_fetcher_ops.model.pipelines_config import PipelinesConfig

from .configure import UnsupportedPipelineVersion, configure_fetcher
from .undeploy import undeploy_fetcher

logger = logging.getLogger(__name__)


def apply(
    git_repositories_root_dir: Optional[Path] = typer.Option(
        None,
        envvar="GIT_REPOSITORIES_ROOT_DIR",
        help="Directory where the fetcher pipeline keeps clones of the source-data and json-data Git repositories",
    ),
    solr_url: Optional[str] = typer.Option(None, envvar="SOLR_URL"),
    workspaces_root_dir: Optional[Path] = typer.Option(
        None,
        envvar="WORKSPACES_ROOT_DIR",
        help="Directory where the fetcher pipeline writes data to, during download and convert jobs",
    ),
):
    """Configure all fetchers listed in fetchers.yml and undeploy the remaining ones."""
    app_args = get_app_args()
    if app_args.gitlab_private_token is None:
        raise typer.BadParameter("GitLab private token must be given")

    fetcher_metadata = app_args.fetcher_metadata
    pipelines_config = app_args.pipelines_config

    logger.info("Configuring fetchers defined in %r...", app_args.fetchers_yml)
    configure_defined_fetchers(fetcher_metadata, pipelines_config, app_args.debug_gitlab, app_args.gitlab_private_token)

    if workspaces_root_dir is not None:
        logger.info(
            "Undeploying fetchers that are not defined in %r, but did run previously...",
            app_args.fetchers_yml,
        )
        undeploy_remaining_fetchers(
            fetcher_metadata,
            app_args.debug_gitlab,
            app_args.gitlab_private_token,
            solr_url,
            git_repositories_root_dir,
            workspaces_root_dir,
        )


def configure_defined_fetchers(
    fetcher_metadata: GitLabFetcherMetadata,
    pipelines_config: PipelinesConfig,
    debug_gitlab: bool,
    gitlab_private_token: str,
):
    for fetcher_pos, fetcher_def in enumerate(fetcher_metadata.fetchers, start=1):
        logger.info(
            "Configuring fetcher of provider %r (%d/%d)...",
            fetcher_def.provider_code,
            fetcher_pos,
            len(fetcher_metadata.fetchers),
        )
        pipeline_v5_config = pipelines_config.pipeline_versions.v5
        try:
            configure_fetcher(
                fetcher_def,
                debug_gitlab=debug_gitlab,
                fetcher_metadata=fetcher_metadata,
                gitlab_private_token=gitlab_private_token,
                pipeline_v5_config=pipeline_v5_config,
            )
        except UnsupportedPipelineVersion as exc:
            logger.warning(
                "Fetcher %r uses an unsupported pipeline version %r in fetchers.yml, skipping",
                fetcher_def.provider_slug,
                exc.version,
            )


def undeploy_remaining_fetchers(
    fetcher_metadata: GitLabFetcherMetadata,
    debug_gitlab: bool,
    gitlab_private_token: str,
    solr_url: Optional[str],
    git_repositories_root_dir: Optional[Path],
    workspaces_root_dir: Path,
):
    remaining_provider_slugs = get_remaining_provider_slugs(fetcher_metadata, workspaces_root_dir)
    for provider_slug in remaining_provider_slugs:
        undeploy_fetcher(
            provider_slug,
            debug_gitlab=debug_gitlab,
            fetcher_metadata=fetcher_metadata,
            git_repositories_root_dir=git_repositories_root_dir,
            gitlab_private_token=gitlab_private_token,
            solr_url=solr_url,
            workspaces_root_dir=workspaces_root_dir,
        )


def get_remaining_provider_slugs(fetcher_metadata: FetcherMetadata, workspaces_root_dir: Path) -> Set[str]:
    provider_slugs_in_fetchers_yml = {fetcher_def.provider_slug for fetcher_def in fetcher_metadata.fetchers}
    provider_slugs_in_workspace = set(iter_provider_slugs_in_workspace(workspaces_root_dir))
    remaining_provider_slugs = provider_slugs_in_workspace - provider_slugs_in_fetchers_yml
    logger.debug("Found %d remaining fetchers: %r", len(remaining_provider_slugs), remaining_provider_slugs)
    return remaining_provider_slugs


def iter_provider_slugs_in_workspace(workspaces_root_dir: Path) -> Iterator[str]:
    for child_dir in iter_child_directories(workspaces_root_dir):
        yield child_dir.name
