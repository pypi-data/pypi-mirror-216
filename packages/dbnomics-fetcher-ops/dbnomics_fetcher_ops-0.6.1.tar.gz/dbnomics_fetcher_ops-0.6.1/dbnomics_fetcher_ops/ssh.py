import subprocess
import tempfile
from pathlib import Path
from typing import Tuple


def generate_ssh_key_pair(provider_slug: str) -> Tuple[str, str]:
    with tempfile.NamedTemporaryFile(prefix="_" + provider_slug) as tmpfile:
        private_key_path = Path(tmpfile.name)
    subprocess.run(
        [
            "ssh-keygen",
            "-f",
            str(private_key_path),
            "-t",
            "rsa",
            "-C",
            f"{provider_slug}-fetcher@localhost",
            "-b",
            "4096",
            "-N",
            "",
        ],
        check=True,
    )
    public_key_path = private_key_path.with_suffix(".pub")
    public_key = public_key_path.read_text()
    public_key_path.unlink()
    private_key = private_key_path.read_text()
    private_key_path.unlink()
    return (public_key, private_key)
