from flask import Flask
from api.views import book

def create_app():
    app = Flask(__name__)

    app.register_blueprint(book.book)
    app.config.update(CELERY_CONFIG={
        'broker_url': 'redis://localhost:6379',
        'result_backend': 'redis://localhost:6379',
    })


    return app
