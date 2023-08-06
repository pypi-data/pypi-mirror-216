from ghapi.all import GhApi

from gg_release_notes.config.env_config import EnvConfig


class GithubAPIConfig:
    """Wrapper for Github API"""

    def __init__(self, owner: str, repository: str, env_config: EnvConfig, github_prod_release_label: str = "prod-release"):
        self.owner = owner
        self.repository = repository
        self.github_api = GhApi(
            owner=owner,
            repo=repository,
            token=env_config.ENV_GITHUB_API_TOKEN,
        )
        self.github_prod_release_label = github_prod_release_label
