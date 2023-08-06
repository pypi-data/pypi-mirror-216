from typing import Optional

from gitlab import Gitlab


def init_gitlab_client(
    gitlab_base_url: str, *, private_token: Optional[str] = None, enable_debug: bool = False
) -> Gitlab:
    gl = Gitlab(gitlab_base_url, private_token=private_token, api_version="4")
    if private_token is not None:
        gl.auth()
    if enable_debug:
        gl.enable_debug()
    return gl
