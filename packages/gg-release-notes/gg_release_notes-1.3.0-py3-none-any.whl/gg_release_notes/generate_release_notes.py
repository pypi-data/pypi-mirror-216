import re
from typing import Any, Tuple
import openai

from gg_release_notes.config.env_config import EnvConfig
from gg_release_notes.config.prompt_config import PromptConfig
from gg_release_notes.pull_request import ProdReleasePR


class ReleaseNotes:
    def __init__(
        self,
        env_config: EnvConfig,
        prompt_config: PromptConfig,
        prod_release_pr: ProdReleasePR,
        token_limit: int = 2000,
        **text_generation_params,
    ):
        self.env_config = env_config
        self.prompt_config = prompt_config
        self.prod_release_pr = prod_release_pr
        self.token_limit = token_limit
        self.text_genration_params = text_generation_params
        openai.api_key = env_config.OPENAI_API_KEY
        openai.organization = env_config.OPENAI_API_ORG

    def generate_release_notes(self, prompt: str) -> Any:
        """Generates release notes based on the issues and PR's in the Prod Release PR.

        Args:
            prompt (str): The prompt to use for the openai API
            prod_release_pr_number (str): The PR number of the prod release PR
        Returns:
            Any: Response object from opeanai API
        """

        combined_release_notes = []
        batched_prompt, prompt_issues_descriptions = self._create_prompt_batches(5)
        for batch in batched_prompt:
            try:
                print(f"Generating Prod Release for: \n{batch}")
                # Assemble github titles for prompt
                prompt = f"{prompt} {','.join(batch)}"
                max_tokens = self.token_limit - len(prompt)
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    max_tokens=max_tokens,
                    temperature=0.7,
                    n=1,
                    **self.text_genration_params,
                )
                combined_release_notes.append(response.get("choices")[0].get("text"))
            except Exception as e:
                print(e)
                continue

        response = (
            "\n\n"
            + self.prompt_config.release_notes_start_text
            + "\n".join(combined_release_notes).strip("\t").strip("  ")
            + "\n\nIncludes the following Pull Requests:\n\n"
            + "\n".join(prompt_issues_descriptions)
            + "\n\nCloses the following issues:\n\n"
            + "\n".join(list(self.prod_release_pr.linked_issues))
            + self.prompt_config.release_notes_end_text
        )
        # Ensure that the response doesn't contain @
        response = response.replace("@", "")
        return response

    def _create_prompt_batches(self, batch_size: int) -> Tuple[list, list]:
        """Creates batches of issues to be used in the prompt for the openai API.

        Args:
            prod_release_pr_number (str): The PR number of the prod release PR

        Returns:
            Tuple[list, list]: Tuple of List of batches of issues to be used in the prompt for the openai API.
        """
        prompt_issues_descriptions = list(
            set(
                [
                    "\n" + f"#{''.join(issue_num)}" + issue_title
                    for issue_title, issue_num in self.prod_release_pr.request_pr_commits()
                ]
            )
        )
        # Cleanup prompt with using regex and replace
        prompt_issues_descriptions = [
            issue.replace(
                re.findall("Merge pull request #.* from", issue)[0], ""
            ).strip()
            for issue in prompt_issues_descriptions
        ]

        # batch prompt to avoid 4000 token limit
        batched_prompt = [
            prompt_issues_descriptions[i : i + batch_size]
            for i in range(0, len(prompt_issues_descriptions), batch_size)
        ]
        return batched_prompt, prompt_issues_descriptions

    def create_release_notes(self) -> dict:
        """Creates release notes for all configurations in self.prompt_config.prompt_config for PR self.prod_release_pr.issue_num.

        Returns:
            dict: Dictionary of release notes for all configurations in self.prompt_config.prompt_config for PR self.prod_release_pr.issue_num.
                  Keys are the prompt keys and values are the release notes.
        """
        return {
            prompt_key: {"prompt": prompt, "response": response}
            for prompt_key, response, prompt in [
                [key, self.generate_release_notes(prompt), prompt]
                for key, prompt in self.prompt_config.prompt_config.items()
            ]
        }
