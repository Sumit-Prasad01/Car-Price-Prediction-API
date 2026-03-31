import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "policy_lens_agent"

list_of_files = [

    # Data
    "data/raw/.gitkeep",
    "data/processed/.gitkeep",

    # Main Application
    "app/__init__.py",
    "app/main.py",

    # Configurations and Security
    "app/core/__init__.py",
    "app/core/config.py",
    "app/core/security.py",
    "app/core/dependencies.py",
    "app/core/exceptions.py",

    # FastApi API
    "app/api/__init__.py",
    "app/api/routes_auth.py",
    "app/api/routes_predict.py",

    # Caching
    "app/cache/__init__.py",
    "app/cache/redis_cache.py",

    # Middlewares
    "app/middlewares/__init__.py",
    "app/middlewares/logging_middleware.py",

    # Saved Models
    "app/models/.gitkeep",

    # Services
    "app/services/__init__.py",
    "app/services/model_service.py",

    # Notebooks
    "notebooks/experimets.ipynb",

    # Utils
    "app/utils/__init__.py",
    "app/utils/logger.py",

    # Training Scripts
    "train/__init__.py",
    "train/data_ingestion.py",
    "train/data_processor.py",
    "train/model_trainer.py",
    "train/model_config.py",

    # Others
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