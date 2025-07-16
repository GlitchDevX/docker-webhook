import sys
import uvicorn
import multiprocessing

from docker_webhook.app.main import app

def run_app():
    multiprocessing.freeze_support()  # For Windows support
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, workers=1)

if __name__ == '__main__':
    run_app()
