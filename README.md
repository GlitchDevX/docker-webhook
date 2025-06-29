# Docker Redeploy Webhook

This project allows you to interact with docker on your server without having ssh access.

This could be beneficial in an ci/cd pipeline when you don't want to share a private key.


## Local Development

To start the API locally run

```bash
# once to install dependencies & create venv
uv sync

uv run fastapi dev
```

## Useful Links
[Docker Python Lib](https://docker-py.readthedocs.io/en/stable/)
