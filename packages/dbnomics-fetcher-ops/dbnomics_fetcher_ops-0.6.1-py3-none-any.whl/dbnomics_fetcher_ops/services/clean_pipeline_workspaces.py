import shutil
from pathlib import Path
from typing import Optional

import daiquiri
from humanfriendly import format_path, format_size

from dbnomics_fetcher_ops.file_utils import get_directory_size, iter_child_directories
from dbnomics_fetcher_ops.format_utils import format_dir_path_with_size
from dbnomics_fetcher_ops.model.fetcher_metadata.base import FetcherMetadata
from dbnomics_fetcher_ops.model.pipeline_repo.protocol import PipelineRepo, PipelinesByStatus

logger = daiquiri.getLogger(__name__)

DEFAULT_KEEP_FAILED_COUNT = 3
DEFAULT_KEEP_SUCCESS_COUNT = 1


def clean_fetcher_workspace_pipeline_directories(
    workspace_dir: Path,
    *,
    dry_run: bool = False,
    fetcher_metadata: FetcherMetadata,
    keep_failed_count: int = DEFAULT_KEEP_FAILED_COUNT,
    keep_success_count: int = DEFAULT_KEEP_SUCCESS_COUNT,
    pipeline_repo: PipelineRepo,
) -> Optional[int]:
    provider_slug = workspace_dir.name

    fetcher_def = fetcher_metadata.find_fetcher_def_by_provider_slug(provider_slug)
    provider_code = fetcher_def.provider_code

    pipelines_to_keep = pipeline_repo.fetch_pipelines_to_keep(
        provider_slug, keep_failed_count=keep_failed_count, keep_success_count=keep_success_count
    )
    logger.debug("Keeping pipeline directories of fetcher %r: %r", provider_code, pipelines_to_keep)

    reclaimed_bytes = 0
    for pipeline_dir in sorted(iter_child_directories(workspace_dir / "pipelines", warn_other=True)):
        pipeline_dir_size = clean_fetcher_workspace_pipeline_directory(
            pipeline_dir, dry_run=dry_run, pipelines_to_keep=pipelines_to_keep
        )
        if pipeline_dir_size is not None:
            reclaimed_bytes += pipeline_dir_size

    if reclaimed_bytes:
        logger.info(
            "Reclaimed %s in workspace directory %r",
            format_size(reclaimed_bytes, binary=True),
            format_path(str(workspace_dir)),
        )

    return reclaimed_bytes


def clean_fetcher_workspace_pipeline_directory(
    pipeline_dir: Path, *, dry_run: bool = False, pipelines_to_keep: PipelinesByStatus
) -> Optional[int]:
    try:
        pipeline_id = int(pipeline_dir.name)
    except ValueError:
        logger.warning(
            "Ignoring sub-directory %r of workspace directory that does not seem to be a pipeline ID",
            format_path(str(pipeline_dir)),
        )
        return None

    if pipeline_id in pipelines_to_keep.running:
        logger.debug(
            "Keeping pipeline directory %r because the pipeline is running",
            format_path(str(pipeline_dir)),
        )
        return None

    if pipeline_id in pipelines_to_keep.success:
        logger.debug(
            "Keeping pipeline directory %r because the pipeline is one of the successful pipelines to keep",
            format_path(str(pipeline_dir)),
        )
        return None

    if pipeline_id in pipelines_to_keep.failed:
        logger.debug(
            "Keeping pipeline directory %r because the pipeline is one of the failed pipelines to keep",
            format_path(str(pipeline_dir)),
        )
        return None

    pipeline_dir_size = get_directory_size(pipeline_dir)
    dir_path_with_size = format_dir_path_with_size(pipeline_dir, size=pipeline_dir_size)

    if dry_run:
        logger.info(
            "[SKIPPED (dry-run)] The directory %s would have been deleted (unknown size)",
            dir_path_with_size,
        )
    else:
        shutil.rmtree(pipeline_dir)
        logger.info("The directory %s was deleted", dir_path_with_size)

    return pipeline_dir_size
