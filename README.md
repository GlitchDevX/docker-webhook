# Docker Redeploy Webhook

This project allows you to interact with docker on your server without having ssh access.

This could be beneficial in an ci/cd pipeline when you don't want to share a private key.

## Usage

Download the binary on your server and execute it with the api secret in an env variable.

```bash
# download the latest linux binary
curl -s https://api.github.com/repos/glitchdevx/docker-webhook/releases/latest | grep -w "browser_download_url" | grep -e "ubuntu" | sed -E 's/.*: "(.*)"/\1/' | xargs wget

# export env var
export API_SECRET=your-secure-secret

# run the application
./docker-webhook
```

## Local Development

To start the API locally run

```bash
# once to install dependencies & create venv
uv sync

uv run fastapi dev
```

## Useful Links
[Docker Python Lib](https://docker-py.readthedocs.io/en/stable/)
