from itertools import islice
from typing import Iterator, cast

from gitlab import Gitlab
from gitlab.v4.objects import Project, ProjectPipeline

from dbnomics_fetcher_ops.app_args import AppArgs
from dbnomics_fetcher_ops.gitlab_utils import init_gitlab_client
from dbnomics_fetcher_ops.model.fetcher_metadata.gitlab import GitLabFetcherMetadata
from dbnomics_fetcher_ops.model.pipeline_repo.protocol import PipelinesByStatus


class GitLabPipelineRepo:
    def __init__(self, *, fetcher_metadata: GitLabFetcherMetadata, gl: Gitlab):
        self._fetcher_metadata = fetcher_metadata
        self._gl = gl

    @classmethod
    def from_app_args(cls, app_args: AppArgs):
        gitlab_base_url = app_args.fetcher_metadata.gitlab.base_url
        gl = init_gitlab_client(
            gitlab_base_url, enable_debug=app_args.debug_gitlab, private_token=app_args.gitlab_private_token
        )
        return cls(fetcher_metadata=app_args.fetcher_metadata, gl=gl)

    def fetch_latest_pipeline(self, project: Project, *, status: str | None = None) -> ProjectPipeline | None:
        return next(self.fetch_latest_pipelines(project, status=status), None)

    def fetch_latest_pipelines(self, project: Project, *, status: str | None = None) -> Iterator[ProjectPipeline]:
        return cast(
            Iterator[ProjectPipeline],
            project.pipelines.list(status=status, order_by="updated_at", sorted="desc", iterator=True),
        )

    def fetch_pipelines_to_keep(
        self, provider_slug: str, *, keep_failed_count: int, keep_success_count: int
    ) -> PipelinesByStatus:
        project = self._fetch_project(provider_slug)
        return self._fetch_pipelines_to_keep(
            project, keep_failed_count=keep_failed_count, keep_success_count=keep_success_count
        )

    def _fetch_pipelines_to_keep(
        self, project: Project, *, keep_failed_count: int, keep_success_count: int
    ) -> PipelinesByStatus:
        return PipelinesByStatus(
            failed=[
                pipeline.id
                for pipeline in islice(self.fetch_latest_pipelines(project, status="failed"), keep_failed_count)
            ],
            running=[pipeline.id for pipeline in self.fetch_latest_pipelines(project, status="running")],
            success=[
                pipeline.id
                for pipeline in islice(self.fetch_latest_pipelines(project, status="success"), keep_success_count)
            ],
        )

    def _fetch_project(self, provider_slug: str) -> Project:
        project_path_with_namespace = self._fetcher_metadata.gitlab.fetcher.get_path_with_namespace(provider_slug)
        return self._gl.projects.get(project_path_with_namespace)
