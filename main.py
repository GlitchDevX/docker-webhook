import uvicorn
import multiprocessing

from app.main import app

if __name__ == '__main__':
    multiprocessing.freeze_support()  # For Windows support
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, workers=1)
