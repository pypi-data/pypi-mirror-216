import uvicorn
from .just_scan_api import app


def run_api():
    uvicorn.run(app, host="127.0.0.1", port=8000)


def main():
    run_api()


if __name__ == "__main__":
    main()
