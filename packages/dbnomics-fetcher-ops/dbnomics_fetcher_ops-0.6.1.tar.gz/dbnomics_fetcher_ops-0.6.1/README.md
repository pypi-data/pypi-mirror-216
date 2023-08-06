# DBnomics fetcher ops

Manage DBnomics fetchers: list, configure and run pipelines.

## Install

```bash
pip install dbnomics-fetcher-ops[cli]
```

## Usage

### Configure a fetcher

The configure command needs write privileges. Create a GitLab [personal access token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) having the `api` scope, and pass it using the `--gitlab-private-token` option or the `GITLAB_PRIVATE_TOKEN` environment variable in `~/.config/dbnomics/dbnomics-fetchers.env`.

```bash
dbnomics-fetchers -v configure scsmich --dry-run
# If everything seems OK, remove the --dry-run flag:
dbnomics-fetchers -v configure scsmich
```

### List fetchers

```bash
dbnomics-fetchers -v list
```

### Run fetcher pipelines

```bash
# Replace PROVIDER_SLUG by the real value:
dbnomics-fetchers -v run --provider-slug PROVIDER_SLUG

# To run a pipeline for each fetcher:
dbnomics-fetchers -v list --slug | xargs -I {} dbnomics-fetchers -v run --provider-slug {}
```

## Development

Install [Poetry](https://python-poetry.org/).

```bash
# git clone repo or fork
cd dbnomics-fetcher-ops
poetry install
cp .env.example .env
```

Run commands with:

```bash
poetry shell
dbnomics-fetchers COMMAND
```
