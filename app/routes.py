from flask import make_response, redirect, render_template, request, url_for, jsonify
from flask import current_app as app
from bson.objectid import ObjectId
# from .models import db, Users # not currently used
from . import voter, ballot, election
import json

# Grabs all voters
# http://localhost:5000/
@app.route('/')
def index():
    # Creates a new election if there's no exising election document in DB
    filt = {'details' : 'test'}
    update = { "$setOnInsert": { 'choices': {'a':0, 'b':0, 'c':0}, 'details': 'test' }}
    election.update_one(filt, update, upsert=True)
    return "<h1>Welcome to good-team server</h1>"

# GET all voter's info: 
# http://localhost:5000/voters
# 
# GETs a voter's info based on given ID
# http://localhost:5000/voters/<VOTER_ID>
#
# POST add or update the specified voter's info: 
# http://localhost:5000/voters/<NAME>/<EMAIL>
# 
# DELETE a voter based on given ID, along with their existing ballots
# http://localhost:5000/voters/<VOTER_ID>
@app.route('/voters', defaults={'voter_id': None, 'name': None, 'email': None}, methods = ['GET'])
@app.route('/voters/<voter_id>', defaults={'name': None, 'email': None}, methods = ['GET', 'DELETE'])
@app.route('/voters/<name>/<email>', defaults={'voter_id': None}, methods = ['POST'])
def voters(voter_id, name, email):
    output = {}

    # POST /voters
    if request.method == 'POST':
        updated_voter = {"$set": {'email' : email}}
        filt = {'name' : name}
        voter.update_one(filt, updated_voter, upsert=True)

        # Return the updated/new voter
        new_voter = voter.find_one(filt)
        output = {
            '_id': str(new_voter['_id']),
            'name' : new_voter['name'],
            'email' : new_voter['email'],
            'elections' : new_voter['elections']
            }
    
    # GET /voters
    elif request.method == 'GET':
        # Check if there's an id parameter for looking up individuals
        if voter_id:
            # print(collection.find_one({"_id": ObjectId("59d7ef576cab3d6118805a20")}))
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
    
    # DELETE /voters
    elif request.method == 'DELETE':
        if voter_id:
            # print(collection.find_one({"_id": ObjectId("59d7ef576cab3d6118805a20")}))
            filt = {"_id": ObjectId(voter_id)}

            # TODO: Do we delete all the ballots associated to a voter when we delete that voter?
            ballot.delete_many(filt) # Delete all associated ballots to the voter first
            voter.delete_one(filt) # Delete the voter themselves
            output = {'success' : True}

        else:
            # TODO: Replace error message with something else?
            output = {'success' : False}

    print(output)
    return jsonify(output)

# GET all elections' info: 
# http://localhost:5000/elections
# 
# GETs election info based on given ID
# http://localhost:5000/elections/<election_id>
# 
# POST create a new election
# /elections/<details>/<choices>
# choices={"a":0, "b":0, "c":0, "d":0}
#
# POST update an existing election's info:
# /elections/<election_id>/<details>/<choices>
# choices={"a":0, "b":0, "c":0, "d":0}
# 
# DELETE an election based on given ID
# http://localhost:5000/elections/<election_id>
@app.route('/elections', defaults={'election_id': None, 'details': None, 'choices': None}, methods = ['GET'])
@app.route('/elections/<election_id>', defaults={'details': None, 'choices': None}, methods = ['GET', 'DELETE'])
@app.route('/elections/<details>/<choices>', defaults={'election_id': None}, methods = ['POST'])
@app.route('/elections/<election_id>/<details>/<choices>', methods = ['POST'])
def display_elections(election_id, details, choices):
    output = {}

    # POST /elections
    if request.method == 'POST':
        if election_id: # if id is present, then you update            
            updated_choices = json.loads(choices)

            filt = {"_id": ObjectId(election_id)}
            updated_elec = {"$set": {'details' : details, 'choices': updated_choices}}
            election.update_one(filt, updated_elec)

            # Return the updated/new election
            new_election = election.find_one(filt)
            output = {
                '_id': str(new_election['_id']),
                'details': new_election['details'],
                'choices': new_election['choices']
            }

        else: 
            # if no id is present, add an election
            new_choices = json.loads(choices)
            insert = { 'choices': new_choices, 'details': details }
            new_elec = election.insert_one(insert)
            
            filt = {"_id": ObjectId(new_elec.inserted_id)}
            new = election.find_one(filt)
            output = {
                '_id': str(new['_id']),
                'details': new['details'],
                'choices': new['choices']
            }

    # GET /elections
    elif request.method == 'GET':
        # Check if there's an id parameter for looking up specific election
        if election_id:
            # print(collection.find_one({"_id": ObjectId("59d7ef576cab3d6118805a20")}))
            filt = {"_id": ObjectId(election_id)}

            # Check if there's an election with the corresponding ID
            if election.count_documents(filt, limit=1) != 0: 
                found = election.find_one(filt)
                output = {
                    '_id': str(found['_id']),
                    'details': found['details'],
                    'choices': found['choices']
                    }
        
        # No id parameter means getting all elections info instead
        else:
            elections = election.find()
            output = [{
                '_id': str(election['_id']),
                'details': election['details'],
                'choices': election['choices']} for election in elections]
    
    # DELETE /elections
    elif request.method == 'DELETE':
        if election_id:
            filt = {"_id": ObjectId(election_id)}

            # Just delete the election for now
            election.delete_one(filt)
            output = {'success' : True}

        else:
            # TODO: Replace error message with something else?
            output = {'success' : False}

    print(output)
    return jsonify(output)

