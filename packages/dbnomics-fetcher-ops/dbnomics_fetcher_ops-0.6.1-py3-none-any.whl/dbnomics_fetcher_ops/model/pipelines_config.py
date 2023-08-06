from functools import partial
from typing import List, Literal

from pydantic import BaseModel, validator

from dbnomics_fetcher_ops.model.validators import check_model_version


class FileDef(BaseModel):
    content: str
    if_exists: Literal["keep", "replace"]
    path: str


class PipelineV5ConfigFetcherProject(BaseModel):
    files: List[FileDef]


class PipelineV5Config(BaseModel):
    fetcher_project: PipelineV5ConfigFetcherProject


class PipelineVersions(BaseModel):
    v5: PipelineV5Config


class PipelinesConfig(BaseModel):
    version: int

    pipeline_versions: PipelineVersions

    validator("version", allow_reuse=True)(partial(check_model_version, expected=1))
