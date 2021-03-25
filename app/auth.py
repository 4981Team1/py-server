from flask import request, jsonify, abort
from flask import current_app as app
from werkzeug.datastructures import ImmutableMultiDict
from . import voter
from bson.objectid import ObjectId
from . import voter, ACCESS_LEVEL_VOTER, ACCESS_LEVEL_MACHINE
import jwt
import bcrypt
import datetime as dt
from functools import partial, wraps

@app.route('/register', methods = ['POST'])
def register():
    output = { 'success': False, 'error': '' }
    body = request.get_json(force=True)
    
    if 'email' not in body or 'password' not in body:
        output['error'] = 'Required: email, password'
        return jsonify(output), 400
    
    if 'name' not in body:
        name = body['email']
    else:
        name = body['name']

    v = voter.find_one({'email': body['email']})
    if v is not None:
        output['error'] = 'Email taken'
        return jsonify(output), 400
    
    raw_password = body['password'].encode()
    hashed = bcrypt.hashpw(raw_password, bcrypt.gensalt())

    new_voter = {
        'name': name,
        'email': body['email'],
        'password': hashed,
        'elections': [],
        'access_level': ACCESS_LEVEL_VOTER
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
    encoded_jwt = jwt.encode({ "exp": expires_on, "_id":  str(v['_id'])}, "secret-phrase-abc", algorithm="HS256")

    # jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
    output = { 'success': True, 'error': '', 'token': encoded_jwt.decode('utf-8'), '_id': str(v['_id']) }
    return jsonify(output), 200

def _require_access_level(api_method, access_level):
    @wraps(api_method)

    def validate_jwt_token(*args, **kwargs):
        output = { 'success': False, 'error': '' }

        if 'voter-token' not in request.headers:
            output['error'] = "Missing header: voter-token"
            return jsonify(output), 401
        
        encoded_jwt = request.headers['voter-token']
        try:
            jwt_payload = jwt.decode(encoded_jwt, "secret-phrase-abc", algorithms=["HS256"])
        except jwt.InvalidTokenError:
            output['error'] = "Invalid token: bad token"
            return jsonify(output), 401
        
        v = voter.find_one({'_id': ObjectId(jwt_payload['_id'])})
        if v is None:
            output['error'] = f'Invalid token: bad voter_id'
            return jsonify(output), 401

        if v['access_level'] > access_level:
            output['error'] = f'Invalid token: bad acces_level'
            return jsonify(output), 401

        headers_dict = dict(request.headers)
        headers_dict.update(jwt_payload)
        request.headers = ImmutableMultiDict(headers_dict)

        return api_method(*args, **kwargs)

    return validate_jwt_token

require_access_voter = partial(_require_access_level, access_level=ACCESS_LEVEL_VOTER)
require_access_machine = partial(_require_access_level, access_level=ACCESS_LEVEL_MACHINE)

@app.route('/jwt-protected', methods = ['GET'])
@require_access_voter
def jwt_protected():    
    output = { 'success': True, 'error': '' }
    print(request.headers)
    
    return jsonify(output), 200
