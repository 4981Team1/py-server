from flask import json, make_response, redirect, render_template, request, url_for, jsonify
from flask import current_app as app
from . import voter
from bson.objectid import ObjectId
from . import voter
import bcrypt

@app.route('/register', methods = ['POST'])
def register():
    output = { 'success': False, 'error': '' }
    body = request.get_json(force=True)
    
    if 'email' not in body or 'password' not in body:
        output['error'] = 'Required: email, password'
        return jsonify(output), 400

    v = voter.find_one({'email': body['email']})
    if v is not None:
        output['error'] = 'Email taken'
        return jsonify(output), 400
    
    raw_password = body['password'].encode()
    hashed = bcrypt.hashpw(raw_password, bcrypt.gensalt())
    voter.insert({'email': body['email'], 'password': hashed})
    
    output = { 'success': True, 'error': '' }
    return jsonify(output), 200

@app.route('/login', methods = ['POST'])
def login():
    output = { 'success': False, 'error': '' }
    body = request.get_json(force=True)
    
    if 'email' not in body or 'password' not in body:
        output['error'] = 'Required: email, password'
        return jsonify(output), 400
    
    v = voter.find_one({'email': body['email']})
    if v is None:
        output['error'] = f"No user for email {body['email']}"
        return jsonify(output), 400
    
    raw_password = body['password'].encode()
    if not bcrypt.checkpw(raw_password, v['password']):
        output['error'] = f"No user for email {body['email']}"
        return jsonify(output), 400

    # jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
    output = { 'success': True, 'error': '', 'token': 'AUTH-JWT-TOKEN' }
    return jsonify(output), 200