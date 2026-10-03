import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)

import uvicorn  # noqa: E402

if __name__ == "__main__":
    print("[EduGenie] Project folder:", BASE_DIR)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)