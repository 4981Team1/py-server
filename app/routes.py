from flask import make_response, redirect, render_template, request, url_for, jsonify
from flask import current_app as app
from bson.objectid import ObjectId
from . import voter, ballot, election
import json

# Index route
# http://localhost:5000/
@app.route('/')
def index():
    return "<h1>Welcome to good-team server</h1>"
