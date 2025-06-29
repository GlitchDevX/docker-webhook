# Docker Redeploy Webhook

This project allows you to interact with docker on your server without having ssh access.

This could be beneficial in an ci/cd pipeline when you don't want to share a private key.

## Usage

Download the binary on your server and execute it with the api secret in an env variable.

```bash
# download the latest binary
wget https://github.com/GlitchDevX/docker-webhook/releases/latest/download/docker-webhook

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
