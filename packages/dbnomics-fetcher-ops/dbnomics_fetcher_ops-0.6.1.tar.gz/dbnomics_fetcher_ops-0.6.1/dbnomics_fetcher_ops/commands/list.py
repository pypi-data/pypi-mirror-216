from typing import List

import typer

from dbnomics_fetcher_ops.app_args import get_app_args
from dbnomics_fetcher_ops.model.validators import PipelineVersionError, validate_pipeline_version


def list_(
    slug: bool = typer.Option(False, help="Print fetcher slug instead of code"),
    pipeline_versions: List[str] = typer.Option([], "--pipeline-version", help="Filter fetchers by pipeline version"),
):
    """List fetchers.

    Read fetchers from fetchers.yml.

    Useful to build another script based on the output.
    """
    app_args = get_app_args()

    # Validate pipeline versions dynamically because Typer can't take advantage of Literal.
    try:
        for pipeline_version in pipeline_versions:
            validate_pipeline_version(pipeline_version)
    except PipelineVersionError as exc:
        typer.echo(f"Unsupported pipeline version {exc.version!r}, known versions are {exc.known_versions!r}")
        raise typer.Abort()

    for fetcher in app_args.fetcher_metadata.fetchers:
        if pipeline_versions and fetcher.pipeline not in pipeline_versions:
            continue
        if slug:
            typer.echo(fetcher.provider_slug)
        else:
            typer.echo(fetcher.provider_code)
