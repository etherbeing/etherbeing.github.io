#!/usr/bin/env python3
# Startup script for DEVELOPMENT mode only

import atexit
import glob
import subprocess
import pathlib
import os
import logging
import sys
import requests
from threading import Thread
from time import sleep

logging.basicConfig(level=logging.DEBUG)

def start_the_postgres():
    """
    Startup the postgres DB in case isn't already
    """
    try:
        try:
            with open(os.devnull, "w") as f:
                subprocess.check_call(["-c", "psql -l"], shell=True, stdin=f, stderr=f, stdout=f)
            return # go on as the psql server is already running
        except subprocess.CalledProcessError: # if the psql server is not running then start it
            command = subprocess.run(["-c", "/usr/bin/systemctl start postgresql"], shell=True, stdin=sys.stdin, stderr=sys.stderr, stdout=sys.stdout)
            if command.returncode == 0:
                logging.info("DB successfully enabled")
            else:
                logging.warning("DB couldn't startup successfully")
                exit(1)
    except KeyboardInterrupt:
        logging.info("Command exited with keyboard interrupt signal...")
        exit(1)

def watch_the_cargo():
    """
    BACKEND
    Execute the cargo Actix Web server in watch mode so it auto reload
    """
    try:
        command = subprocess.run(["-c", "watchexec -e rs -r cargo run src/main.rs"], cwd=pathlib.Path("./api/"), shell=True, stdin=sys.stdin, stderr=sys.stderr, stdout=sys.stdout)
        if command.returncode == 0:
            logging.info("Backend was quitted")
        else:
            logging.warning("Backend couldn't run successfully")
    except KeyboardInterrupt:
        logging.info("Command exited with keyboard interrupt signal...")
        exit(2)

def watch_the_vite():
    """
    FRONTEND
    Execute the frontend in svelte using pnpm run dev
    """
    try:
        command = subprocess.run(["-c", "pnpm run dev"], cwd=pathlib.Path("./web/"), shell=True, stdin=sys.stdin, stderr=sys.stderr, stdout=sys.stdout)
        if command.returncode == 0:
            logging.info("Frontend was quitted")
        else:
            logging.warning("Frontend couldn't run successfully")
    except KeyboardInterrupt:
        logging.info("Command exited with keyboard interrupt signal...")
        exit(3)


def watch_the_api_for_vite():
    """
    FRONTEND LINK TO BACKEND
    Execute the link to openapi from the frontend in svelte to the backend through utoipa (openapi.json) using pnpm run openapi-ts -w 
    """
    try:
        command = subprocess.run(["-c", "pnpm run openapi-ts -w"], cwd=pathlib.Path("./web/"), shell=True, stdin=sys.stdin, stderr=sys.stderr, stdout=sys.stdout)
        if command.returncode == 0:
            logging.info("Frontend Linker was quitted")
        else:
            logging.warning("Frontend Linker couldn't run successfully")
    except KeyboardInterrupt:
        exit(4)

@atexit.register
def cleanup():
    logging.info("Cleaning up the logs and rest of files")
    to_remove = []
    for place in ["web", "api"]:
        for file in glob.glob(f"{place}/*.log"):
            to_remove.append(file)
    logging.info(f"Detected {len(to_remove)} trash files to remove with the name:\n{"\n".join(to_remove)}")
    for file in to_remove:
        os.remove(file)

if __name__ == "__main__":
    # Startup the DB
    start_the_postgres()
    # Execute Backend Server
    backend = Thread(target=watch_the_cargo, daemon=False)
    backend.start()
    # Start the frontend server
    frontend = Thread(target=watch_the_vite, daemon=False)
    frontend.start()
    # Start the frontend linker server
    frontend_linker = Thread(target=watch_the_api_for_vite, daemon=False)
    max_attempts = 10
    sleep(3) # delay
    while True:
        try:
            requests.get("http://localhost:8080/swagger-ui/#/").raise_for_status()
            break
        except requests.exceptions.RequestException:
            sleep(1)
            max_attempts -= 1
            if not max_attempts:
                break
            continue
    frontend_linker.start()
    rotation_speed = 5 # seconds
    while True:
        for thread in [backend, frontend, frontend_linker]: # iterates over each watching if there is any that exited already if so then quit them all
            try:
                if thread.is_alive():
                    thread.join(rotation_speed)
                else:
                    exit(0) # quit them all
            except TimeoutError:
                continue
            except RuntimeError:
                exit(0) # quit them all
            except KeyboardInterrupt:
                exit(0)
