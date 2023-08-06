# GPT Release Notes

## Requirements
- .env file -> .env 
- python packages requirements.txt
- OPTIONAL - requirements-test.txt
- Github Repository
- OPENAI account

## pip installation
`pip install gg-release-notes`

## Installation
`python3 -m pip install -r requirements.txt`

## Dev installation
`python3 -m pip install -r dev.requirements.txt`


## Usage

### Example python script
```python
from release_notes.config.env_config import EnvConfig
from release_notes.config.github_config import GithubAPIConfig
from release_notes.config.prompt_config import PromptConfig

from release_notes.pull_request import ProdReleasePR
from release_notes.version import ReleaseVersion
from release_notes.generate_release_notes import ReleaseNotes

from release_notes.upload import UploadRelease, upload_release_notes


config = EnvConfig(".env")
github_api = GithubAPIConfig("DataWiz40", "gg-release-example", config)
prompt_config = PromptConfig(github_api)

prod_release_pr = ProdReleasePR(github_api)
release_version = ReleaseVersion(github_api)

release_notes_instance = ReleaseNotes(
    env_config=config, prompt_config=prompt_config, prod_release_pr=prod_release_pr
)

if __name__ == "__main__":
    generated_release_notes = release_notes_instance.create_release_notes()
    chosen_release = generated_release_notes.get("internal_release").get("response")
    upload_instance = UploadRelease(
        github_config=github_api,
        env_config=config,
        prod_release_pr=prod_release_pr,
        prod_release_version=release_version,
        release_notes_text=chosen_release,
    )
    upload_release_notes(
        prod_release_pr.issue_num, upload_instance, make_github_release=True
    )

```
### Example Github Actions workflow

```yaml
name: Generate Release notes

on:
  pull_request:
    types: [labeled]
    branches:
      - main
  workflow_dispatch:

jobs:
  test-release-notes:
    if: ${{ github.event.label.name == 'prod-release' }}
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8"]
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python3 -m pip install --upgrade pip
          python3 -m pip install -r requirements.txt

      - name: Decode base64 env
        run: echo ${{ secrets.INSERT_SECRETS_KEY }} | base64 --decode > .env

      - name: Generate Release Notes
        run: python3 ./path_to_script.py
```
