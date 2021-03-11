from flask import make_response, redirect, render_template, request, url_for, jsonify
from flask import current_app as app
from . import voter, ballot, election
from bson.objectid import ObjectId

@app.route('/voterstest')
def voterstest():
    return "<h1>Welcome to voters</h1>"

# Create Voter - POST /voters
# INCOMING: { name = "", email = "" }
@app.route('/voters', methods = ['POST'])
def post_voter():
    output = {
        '_id': "",
        'success': False
    }

    name = request.json["name"]
    email = request.json["email"]

    if name and email:
        output = create_voter(name, email)
    
    return jsonify(output)

# Get Voter - GET /voters/:id
# Delete Voter - DELETE /voters/:id
@app.route('/voters/<voter_id>', defaults={'name': None, 'email': None}, methods = ['GET', 'DELETE'])
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

# Get Elections for a Voter - GET /voters/:voterId/elections
@app.route('/voters/<voter_id>/elections', methods = ['GET'])
def get_elections_for_voters(voter_id):
    keyword = "elections"
    url = str(request.url_rule)
    output = {}

    if request.method == 'GET' and keyword in url:
        if voter_id:
            found = voter.find_one({'_id': ObjectId(voter_id)})
            elecs = found['elections']
            output = find_elections(elecs, voter_id)

    return output

# Add Election for a Voter - POST /voters/:voterId/elections/:electionId
@app.route('/voters/elections', methods = ['POST'])
def add_election_for_voter():
    keyword = "elections"
    url = str(request.url_rule)
    output = {}

    voter_id = request.json["voter_id"]
    election_id = request.json["election_id"]

    if request.method == 'POST' and keyword in url:
        if voter_id and election_id:
            # Verify first if given election exists
            efilt = {'_id' : ObjectId(election_id)}
            if election.count_documents(efilt, limit=1) != 0: 
                # If election exists, update the voter's election array!
                vfilt = {'_id' : ObjectId(voter_id)}
                update = { "$push": { 'elections' : election_id}}
                voter.update_one(vfilt, update)
                output = {'success' : True}
            else:
                output = {'success' : False}
    return jsonify(output)

# Remove Election from a Voter - DELETE /voters/:voterId/elections/:electionId
@app.route('/voters/<voter_id>/elections/<election_id>', methods = ['DELETE'])
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

# Helper function to create a new voter
# INCOMING: { name = "", email = "" }
def create_voter(name, email):
    output = {}

    new_voter = {
        'name' : name,
        'email' : email,
        'elections': []
    }
    
    created_voter = voter.insert_one(new_voter)

    filt = {"_id": ObjectId(created_voter.inserted_id)}
    check_user = voter.find_one(filt)
    output = {
        '_id': str(check_user['_id']),
        'success': True
    }

    return output

# Requires a voters' elections array and voterID
def find_elections(elecs, vid):
    """
    Helper function for finding a voter's votable and non-votable elections.\n
    Returns:\n
    JSON obj of a voter's votable and non-votable elections.
    """

    output = {}
    non_votable = []
    votable = []

    for eid in elecs:
        elec = election.find_one({'_id' : ObjectId(eid)})
        filt = {'election_id' : eid, 'voter_id' : vid}

        # If there's NO EXISTING ballots made by the user for the current election,
        # add the electionID into the "votable" elections list.
        if ballot.count_documents(filt, limit=1) == 0:
            votable.append(eid)
        
        # If a ballot made by the user EXISTS for the current election,
        # add electionID into "non-votable" elections list.
        else:
            non_votable.append(eid)

    output = {
        'votable' : votable,
        'non_votable' : non_votable
    }
    
    return output