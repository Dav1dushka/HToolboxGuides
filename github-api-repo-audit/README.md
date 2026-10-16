# GitHub API Repo Audit

A small CLI app in development that integrates with the GitHub REST API to summarize public repositories.

## What it does

Given an owner and repository name, it requests public repository metadata and reports:

- description and URL
- visibility and default branch
- stars, forks, and open issue count
- primary language and license (when available)
- creation and last-update timestamps

It only performs a read-only GET request to the public repository endpoint. It does not request credentials, create issues, modify repositories, or access private data.

## Requirements

- Python 3.9+
- No third-party packages

## Usage

From this directory:

```bash
python3 main.py octocat Hello-World
```

Example for this project:

```bash
python3 main.py Dav1dushka HToolboxGuides
```

The GitHub public REST API has rate limits for unauthenticated requests. If the limit is reached, wait and try again. Do not paste access tokens into source code or commit secrets.

## API used

`GET https://api.github.com/repos/{owner}/{repo}`

Documentation: https://docs.github.com/en/rest/repos/repos#get-a-repository

## Project status

Educational prototype. This is an integration-in-development example, not an official GitHub product and not endorsed by GitHub.

## Support

For support, open an issue in this repository. If registering this project for the GitHub Developer Program, provide an email address you monitor for support requests.
