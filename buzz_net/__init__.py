from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__,
                instance_relative_config=False,
                template_folder="templates",
                static_folder="static")
    if app.config['ENV'] == 'production':
        app.config.from_object('config.ProdConfig')
    elif app.config['ENV'] == 'testing':
        app.config.from_object('config.TestConfig')
    else:
        app.config.from_object('config.DevConfig')

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from buzz_net.blue_prints import register_all_blueprints
        register_all_blueprints(app)

        db.create_all()
        return app
