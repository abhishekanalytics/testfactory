from flask import Flask
from flask_pymongo import PyMongo
from .config import Config             

mongo = PyMongo()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mongo.init_app(app)

    from .views.views import main_blueprint
    app.register_blueprint(main_blueprint)

    return app  


if __name__ == '__main__':
    app =create_app()
    app.run(debug=True)
