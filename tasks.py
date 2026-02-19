import os

from dotenv import load_dotenv

from celery import Celery

load_dotenv()

app = Celery('tasks', broker=os.getenv('CELERY_BROKER_URL'))