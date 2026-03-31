import urllib.request
from app.core.paths import DATASET_PATH
from app.core.config import settings
from app.utils.logger import logger
from app.utils.custom_exception import CustomException

url = settings.DATASET_URL

try:
    logger.info("Downloading dataset......")

    urllib.request.urlretrieve(url, DATASET_PATH)

    logger.info("Dataset downloaded successfully!")

except Exception as e:
    logger.error(f"Error while downloading dataset : {e}")
    raise CustomException("Failed to download dataset : ", e)