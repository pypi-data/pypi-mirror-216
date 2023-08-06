from dataclasses import dataclass
from typing import Protocol


@dataclass
class PipelinesByStatus:
    failed: list[int]
    running: list[int]
    success: list[int]


class PipelineRepo(Protocol):
    def fetch_pipelines_to_keep(
        self, provider_slug: str, *, keep_failed_count: int, keep_success_count: int
    ) -> PipelinesByStatus:
        ...
