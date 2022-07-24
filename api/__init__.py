from celery import Celery
from config import Config

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
celery.config_from_object(__name__)