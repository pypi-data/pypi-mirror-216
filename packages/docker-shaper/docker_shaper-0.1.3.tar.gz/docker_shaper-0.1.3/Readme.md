# Docker Shaper

This repository includes scripts/tools for Checkmk developers.

## Installation

```sh
[<PYTHON> -m] pip[3] install [--user] [--upgrade] docker-shaper
```

## Usage

```
docker-shaper serve`
```
Navigate to e.g. http://build-fra-003:5432/


## Development & Contribution

### Todo

- [x] pip package
- [x] Quart interface
- [ ] bring in dockermon
- [ ] auto update
- [ ] bring in dgcd
- [ ] bring in list_volumes
- [ ] outsource config
- [ ] 	increase/decrease logging
- [ ] new: untag certain tags
- [ ] new: container cleanup


### Setup

### Prerequisites

* Python 3.8.10
* `poetry`
* `pre-commit`


```sh
python3 -m pip install --upgrade --user poetry pre-commit
git clone ssh://review.lan.tribe29.com:29418/checkmk_ci
cd checkmk_ci
pre-commit install
# if you need a specific version of Python inside your dev environment
poetry env use ~/.pyenv/versions/3.8.10/bin/python3
poetry install
```

### Workflow
poetry config repositories.checkmk https://upload.pypi.org/legacy/
poetry config pypi-token.checkmk pypi-

pip3 install --user --upgrade docker-shaper
~/.local/bin/docker-shaper server

poetry run mypy docker_shaper

* (once and only for publishing to PyPi) Get token on PyPi.org
* (once and only for publishing to PyPi) `poetry config pypi-token.pypi pypi-<LONG-STRING>`
  (will write to `~/.config/pypoetry/auth.toml`)
* modify and check commits via `pre-commit`
* after work is done locally:
  - adapt version in `pyproject.toml`
  - build and check a package
```sh
poetry build && \
twine check dist/* &&
python3 -m pip uninstall -y checkmk_dev_tools && \
python3 -m pip install --user dist/checkmk_dev_tools-$(grep -E "^version.?=" pyproject.toml | cut -d '"' -f 2)-py3-none-any.whl
```
  - check installed package
  - go through review process
  - publish the new package `poetry publish --build --repository checkmk`
  - commit new version && push


## Knowledge
https://github.com/torfsen/python-systemd-tutorial
https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application
* https://blog.miguelgrinberg.com/post/beautiful-interactive-tables-for-your-flask-templates
* https://stackoverflow.com/questions/49957034/live-updating-dynamic-variable-on-html-with-flask
* https://pgjones.gitlab.io/quart/how_to_guides/templating.html

