from dbnomics_fetcher_ops.model.errors import PipelineVersionError, UnsupportedModelVersion


def check_model_version(found: int, *, expected: int):
    if found != expected:
        raise UnsupportedModelVersion(expected=expected, found=found)


def validate_pipeline_version(version: str):
    known_versions = ["v1", "v2", "v5"]
    if version not in known_versions:
        raise PipelineVersionError(known_versions=known_versions, version=version)
