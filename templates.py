import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "policy_lens_agent"

list_of_files = [

    # Data
    "data/.gitkeep",

    # Main Application
    "app/__init__.py",

    # Configurations and Security
    "app/core/__init__.py",
    "app/core/config.py",
    "app/core/security.py",

    # Notebooks
    "notebooks/experimets.ipynb",

    "setup.py",
    "requirements.txt",
    ".env",
    ".gitignore",
    "dockerfile",
    "docker-compose.yml",
    "prometheus.yml",
    "render.yml"


]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file {filename}")

    if not os.path.exists(filepath):
        with open(filepath, 'w'):
            pass
        logging.info(f"Creating file: {filepath}")
    else:
        logging.info(f"{filename} already exists")