"""Prune fetcher, the application-level service."""


import daiquiri
from gitlab.v4.objects import Project

from dbnomics_fetcher_ops.gitlab_utils import init_gitlab_client
from dbnomics_fetcher_ops.model.fetcher_metadata.gitlab import GitLabFetcherMetadata

__all__ = ["PruneService"]

logger = daiquiri.getLogger(__name__)


class PruneService:
    def __init__(
        self,
        *,
        debug_gitlab: bool = False,
        dry_run: bool = False,
        fetcher_metadata: GitLabFetcherMetadata,
        gitlab_private_token: str,
        json_data_deploy_key: str | None,
        source_data_deploy_key: str | None,
    ) -> None:
        self.debug_gitlab = debug_gitlab
        self.dry_run = dry_run
        self.fetcher_metadata = fetcher_metadata
        self.gitlab_private_token = gitlab_private_token
        self.json_data_deploy_key = json_data_deploy_key
        self.source_data_deploy_key = source_data_deploy_key

        # Create GitLab client.
        gitlab_url = fetcher_metadata.gitlab.base_url
        self.gl = init_gitlab_client(gitlab_url, enable_debug=debug_gitlab, private_token=gitlab_private_token)

    def prune_fetcher(self, provider_slug: str) -> None:
        if self.json_data_deploy_key is not None:
            project_path_with_namespace = self.fetcher_metadata.gitlab.json_data.get_path_with_namespace(provider_slug)
            project = self.gl.projects.get(project_path_with_namespace)
            self._delete_deploy_key(self.json_data_deploy_key, project=project)
        if self.source_data_deploy_key is not None:
            project_path_with_namespace = self.fetcher_metadata.gitlab.source_data.get_path_with_namespace(
                provider_slug
            )
            project = self.gl.projects.get(project_path_with_namespace)
            self._delete_deploy_key(self.source_data_deploy_key, project=project)

    def _delete_deploy_key(self, title: str, *, project: Project) -> None:
        logger.debug("Deleting the deploy key %r from %r...", title, project.path_with_namespace)
        key = next((key for key in project.keys.list() if key.title == title), None)
        if key is None:
            logger.debug("No deploy key with title %r found for %r", title, project.path_with_namespace)
            return

        if self.dry_run:
            logger.info("[SKIPPED (dry-run)] %r would have been deleted from %r", key, project.path_with_namespace)
        else:
            key.delete()
            logger.info("%r deleted from %r", key, project.path_with_namespace)
