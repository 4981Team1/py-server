from flask import make_response, redirect, render_template, request, url_for, jsonify
from flask import current_app as app
from . import voter, ballot, election
from bson.objectid import ObjectId

@app.route('/register', methods = ['POST'])
def register():
    return "Register route"

@app.route('/login', methods = ['POST'])
def login():
    return "Login route"