from flask import request, jsonify, abort
from flask import current_app as app
from . import voter
from bson.objectid import ObjectId
from . import voter
import jwt
import bcrypt
import datetime as dt
from functools import wraps

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

    new_voter = {
        'name': body['email'],
        'email': body['email'],
        'password': hashed,
        'elections': []
    }

    voter_id = voter.insert_one(new_voter).inserted_id
    
    output = { 'success': True, 'error': '', '_id': str(voter_id) }
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
    
    # {"exp": 1371720939}
    expires_on = dt.datetime.utcnow() + dt.timedelta(hours=1)
    encoded_jwt = jwt.encode({ "exp": expires_on }, "secret-phrase-abc", algorithm="HS256")

    # jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
    output = { 'success': True, 'error': '', 'token': encoded_jwt.decode('utf-8') }
    return jsonify(output), 200

def require_jwt_token(api_method):
    @wraps(api_method)

    def check_jwt_token(*args, **kwargs):
        output = { 'success': False, 'error': '' }
        if 'voter-token' not in request.headers:
            output['error'] = "Missing token: voter-token"
            return jsonify(output), 401
        
        encoded_jwt = request.headers['voter-token']

        try:
            jwt.decode(encoded_jwt, "secret-phrase-abc", algorithms=["HS256"])
        except jwt.InvalidTokenError:
            output['error'] = "Invalid token: voter-token"
            return jsonify(output), 401
        
        return api_method(*args, **kwargs)

    return check_jwt_token


@app.route('/jwt-protected', methods = ['GET'])
@require_jwt_token
def jwt_protected():    
    output = { 'success': True, 'error': '' }
    return jsonify(output), 200
