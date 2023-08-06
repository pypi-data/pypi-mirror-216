from functools import partial
from typing import Dict, List, Literal, Union

from pydantic import BaseModel, Field, validator

from dbnomics_fetcher_ops.model.errors import FetcherDefNotFound
from dbnomics_fetcher_ops.model.validators import check_model_version

DownloadMode = Literal["full", "incremental"]
LabelValue = Union[str, int, float]
PipelineVersion = Literal["v1", "v2", "v5"]
ProviderCode = str
UpdateStrategy = Literal["merge", "replace"]


class ScheduleDef(BaseModel):
    cron: str
    owner: str
    timezone: str


class FetcherDef(BaseModel):
    """The definition of a fetcher.

    Pipeline versions are described in [this issue](https://git.nomics.world/dbnomics-fetchers/management/-/issues/948).
    """

    provider_code: ProviderCode
    provider_slug: str
    pipeline: PipelineVersion = "v5"
    category_tree_update_strategy: UpdateStrategy = "merge"
    dataset_update_strategy: UpdateStrategy = "replace"
    download_mode: DownloadMode = "full"
    env: Dict[str, str] = Field(default_factory=dict)
    ignore_managed_files: List[str] = Field(default_factory=list)
    labels: Dict[str, LabelValue] = Field(default_factory=dict)
    schedules: List[ScheduleDef] = Field(default_factory=list)


class FetcherMetadata(BaseModel):
    version: int

    fetchers: List[FetcherDef]

    def find_fetcher_def_by_provider_slug(self, provider_slug: str) -> FetcherDef:
        for fetcher in self.fetchers:
            if fetcher.provider_slug == provider_slug:
                return fetcher
        raise FetcherDefNotFound(provider_slug=provider_slug)

    validator("version", allow_reuse=True)(partial(check_model_version, expected=2))
