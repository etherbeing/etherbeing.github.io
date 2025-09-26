#!./scripts/.venv/bin/python
import subprocess
import dotenv
import os
import pathlib


if __name__ == "__main__":
    dotenv.load_dotenv()
    DATABASE_URL = os.environ.get("DATABASE_URL")
    COMMAND = "cargo sqlx prepare -- --lib"
    print(f"Running: DATABASE_URL={DATABASE_URL} {COMMAND}")
    subprocess.call(COMMAND, shell=True, env=os.environ, cwd=pathlib.Path(__file__).parent.parent)