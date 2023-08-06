from pathlib import Path
from typing import Optional

from humanfriendly import format_path, format_size

from dbnomics_fetcher_ops.file_utils import get_directory_size


def format_dir_path_with_size(directory: Path, *, size: Optional[float] = None) -> str:
    path_str = f"{format_path(str(directory))!r}"
    if size is None:
        size = get_directory_size(directory)
    size_str = format_size(size, binary=True) if size is not None else "unknown size"
    return f"{path_str} ({size_str})"
