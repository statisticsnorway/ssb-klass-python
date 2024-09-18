# Project setup

## Regenerate documentation into .rst files
```bash
poetry run sphinx-apidoc -T -f -t ./docs/templates -o ./docs ./src
```
Remove "types" from requests-modules after?

## Poetry venv
Installing the dev-dependencies in a new environment can be done with the following command:
```bash
poetry install --with dev
ssb-project build
```

## Pre-commit install
You're gonna have to install the pre-commit hooks locally to have them run on git commits.
```bash
poetry run pre-commit install
```

## Configuration
pflake8 has its config in pyproject.toml, not in .flake8


# Running stuff locally
## Running the pre-commit hooks locally
```bash
poetry run pre-commit run --all-files
```
Several of the pre-commit hooks will "fail" when they modify files. Re-running the commit after it fails might therefore result in a different result the second time.

## Pytest suites
```bash
poetry run pytest
```


## Pytest coverage
```bash
poetry run pytest --cov=statbank --cov-report term-missing
```
Run this when developing tests.
If you achieve a higher testing coverage make sure to increase the threshold in the workflow.
.github/workflows/test_push.yml
(at the bottom)


## Type-checking with Mypy
```bash
poetry run mypy .
```


# Publish new version of package to Pypi

The action to publish to Pypi is connected with a workflow to releases from Github.
So to publish to Pypi, make sure everything is done on current branch, use bump2version tool to bump version, do a PR into main.
When the PR is merged the github action should push the updated package to Pypi.

## Bump version
```bash
poetry run bump2version patch
```
patch: 0.0.1 -> 0.0.2 \
minor: 0.0.1 -> 0.1.0 \
major: 0.0.1 -> 1.0.0
