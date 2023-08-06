from dataclasses import dataclass


class FetcherDefNotFound(Exception):
    def __init__(self, provider_slug: str):
        self.provider_slug = provider_slug
        super().__init__(f"Could not find fetcher definition for provider {provider_slug!r}")


@dataclass
class PipelineVersionError(Exception):
    known_versions: list[str]
    version: str


@dataclass
class UnsupportedModelVersion(Exception):
    expected: int
    found: int
