from flask import json, make_response, redirect, render_template, request, url_for, jsonify
from flask import current_app as app
from . import voter, ballot, election
from bson.objectid import ObjectId

@app.route('/register', methods = ['POST'])
def register():
    output = { 'success': True }
    return jsonify(output), 200

@app.route('/login', methods = ['POST'])
def login():
    output = { 'token': 'AUTH-JWT-TOKEN' }
    return jsonify(output), 200