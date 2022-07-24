from app import create_app
from api import celery
app = create_app()
app.app_context().push()