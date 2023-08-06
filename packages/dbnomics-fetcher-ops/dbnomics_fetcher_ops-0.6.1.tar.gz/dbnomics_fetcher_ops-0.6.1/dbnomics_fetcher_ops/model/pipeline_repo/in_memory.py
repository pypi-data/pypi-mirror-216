import random
from itertools import islice

from dbnomics_fetcher_ops.model.pipeline_repo.protocol import PipelinesByStatus


class InMemoryPipelineRepo:
    def __init__(self, pipelines_by_provider_slug: dict[str, PipelinesByStatus]):
        self._pipelines_by_provider_slug = pipelines_by_provider_slug

    def fetch_pipelines_to_keep(
        self, provider_slug: str, *, keep_failed_count: int, keep_success_count: int
    ) -> PipelinesByStatus:
        provider_pipelines = self._pipelines_by_provider_slug[provider_slug]
        return PipelinesByStatus(
            failed=list(islice(provider_pipelines.failed, keep_failed_count)),
            running=provider_pipelines.running,
            success=list(islice(provider_pipelines.success, keep_success_count)),
        )


def generate_provider_pipelines(
    *, failed_count: int, provider_slugs: list[str], running_count: int, success_count: int
) -> dict[str, PipelinesByStatus]:
    return {
        provider_slug: PipelinesByStatus(
            failed=generate_pipeline_ids(failed_count),
            running=generate_pipeline_ids(running_count),
            success=generate_pipeline_ids(success_count),
        )
        for provider_slug in provider_slugs
    }


def generate_pipeline_ids(count: int) -> list[int]:
    return random.sample(range(100_000), count)
