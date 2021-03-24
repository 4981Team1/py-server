from app.auth import require_jwt_token
from flask import make_response, redirect, render_template, request, url_for, jsonify
from flask import current_app as app
from . import voter, ballot, election
from bson.objectid import ObjectId

# GETs election info based on given ID
# http://localhost:5000/elections/<election_id>
@app.route('/elections/<election_id>', methods = ['GET'])
@require_jwt_token
def get_election(election_id):
    output = { 'success': False, 'error': '', 'election': '' }

    found = election.find_one({"_id": ObjectId(election_id)})
    if not found:
        output['error'] = f'Election not found for id {election_id}'
        return jsonify(output), 400
    
    output = { 'success': True, 'error': '', 'election': '' }
    output['election'] = {'_id': str(found['_id']), 'details': found['details'], 'choices': found['choices'] }
    return jsonify(output), 200

# GET all elections' info: 
# http://localhost:5000/elections
@app.route('/elections', methods = ['GET'])
@require_jwt_token
def get_elections():
    elections = election.find()
    output = [{ '_id': str(e['_id']),
            'details': e['details'],
            'choices': e['choices']} for e in elections] 
    return jsonify(output), 200

# POST create a new election
# /elections
# Incoming JSON data:
# { details="", choices=[]}
# e.g choices=["a", "b", "c"]
@app.route('/elections', methods = ['POST'])
@require_jwt_token
def post_elections():
    output = {'success': False, 'error': '' }
    body = request.get_json(force=True)

    if 'details' not in body or 'choices' not in body:
        output['error'] = 'Required: details, choices'
        return jsonify(output), 400
    
    details = body["details"]
    choices = body["choices"]
    
    election_id = insert_election(details, choices).inserted_id
            
    output = {'success': True, 'error': '', '_id': str(election_id)}
    return jsonify(output)


# Get Voters for eligible for given Election
# GET /elections/:electionID/voters
@app.route('/elections/<election_id>/voters', methods = ['GET'])
def get_voters_for_election(election_id):
    keyword = "voters"
    url = str(request.url_rule)
    output = []

    # checking if /voters is in the url
    if request.method == "GET" and keyword in url:
        # check if an election id is given
        if election_id:
            voters = voter.find() # get all voters
            allvoters = [{
                '_id': str(v['_id']),
                'name' : v['name'],
                'email' : v['email'],
                'elections': v['elections']} for v in voters]
            
            # Go through each voter's eligible elections
            # If voter is eligible in given election, update the list
            for curr_voter in allvoters:
                for curr_elec in curr_voter['elections']:
                    if election_id in curr_elec:
                        print("found it!")
                        output.append(curr_voter['_id'])
                        break

    return jsonify(output)


def insert_election(details, choices):
    """Helper function for inserting new elections"""

    new_choices = [{
        'option': str(choice),
        'count': 0} for choice in choices]
    insert = { 'choices': new_choices, 'details': details }
    new_elec = election.insert_one(insert)
    
    return new_elec

