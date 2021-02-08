from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
# from flask_mongoengine import MongoEngine

# db = SQLAlchemy()
app = Flask(__name__, instance_relative_config=False)
mongo = PyMongo(app, uri="mongodb://localhost:27017/flaskdb")
db = mongo.db

# collections needed can go here
voter = db.voter
ballot = db.ballot
election = db.election

def create_app():
    """Construct the core application."""
    # app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    

    # db.init_app(app)
    # app.config["MONGO_URI"] = "mongodb://localhost:27017/flaskdb"
    # mongo = PyMongo(app)
    # db_operations = mongo.db.voter

    with app.app_context():
        from . import routes  # Import routes
        # db.create_all()  # Create sql tables for our data models

        return app