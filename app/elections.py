from app.auth import require_access_voter
from flask import make_response, redirect, render_template, request, url_for, jsonify
from flask import current_app as app
from . import voter, ballot, election
from bson.objectid import ObjectId
import time

# GETs election info based on given ID
# http://localhost:5000/elections/<election_id>
@app.route('/elections/<election_id>', methods = ['GET'])
# @require_access_voter
def get_election(election_id):
    output = { 'success': False, 'error': '', 'election': '' }

    found = election.find_one({"_id": ObjectId(election_id)})
    if not found:
        output['error'] = f'Election not found for id {election_id}'
        return jsonify(output), 400
    
    output = { 'success': True, 'error': '', 'election': '' }
    output['election'] = {'_id': str(found['_id']), 'details': found['details'], 'choices': found['choices'], 'start': found['start'], 'end': found['end'] }
    return jsonify(output), 200

# GET all elections' info: 
# http://localhost:5000/elections
@app.route('/elections', methods = ['GET'])
# @require_access_voter
def get_elections():
    elections = election.find()
    output = [str(e['_id']) for e in elections]
    return jsonify(output), 200

# POST create a new election
# /elections
# Incoming JSON data:
# { "details":"", "choices":[], "start": 1616649785.220375, "end": 1616649785.220375}
# e.g choices=["a", "b", "c"]
@app.route('/elections', methods = ['POST'])
# @require_access_voter
def post_elections():
    output = {'success': False, 'error': '' }
    body = request.get_json(force=True)

    if 'details' not in body or 'choices' not in body:
        output['error'] = 'Required: details, choices'
        return jsonify(output), 400

    if 'start' not in body or 'end' not in body:
        output['error'] = 'Required: start, end'
        return jsonify(output), 400
    
    details = body["details"]
    choices = body["choices"]
    start = body["start"]
    end = body["end"]

    difference = end - start

    if difference <= 0:
        output['error'] = 'Invalid start and end dates'
        return jsonify(output), 400

    
    election_id = insert_election(details, choices, start, end).inserted_id
            
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


@app.route('/time', methods = ['GET'])
def get_time():
    output = time.time()

    return jsonify(output)

# Get elections you created (ONLY for your own voter_id)
# GET /elections/created/<voter_id>  (response have 2 lists: live and expired elections)

# Add Election for a Voter - POST /voters/:voterId/elections/:electionId
# @app.route('/elections/created/<voter_id>', methods = ['GET'])
# # @require_access_voter
# def get_owned_elections():
#     output = { 'success': False, 'error': '' }
#     body = request.get_json(force=True)

#     if 'voter_id' not in body or 'election_id' not in body:
#         output['error'] = 'Required: voter_id, election_id'
#         return jsonify(output), 400

#     voter_id = body["voter_id"]
#     election_id = body["election_id"]    

#     voter_to_update = voter.find_one({"_id": ObjectId(voter_id)})
#     if not voter_to_update:
#         output['error'] = f'Voter not found for id: {voter_id}'
#         return jsonify(output), 400
    
#     election_to_add = election.find_one({"_id": ObjectId(election_id)})
#     if not election_to_add:
#         output['error'] = f'Election not found for id: {election_id}'
#         return jsonify(output), 400

#     voter.update_one({ "_id": ObjectId(voter_id) }, {'$push': {'elections': election_id}})

#     output = { 'success': True, 'error': ''}
#     return jsonify(output), 200

def insert_election(details, choices, start, end):
    """Helper function for inserting new elections"""

    new_choices = [{
        'option': str(choice),
        'count': 0} for choice in choices]
    insert = { 'choices': new_choices, 'details': details, 'start': start, 'end': end }
    new_elec = election.insert_one(insert)
    
    return new_elec

