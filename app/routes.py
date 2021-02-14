from flask import make_response, redirect, render_template, request, url_for, jsonify
from flask import current_app as app
from bson.objectid import ObjectId
# from .models import db, Users # not currently used
from . import voter, ballot, election

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
# http://localhost:5000/voters?id=[VOTER_ID]
#
# POST add or update the specified voter's info: 
# http://localhost:5000/voters?name=[NAME]&email=[EMAIL]
# 
# DELETE a voter based on given ID, along with their existing ballots
# http://localhost:5000/voters?id=[VOTER_ID]
# @app.route('/eligible/<voter_id>', defaults={'election_id': None}, methods = ['GET'])
@app.route('/voters', defaults={'voter_id': None, 'name': None, 'email': None}, methods = ['GET'])
@app.route('/voters/<voter_id>', defaults={'name': None, 'email': None}, methods = ['GET', 'DELETE'])
@app.route('/voters/<name>/<email>', defaults={'voter_id': None}, methods = ['POST'])
def voters(voter_id, name, email):

    output = {}
    # POST /voters
    if request.method == 'POST':
        # name = request.args.get('name')
        # email = request.args.get('email')
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
        # voter_id = request.args.get('id')
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
        # voter_id = request.args.get('id')
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


# GET all elections a given voter is eligible for
# http://localhost:5000/eligible?id=[VOTER_ID]
# 
# GET check if voter is eligible to vote in given election
# http://localhost:5000/eligible?id=[VOTER_ID]&election_id=[ELECTION_ID]
# 
# POST add voter to an election
# http://localhost:5000/eligible?id=[VOTER_ID]&election_id=[ELECTION_ID]
@app.route('/eligible/<voter_id>', defaults={'election_id': None}, methods = ['GET'])
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
            output = found['elections']
       
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
# POST http://localhost:5000/vote?id=[VOTER_ID]&election_id=[ELECTION_ID]&choice=[CHOICE]
# e.g. http://localhost:5000/vote?name=grover&choice=a
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

# TODO: Update so it shows results of a specified election instead
# Outputs the vote count as a JSON object
# http://localhost:5000/results
@app.route('/results', methods=['GET'])
def results():
    if request.method == 'GET':
        # Get objectID of test election
        elec = election.find_one({'details' : 'test'})
        output = elec['choices']

    print(output)
    return jsonify(output)

# GET all ballots' info: 
# http://localhost:5000/ballots
@app.route('/ballots', methods=['GET'])
def ballots():
    if request.method == 'GET':
        ballots = ballot.find()
        output = [{
            '_id': str(bal['_id']),
            'election_id': bal['election_id'],
            'voter_id': bal['voter_id'],
            'choice' : bal['choice']} for bal in ballots]
    
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