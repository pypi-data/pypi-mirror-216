import os
from genericparser.plugins.domain.generic_class import GenericStaticABC
import requests


class ParserGithub(GenericStaticABC):
    token = "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"

    def _make_request(self, url, token):
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            print("error making request to github api in url: ", url, e)
        return response.json() if response.status_code == 200 else {}

    # Get statistics metrics functions
    def _get_statistics_weekly_code_frequency(self, base_url, token):
        values = [0] * 7
        metrics = [
            "commits_on_sunday",
            "commits_on_monday",
            "commits_on_tuesday",
            "commits_on_wednesday",
            "commits_on_thursday",
            "commits_on_friday",
            "commits_on_saturday",
        ]
        url = f"{base_url}/stats/punch_card"
        response = self._make_request(url, token)
        for commit_count in response or []:
            values[commit_count[0]] += commit_count[2]

        return {"metrics": metrics, "values": values}

    # Get comunity metrics
    def _get_comunity_metrics(self, base_url, token):
        values = []
        metrics = [
            "health_percentage",
            "updated_at",
            "created_at",
            "watchers_count",
            "forks_count",
            "open_issues_count",
            "forks",
            "open_issues",
            "watchers",
            "subscribers_count",
            "size",
        ]
        url = f"{base_url}/community/profile"
        response = {
            **self._make_request(base_url, token),
            **self._make_request(url, token),
        }
        for metric in metrics:
            values.append(response.get(metric, None))

        return {"metrics": metrics, "values": values}

    # Get statistics metrics
    def _get_statistics_metrics(self, base_url, token):
        return {
            **self._get_statistics_weekly_code_frequency(base_url, token),
        }

    def extract(self, input_file):
        token_from_github = (
            input_file.get("token", None)
            if type(input_file) == dict
            else None or os.environ.get("GITHUB_TOKEN", None) or self.token
        )
        repository = (
            input_file.get("repository", None)
            if (type(input_file) == dict)
            else input_file
        )
        metrics = []
        keys = repository
        values = []
        owner, repository_name = repository.split("/")
        url = f"https://api.github.com/repos/{owner}/{repository_name}"

        # Get comunity metrics
        return_of_comunity_metrics = self._get_comunity_metrics(url, token_from_github)
        metrics.extend(return_of_comunity_metrics["metrics"])
        values.extend(return_of_comunity_metrics["values"])

        # Get statistics metrics
        return_of_statistics_metrics = self._get_statistics_metrics(
            url, token_from_github
        )
        metrics.extend(return_of_statistics_metrics["metrics"])
        values.extend(return_of_statistics_metrics["values"])

        return {"metrics": metrics, "values": values, "file_paths": keys}


def main():
    return ParserGithub()
