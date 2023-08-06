import re
import subprocess
from pathlib import Path
from typing import Iterator, Optional

import daiquiri
from humanfriendly import format_path

logger = daiquiri.getLogger(__name__)


def get_directory_size(directory: Path) -> Optional[int]:
    output = subprocess.check_output(["/usr/bin/du", "-sb", str(directory)])
    match = re.match(rb"^(\d+)", output)
    if match is None:
        return None
    return int(match.group(1))


def iter_child_directories(directory: Path, *, warn_other: bool = False) -> Iterator[Path]:
    """Iterate over child directories of a directory."""
    for child in directory.iterdir():
        if child.is_dir():
            yield child
        elif warn_other:
            logger.warning("Ignoring %r because it is not a directory", format_path(str(child)))
