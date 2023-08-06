#! /usr/bin/env python3

"""CLI to manage DBnomics fetchers."""


import logging
from typing import Optional

import daiquiri
import typer

from . import app_args, commands, loaders
from .cli_utils import load_config_from_dotenv

logger = daiquiri.getLogger(__name__)

daiquiri.setup()
daiquiri.set_default_log_levels([(__package__, logging.INFO)])

# Do this before calling os.getenv().
load_config_from_dotenv()


app = typer.Typer()
app.command(name="apply")(commands.apply)
app.command(name="clean-workspace")(commands.clean_workspace)
app.command(name="clean-workspaces")(commands.clean_workspaces)
app.command(name="configure")(commands.configure)
app.command(name="list")(commands.list_)
app.command(name="prune")(commands.prune)
app.command(name="retry")(commands.retry)
app.command(name="run")(commands.run)
app.command(name="undeploy")(commands.undeploy)


@app.callback(context_settings={"help_option_names": ["-h", "--help"]})
def main_callback(
    debug: bool = typer.Option(False, "-d", "--debug", envvar="DEBUG", help="Display DEBUG log messages"),
    debug_gitlab: bool = typer.Option(False, help="Show logging debug messages of Python GitLab"),
    dry_run: bool = typer.Option(False, "-n", "--dry-run", envvar="DRY_RUN", help="Do not execute actions for real"),
    fetchers_yml: str = typer.Option(..., envvar="FETCHERS_YML", help="Path or URL to fetchers.yml"),
    gitlab_private_token: Optional[str] = typer.Option(
        None, envvar="GITLAB_PRIVATE_TOKEN", help="Private access token used to authenticate to GitLab API"
    ),
    pipelines_yml: str = typer.Option(..., envvar="PIPELINES_YML", help="Path or URL to pipelines.yml"),
    verbose: bool = typer.Option(False, "-v", "--verbose", envvar="VERBOSE", help="Display INFO log messages"),
):
    """Manage DBnomics fetchers."""
    daiquiri.set_default_log_levels(
        [(__package__, logging.DEBUG if debug else logging.INFO if verbose else logging.WARNING)]
    )

    fetcher_metadata = loaders.load_fetchers_yml(fetchers_yml)
    pipelines_config = loaders.load_pipelines_yml(pipelines_yml)

    app_args._app_args = app_args.AppArgs(
        debug=debug,
        debug_gitlab=debug_gitlab,
        dry_run=dry_run,
        fetcher_metadata=fetcher_metadata,
        fetchers_yml=fetchers_yml,
        gitlab_private_token=gitlab_private_token,
        pipelines_config=pipelines_config,
        pipelines_yml=pipelines_yml,
        verbose=verbose,
    )


if __name__ == "__main__":
    app()
