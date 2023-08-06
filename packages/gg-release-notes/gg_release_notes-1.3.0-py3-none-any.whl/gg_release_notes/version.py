from typing import Optional

from ghapi.all import GhApi

from gg_release_notes.config.github_config import GithubAPIConfig


class ReleaseVersion:
    """
    Class for getting and incrementing the version number of the current release in Github.
    """

    def __init__(self, github_configuration: GithubAPIConfig):
        self.github_configuration = github_configuration
        self.github_api: GhApi = github_configuration.github_api

    @property
    def _version_mapping(self) -> dict:
        """Maps the versioning type to the correct incrementation function."""
        return {
            "major": 0,
            "minor": 1,
            "patch": 2,
        }

    @property
    def current_version(self) -> str:
        """Gets the current version number of the release."""
        try:
            release_req = self.github_api.repos.get_latest_release()
            version = release_req.get("tag_name", "1.0.0")
        except:
            # No release exists yet
            version = "1.0.0"
        
        return str(version)

    def increment_version(
        self, current_version: str, versioning_type: Optional[str]
    ) -> str:
        """Increments the version number of the current release."""
        print(f"Current version: {current_version}")
        # Remove the 'v' from the version number
        if current_version.startswith("v."):
            current_version = current_version[2:]
            
        version_parts = list(map(int, current_version.split('.')))
        if str(versioning_type).lower() == 'major':
            version_parts[0] += 1
            version_parts[1], version_parts[2] = 0, 0
        elif str(versioning_type).lower() == 'minor':
            version_parts[1] += 1
            version_parts[2] = 0
        else:
            version_parts[2] += 1
        return '.'.join(map(str, version_parts))
