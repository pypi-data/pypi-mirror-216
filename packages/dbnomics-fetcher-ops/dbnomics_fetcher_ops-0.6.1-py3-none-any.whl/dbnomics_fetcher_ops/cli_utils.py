import daiquiri
from dotenv import load_dotenv
from humanfriendly import format_path
from typer import BadParameter
from xdg import xdg_config_home

logger = daiquiri.getLogger(__name__)


def check_provider_slug_is_lowercase(value: str):
    if value != value.lower():
        raise BadParameter("Provider slug must be lowercase")
    return value


def get_fetcher_def_not_found_error_message(provider_slug: str, fetchers_yml: str) -> str:
    return f"Could not find fetcher definition for provider {provider_slug!r} in {fetchers_yml!r}"


def load_config_from_dotenv() -> None:
    config_env_file = xdg_config_home() / "dbnomics" / "dbnomics-fetchers.env"
    if config_env_file.is_file():
        load_dotenv(config_env_file)
        logger.info("Environment variables loaded from %r", format_path(str(config_env_file)))
    load_dotenv()
