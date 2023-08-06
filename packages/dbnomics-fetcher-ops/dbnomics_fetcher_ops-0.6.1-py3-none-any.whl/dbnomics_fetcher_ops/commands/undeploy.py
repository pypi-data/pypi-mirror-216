import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import gitlab
import typer
from dbnomics_solr import DBnomicsSolrClient
from dbnomics_solr.dbnomics_solr_client import ProviderNotFound
from gitlab.v4.objects import Project
from humanfriendly import format_path

from dbnomics_fetcher_ops.app_args import get_app_args
from dbnomics_fetcher_ops.cli_utils import check_provider_slug_is_lowercase, get_fetcher_def_not_found_error_message
from dbnomics_fetcher_ops.gitlab_utils import init_gitlab_client
from dbnomics_fetcher_ops.model.errors import FetcherDefNotFound
from dbnomics_fetcher_ops.model.fetcher_metadata.gitlab import GitLabFetcherMetadata

logger = logging.getLogger(__name__)


def undeploy(
    provider_slug: str = typer.Argument(..., callback=check_provider_slug_is_lowercase),
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
    """Remove data of this provider on a DBnomics instance.

    This command:

    - disables the schedules of the GitLab project of the fetcher
    - deletes all the Solr documents corresponding to this provider
    - deletes the directories used by the fetcher pipeline (source-data and json-data clones, and workspace)

    As a consequence, the provider won't appear on DBnomics website and API anymore.

    This command does not delete:

    - the GitLab project of the source code of the fetcher
    - the GitLab project of "source-data"
    - the GitLab project of "json-data"
    - the "json-data" directory served by the API (this is done by dbnomics-sync-git)
    """
    app_args = get_app_args()
    if app_args.gitlab_private_token is None:
        raise typer.BadParameter("GitLab private token must be given")

    try:
        undeploy_fetcher(
            provider_slug,
            debug_gitlab=app_args.debug_gitlab,
            fetcher_metadata=app_args.fetcher_metadata,
            git_repositories_root_dir=git_repositories_root_dir,
            gitlab_private_token=app_args.gitlab_private_token,
            solr_url=solr_url,
            workspaces_root_dir=workspaces_root_dir,
        )
    except FetcherDefNotFound:
        logger.error(get_fetcher_def_not_found_error_message(provider_slug, app_args.fetchers_yml))
        raise typer.Abort()


def undeploy_fetcher(
    provider_slug: str,
    *,
    debug_gitlab: bool,
    fetcher_metadata: GitLabFetcherMetadata,
    git_repositories_root_dir: Optional[Path],
    gitlab_private_token: str,
    solr_url: Optional[str],
    workspaces_root_dir: Optional[Path],
):
    # Disable GitLab schedules
    disable_schedules(
        provider_slug,
        debug_gitlab=debug_gitlab,
        fetcher_metadata=fetcher_metadata,
        gitlab_private_token=gitlab_private_token,
    )

    # Delete documents from Solr
    if solr_url is not None:
        delete_provider_from_solr(provider_slug, solr_url=solr_url)

    # Delete directories used by the fetcher pipeline
    delete_pipeline_directories(
        provider_slug, git_repositories_root_dir=git_repositories_root_dir, workspaces_root_dir=workspaces_root_dir
    )


def delete_pipeline_directories(
    provider_slug: str, *, git_repositories_root_dir: Optional[Path], workspaces_root_dir: Optional[Path]
):
    if git_repositories_root_dir is not None:
        git_repositories_dir = git_repositories_root_dir / provider_slug
        delete_pipeline_directory(git_repositories_dir)

    if workspaces_root_dir is not None:
        workspace_dir = workspaces_root_dir / provider_slug
        delete_pipeline_directory(workspace_dir)


def delete_pipeline_directory(path: Path):
    if path.is_dir():
        logger.info("Deleting pipeline directory: %r...", format_path(str(path)))
        shutil.rmtree(path)


def delete_provider_from_solr(provider_slug: str, *, solr_url: str):
    dbnomics_solr_client = DBnomicsSolrClient(solr_url)
    provider_code = dbnomics_solr_client.find_provider_code_from_slug(provider_slug)
    logger.debug("Deleting documents related to provider %r from Solr...", provider_code)
    try:
        dbnomics_solr_client.delete_provider_docs(provider_code)
    except ProviderNotFound:
        logger.debug("Provider %r was not found in Solr index, skipping", provider_code)


def disable_schedules(
    provider_slug: str,
    *,
    gitlab_private_token: str,
    debug_gitlab: bool,
    fetcher_metadata: GitLabFetcherMetadata,
):
    logger.debug("Disabling schedules of fetcher %r...", provider_slug)

    # Create GitLab client.
    gitlab_url = fetcher_metadata.gitlab.base_url
    gl = init_gitlab_client(gitlab_url, enable_debug=debug_gitlab, private_token=gitlab_private_token)

    try:
        fetcher_project = load_fetcher_project(gl, fetcher_metadata, provider_slug)
    except GitLabProjectNotFound as exc:
        logger.debug(
            "Could not find project %r for fetcher source code of provider %r, skipping disabling schedules",
            exc.project_path_with_namespace,
            provider_slug,
        )
        return

    for schedule in fetcher_project.pipelineschedules.list(as_list=False):
        logger.info("Deleting schedule %r for project %r", schedule, fetcher_project.path_with_namespace)
        schedule.delete()


@dataclass
class GitLabProjectNotFound(Exception):
    project_path_with_namespace: str


def load_fetcher_project(gl: gitlab.Gitlab, fetcher_metadata: GitLabFetcherMetadata, provider_slug: str) -> Project:
    project_path_with_namespace = fetcher_metadata.gitlab.fetcher.get_path_with_namespace(provider_slug)
    try:
        fetcher_project = gl.projects.get(project_path_with_namespace)
    except gitlab.exceptions.GitlabGetError as exc:
        if exc.response_code != 404:
            raise
        raise GitLabProjectNotFound(project_path_with_namespace=project_path_with_namespace) from exc
    return fetcher_project
