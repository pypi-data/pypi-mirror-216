"""Retry failed fetcher pipeline jobs, the application-level service."""


import daiquiri
from gitlab.v4.objects import Project

from dbnomics_fetcher_ops.gitlab_utils import init_gitlab_client
from dbnomics_fetcher_ops.model.fetcher_metadata.gitlab import GitLabFetcherMetadata
from dbnomics_fetcher_ops.model.pipeline_repo.gitlab import GitLabPipelineRepo

__all__ = ["RetryFetcherPipelineJobsService"]

logger = daiquiri.getLogger(__name__)


class RetryFetcherPipelineJobsService:
    def __init__(
        self,
        *,
        debug_gitlab: bool = False,
        dry_run: bool = False,
        fetcher_metadata: GitLabFetcherMetadata,
        gitlab_private_token: str,
    ) -> None:
        self.debug_gitlab = debug_gitlab
        self.dry_run = dry_run
        self.fetcher_metadata = fetcher_metadata
        self.gitlab_private_token = gitlab_private_token

        # Create GitLab client.
        gitlab_url = fetcher_metadata.gitlab.base_url
        self.gl = init_gitlab_client(gitlab_url, enable_debug=debug_gitlab, private_token=gitlab_private_token)

        self.pipeline_repo = GitLabPipelineRepo(fetcher_metadata=fetcher_metadata, gl=self.gl)

    def retry_pipeline_jobs(self, job_names: list[str], *, provider_slug: str) -> None:
        fetcher_project = self._fetch_fetcher_project(provider_slug)
        for job_name in job_names:
            self.retry_pipeline_job(job_name, fetcher_project=fetcher_project)

    def retry_pipeline_job(self, job_name: str, *, fetcher_project: Project) -> None:
        pipeline = self.pipeline_repo.fetch_latest_pipeline(fetcher_project)
        if pipeline is None:
            logger.debug("No pipeline found for %r", fetcher_project.path_with_namespace)
            return

        logger.debug(
            "Retrying the job %r of the latest pipeline %r of %r",
            job_name,
            pipeline,
            fetcher_project.path_with_namespace,
        )
        job = next((job for job in pipeline.jobs.list() if job.name == job_name), None)
        if job is None:
            logger.debug(
                "No job named %r was found in %r of %r", job_name, pipeline, fetcher_project.path_with_namespace
            )
            return

        if job.status != "failed":
            logger.debug(
                "Job %r was found in %r of %r but refusing to retry it since it did not fail",
                job,
                pipeline,
                fetcher_project.path_with_namespace,
            )
            return

        if self.dry_run:
            logger.info(
                "[SKIPPED (dry-run)] The job %r of the latest pipeline %r of %r would have been retried",
                job,
                pipeline,
                fetcher_project.path_with_namespace,
            )
        else:
            project_job = fetcher_project.jobs.get(job.id, lazy=True)
            new_job_attributes = project_job.retry()
            logger.info(
                "Triggered retry of job %r of the latest pipeline %r of %r: %s",
                job,
                pipeline,
                fetcher_project.path_with_namespace,
                new_job_attributes["web_url"],
            )

    def _fetch_fetcher_project(self, provider_slug: str) -> Project:
        project_ref = self.fetcher_metadata.gitlab.fetcher
        project_path_with_namespace = project_ref.get_path_with_namespace(provider_slug)
        return self.gl.projects.get(project_path_with_namespace)
