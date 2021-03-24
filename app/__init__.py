from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
# from flask_mongoengine import MongoEngine

# db = SQLAlchemy()
app = Flask(__name__, instance_relative_config=False)
uri = "mongodb+srv://admin:goodteam@cluster0.x0m4l.mongodb.net/flaskdb?retryWrites=true&w=majority"
# uri = "mongodb://localhost:27017/flaskdb" # uri for local db
# uri = "mongodb://localhost:27017/py_server" # uri for brian local db
mongo = PyMongo(app, uri)
# mongo = PyMongo(app, uri) # for connecting to hosted db
db = mongo.db

# collections needed can go here
voter = db.voter
ballot = db.ballot
election = db.election

def create_app():
    """Construct the core application."""
    # app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    

    with app.app_context():
        from . import routes  # Import routes
        from . import voters
        from . import elections
        from . import ballots
        from . import auth
        return app