# GET all elections a given voter is eligible for and
# elections they haven't voted on yet.
# http://localhost:5000/eligible/<VOTER_ID>
# 
# GET check if voter is eligible to vote in given election
# http://localhost:5000/eligible/<VOTER_ID>/<ELECTION_ID>
# 
# POST add voter to an election
# http://localhost:5000/eligible/<VOTER_ID>/<ELECTION_ID>
# @app.route('/eligible/<voter_id>/voted', defaults={'election_id': None}, methods = ['GET'])
@app.route('/eligible/<voter_id>', defaults={'election_id': None}, methods = ['GET'])
# @app.route('/eligible/voted/<voter_id>', defaults={'election_id': None}, methods = ['GET'])
@app.route('/eligible/<voter_id>/<election_id>', methods = ['GET', 'POST'])
def eligible(voter_id, election_id):
    output = {} #not sure what to put for error message
    if voter_id:

        if request.method == 'GET' and election_id:
            found = voter.find_one({'_id': ObjectId(voter_id)})

            # Check if voter is allowed to vote in specified election
            output = {'eligible' : False}
            elections = found['elections']
            for e in elections:
                if e == election_id:
                    output = {'eligible' : True}
                    break
        
        # Getting all elections voter is eligible for
        elif request.method == 'GET':
            found = voter.find_one({'_id': ObjectId(voter_id)})
            elecs = found['elections']
            output = {
                'elections': elecs,
                'voteless': find_voteless_elections(elecs, voter_id)
            }

            # c = request.url_rule

            # if "voted" in c.rule:
            #     print("they voted")
       
        elif request.method == 'POST':
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
    print(output)
    return jsonify(output)

# Records the vote made by a voter into their ballot.
# If they haven't voted before, a new Ballot document will be created.
# Otherwise, an error message will occur.
# 
# POST http://localhost:5000/vote/<VOTER_ID>/<ELECTION_ID>/<CHOICE>
@app.route('/vote/<voter_id>/<election_id>/<choice>', methods = ['POST'])
def vote(voter_id, election_id, choice):   
    output = {} #not sure what to put for error message
    if voter_id and election_id and choice:

        if request.method == 'POST':
            found = voter.find_one({'_id': ObjectId(voter_id)})

            # Check if voter is allowed to vote in specified election,
            # then record their vote
            elections = found['elections']
            for e in elections:
                if e == election_id:
                    output = record_vote(voter_id, election_id, choice)
                    break
    return output

# Outputs the vote count as a JSON object
# http://localhost:5000/results/<election_id>
@app.route('/results/<election_id>', methods=['GET'])
def results(election_id):
    if request.method == 'GET':
        # Get objectID of test election
        elec = election.find_one({'_id': ObjectId(election_id)})
        output = elec['choices']

    print(output)
    return jsonify(output)

# Helper function for recording votes
def record_vote(vid, eid, choice):
    # Checking if user has already voted for that election
    output = {'success' : False}
    elec = election.find_one({'_id' : ObjectId(eid)})
    choices = elec['choices']

    filt = {'election_id' : eid, 'voter_id' : vid}
    if ballot.count_documents(filt, limit=1) == 0:

        # checking if user voted for a valid choice
        keys = [key  for key, value in choices.items()] # grabbing each key
        if choice in keys: 
            # Create new ballot if user hasn't voted yet
            new_ballot = {'choice' : choice, 'election_id' : eid, 'voter_id' : vid }
            ballot.insert_one(new_ballot)

            # Incrementing tally count
            election.update_one({'_id': elec['_id']}, {"$inc": {'choices.'+choice: 1}})
            output = {'success' : True}
    
    return output

# Helper function for finding elections a user is eligible for 
# but hasn't voted on yet.
# Returns array of str election ids
def find_voteless_elections(elecs, vid):
    output = []
    for eid in elecs:
        elec = election.find_one({'_id' : ObjectId(eid)})
        filt = {'election_id' : eid, 'voter_id' : vid}

        if ballot.count_documents(filt, limit=1) == 0:
            output.append(eid);
    
    return output;

