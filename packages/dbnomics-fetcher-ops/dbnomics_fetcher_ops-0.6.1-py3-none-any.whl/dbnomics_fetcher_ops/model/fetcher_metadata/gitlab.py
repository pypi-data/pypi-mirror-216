from typing import Dict, Optional, Tuple

from pydantic import BaseModel, Field, HttpUrl, validator

from dbnomics_fetcher_ops.model.fetcher_metadata.base import FetcherMetadata


class ProjectRef(BaseModel):
    group: str
    name: str
    env: Dict[str, str] = Field(default_factory=dict)
    fork_from: Optional[str] = None

    def expand(self, value: str, provider_slug: str) -> str:
        """Expand the provider slug in the given value."""
        variables = {"PROVIDER_SLUG": provider_slug}
        for k, v in variables.items():
            value = value.replace("{" + k + "}", v)
        return value

    def expand_group_and_name(self, provider_slug: str) -> Tuple[str, str]:
        """Return a tuple with the group name and project name resolved with the given provider slug."""
        return self.expand(self.group, provider_slug), self.expand(self.name, provider_slug)

    def get_path_with_namespace(self, provider_slug: str) -> str:
        namespace_path, project_path = self.expand_group_and_name(provider_slug)
        return f"{namespace_path}/{project_path}"


class GitLabStructure(BaseModel):
    base_url: HttpUrl
    fetcher: ProjectRef
    json_data: ProjectRef
    source_data: ProjectRef

    @validator("base_url")
    def trim_end_slash(cls, v):
        return v.rstrip("/")

    def get_http_clone_url(self, provider_slug: str, *, project_ref: ProjectRef) -> str:
        path_with_namespace = project_ref.get_path_with_namespace(provider_slug)
        return f"{self.base_url}/{path_with_namespace}.git"


class GitLabFetcherMetadata(FetcherMetadata):
    gitlab: GitLabStructure
