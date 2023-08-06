from pathlib import Path
from typing import Any

import daiquiri
import requests
import validators
import yaml

from dbnomics_fetcher_ops.model.fetcher_metadata.gitlab import GitLabFetcherMetadata
from dbnomics_fetcher_ops.model.pipelines_config import PipelinesConfig

__all__ = ["load_fetchers_yml", "load_pipelines_yml"]

logger = daiquiri.getLogger(__name__)


def load_bytes(source: str) -> bytes:
    """Load ``source`` which can be a file path or an URL."""
    if validators.url(source):
        response = requests.get(source)
        response.raise_for_status()
        return response.content

    # Assume it is a file if it's not an URL.
    return Path(source).read_bytes()


def load_fetchers_yml(fetchers_yml_ref: str) -> GitLabFetcherMetadata:
    logger.debug("Loading fetcher metadata from %s...", fetchers_yml_ref)
    fetchers_yml_data = load_yml_file(fetchers_yml_ref)
    return GitLabFetcherMetadata.parse_obj(fetchers_yml_data)


def load_pipelines_yml(pipelines_yml_ref: str) -> PipelinesConfig:
    logger.debug("Loading pipelines config from %s...", pipelines_yml_ref)
    pipelines_yml_data = load_yml_file(pipelines_yml_ref)
    return PipelinesConfig.parse_obj(pipelines_yml_data)


def load_yml_file(ref: str) -> Any:
    text = load_bytes(ref)
    return yaml.safe_load(text)
