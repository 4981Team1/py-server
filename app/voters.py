from app.auth import require_access_voter
from flask import make_response, redirect, render_template, request, url_for, jsonify
from flask import current_app as app
from . import voter, ballot, election
from bson.objectid import ObjectId
import time

@app.route('/voterstest')
def voterstest():
    return "<h1>Welcome to voters</h1>"

# Get Voter - GET /voters/:id
# Delete Voter - DELETE /voters/:id
@app.route('/voters', defaults={'voter_id': None}, methods = ['GET'])
@app.route('/voters/<voter_id>', methods = ['GET', 'DELETE'])
def get_voter(voter_id):
    output = {
        '_id': "",
        'success': False
    }

    if request.method == 'GET':
        # Check if there's an id parameter for looking up individuals
        if voter_id:
            filt = {"_id": ObjectId(voter_id)}

            # Check if there's a voter with the corresponding ID
            if voter.count_documents(filt, limit=1) != 0: 
                found = voter.find_one(filt)
                output = {
                    '_id': str(found['_id']),
                    'name' : found['name'],
                    'email' : found['email'],
                    'elections' : found['elections']
                    }
        
        # No id parameter means getting all voters' info instead
        else:
            voters = voter.find()
            output = [{
                '_id': str(voter['_id']),
                'name' : voter['name'],
                'email' : voter['email'],
                'elections': voter['elections']} for voter in voters]
    
    elif request.method == 'DELETE':
        if voter_id:
            filt = {"_id": ObjectId(voter_id)}

            ballot.delete_many(filt) # Delete all associated ballots to the voter first
            voter.delete_one(filt) # Delete the voter themselves
            output = {'success' : True}

        else:
            output = {'success' : False}

    print(output)
    return jsonify(output)

def filter_votable(elections, v_id):
    votable, non_votable = [], []
    current_time = time.time()

    for e_id in elections:
        existing_ballots = ballot.count_documents({'election_id': e_id, 'voter_id': v_id}, limit=1)
        
        # getting each election's end date
        curr_elec = election.find_one({'_id': ObjectId(e_id)})
        difference = curr_elec['end'] - current_time

        if existing_ballots == 0 and difference > 0:
            votable.append(e_id)
        else:
            non_votable.append(e_id)
            
    return votable, non_votable

# Get Elections for a Voter - GET /voters/:voterId/elections
@app.route('/voters/<voter_id>/elections', methods = ['GET'])
@require_access_voter
def get_elections_for_voters(voter_id):
    output = { 'success': False, 'error': '', 'votable': [], 'non_votable': [] }
    
    found = voter.find_one({'_id': ObjectId(voter_id)})
    if not found:
        output['error'] = f'Voter not found for id {voter_id}'
        return jsonify(output), 400
    
    votable, non_votable = filter_votable(found['elections'], voter_id)
    output = { 'success': True, 'error': '', 'votable': votable, 'non_votable': non_votable }
    return jsonify(output), 200

# Add Election for a Voter - POST /voters/:voterId/elections/:electionId
@app.route('/voters/elections', methods = ['POST'])
@require_access_voter
def add_election_for_voter():
    output = { 'success': False, 'error': '' }
    body = request.get_json(force=True)

    if 'voter_id' not in body or 'election_id' not in body:
        output['error'] = 'Required: voter_id, election_id'
        return jsonify(output), 400

    voter_id = body["voter_id"]
    election_id = body["election_id"]    

    voter_to_update = voter.find_one({"_id": ObjectId(voter_id)})
    if not voter_to_update:
        output['error'] = f'Voter not found for id: {voter_id}'
        return jsonify(output), 400
    
    election_to_add = election.find_one({"_id": ObjectId(election_id)})
    if not election_to_add:
        output['error'] = f'Election not found for id: {election_id}'
        return jsonify(output), 400

    voter.update_one({ "_id": ObjectId(voter_id) }, {'$push': {'elections': election_id}})

    output = { 'success': True, 'error': ''}
    return jsonify(output), 200

# Remove Election from a Voter - DELETE /voters/:voterId/elections/:electionId
@app.route('/voters/<voter_id>/elections/<election_id>', methods = ['DELETE'])
@require_access_voter
def delete_election_for_voter(voter_id, election_id):
    keyword = "elections"
    url = str(request.url_rule)
    output = {
        'success': False
    }

    if request.method == 'DELETE' and keyword in url:
        if voter_id and election_id:
            efilt = {'_id' : ObjectId(election_id)}
            if election.count_documents(efilt, limit=1) != 0: 
                # If election exists, remove election from voter array
                found = voter.find_one({'_id': ObjectId(voter_id)})
                remove = { "$pull": { 'elections': election_id} }
                voter.update(found, remove)
                # print("Successfully removed!")
                output = {'success' : True}
    return output

