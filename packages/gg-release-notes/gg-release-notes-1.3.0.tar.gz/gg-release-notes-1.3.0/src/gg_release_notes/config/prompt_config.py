from gg_release_notes.version import ReleaseVersion
from gg_release_notes.config.github_config import GithubAPIConfig


class PromptConfig:
    """Prompt configuration used for the GPT generation"""

    def __init__(self, github_config: GithubAPIConfig):
        """s

        Args:
            github_config (GithubAPIConfig): Github configuration
        """
        self.github_config = github_config
        self.release_version = ReleaseVersion(github_config)

    @property
    def prompt_internal_release(self):
        """Prompt for the internal release notes"""
        return f"""Write release notes for internal use in {self.github_config.owner} for the repository {self.github_config.repository}. Make a summary highlighting the most important changes and explaining the impact of the changes."""

    @property
    def release_notes_start_text(self):
        """Start of the release notes, which will be added to the generated release notes"""
        return f"""We are happy to announce the release of {self.github_config.owner}/{self.github_config.repository}!"""

    @property
    def release_notes_end_text(self):
        """End of the release notes, which will be added to the generated release notes"""
        return f""""""

    @property
    def prompt_config(self):
        """Determines which prompt to use for the openai API"""
        return {
            "internal_release": self.prompt_internal_release,
        }
