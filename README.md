# Docker Redeploy Webhook

This project allows you to interact with docker on your server without having ssh access.

This could be beneficial in an ci/cd pipeline when you don't want to share a private key.

## Usage

### Precompiled Binaries

Download the binary on your server and execute it with the api secret in an env variable.

```bash
# download the latest linux binary
platform="ubuntu-24.04-x64" # or ubuntu-22.04-arm64
curl -s https://api.github.com/repos/glitchdevx/docker-webhook/releases/latest | grep -w "browser_download_url" | grep -e "$platform" | sed -E 's/.*: "(.*)"/\1/' | xargs wget

# set secret in env var
export API_SECRET=your-secure-secret

# run the application
./docker-webhook
```

### From source code

You'll need to have `git`, `python` & `uv` installed to run this project from source code.

- [Git Download](https://git-scm.com/downloads)
- [Python 3.11 Download](https://www.python.org/downloads/)
- [uv Download](https://docs.astral.sh/uv/getting-started/installation/)


```bash
# clone the repository
git clone https://github.com/glitchdevx/docker-webhook.git && cd docker-webhook

# install dependencies
uv sync

# set secret in env var
export API_SECRET=your-secure-secret

# run code
uv run docker-webhook
```

## Local Development

To start the API locally run

```bash
# once to install dependencies & create venv
uv sync

uv run fastapi dev
```

## Commit Message Convention
This repository uses automatic version increments for releases. 
For this to work we need to add a prefix in the commit message depending on the size of the changes.

- **#none**: v0.12.1 -> v0.12.1 (e.g. README changes)
- **#patch**: v0.12.1 -> v0.12.2
- **#minor**: v0.12.1 -> v0.13.0
- **#major**: v0.12.1 -> v1.0.0

Example commit message
```
#minor added port parameter to redeploy endpoints
```


## Useful Links
[Docker Python Lib](https://docker-py.readthedocs.io/en/stable/)
