from flask import make_response, redirect, render_template, request, url_for, jsonify
from flask import current_app as app
# from .models import db, Users # not currently used
from . import voter, ballot, election

# Grabs all voters
# http://localhost:5000/
@app.route('/')
def index():
  return "<h1>Welcome to good-team server</h1>"


# Grabs all voters
# http://localhost:5000/allvoters
@app.route('/allvoters')
def allvoters():
    # Creates a new election if there's no exising election document in DB
    filt = {'details' : 'test'}
    update = { "$setOnInsert": { 'choices': {'a':0, 'b':0, 'c':0}, 'details': 'test' }}
    election.update_one(filt, update, upsert=True)

    # Grabs all users
    voters = voter.find()
    output = [{'name' : voter['name'], 'email' : voter['email']} for voter in voters]
    print(output)
    return jsonify(output)

# Updates one voter's email based on name, it would 
# insert a new voter if it doesn't already exist.
# http://localhost:5000/update?name=[NAME]&email=[EMAIL]
# e.g. http://localhost:5000/update?name=grover&email=another@email.com
@app.route('/update')
def update():
    name = request.args.get('name')
    email = request.args.get('email')
    updated_voter = {"$set": {'email' : email}}
    filt = {'name' : name}
    voter.update_one(filt, updated_voter, upsert=True)
    result = {'result' : 'Updated successfully'}
    return result;
    
# Deletes one voter based on name
# http://localhost:5000/delete?name=[NAME]
# e.g. http://localhost:5000/delete?name=grover
@app.route('/delete')
def delete():
    name = request.args.get('name')
    filt = {'name' : name}
    voter.delete_one(filt)
    result = {'result' : 'Deleted successfully'}
    return result;

# Records the vote made by a voter into their ballot.
# If they haven't voted before, a new Ballot document will be created.
# Otherwise, an error message will occur.
# 
# http://localhost:5000/vote?name=[NAME]&choice=[CHOICE]
# e.g. http://localhost:5000/vote?name=grover&choice=a
@app.route('/vote')
def vote():
    
    # Get url params
    name = request.args.get('name')
    choice = request.args.get('choice')
    
    # Get objectID of test election
    elec = election.find_one({'details' : 'test'})
    elec_id = str(elec['_id']) #need to convert objectid to string
    choices = elec['choices']
    # print(elec_id)

    # Get voterID of the voter specified by params
    voter_id = str(voter.find_one({'name' : name})['_id'])

    # Checking if user has already voted for that election
    filt = {'election_id' : elec_id, 'voter_id' : voter_id}
    if ballot.count_documents(filt, limit=1) != 0:
        result = {'result': 'Voter already voted!'}
    else:
        # checking if user voted for a valid choice
        keys = [key  for key, value in choices.items()] # grabbing each key
        if choice in keys: 
            
            # Create new ballot if user hasn't voted yet
            new_ballot = {'choice' : choice, 'election_id' : elec_id, 'voter_id' : voter_id }
            ballot.insert_one(new_ballot)

            # Incrementing tally count
            election.update_one({'_id': elec['_id']}, {"$inc": {'choices.'+choice: 1}})
            result = {'result' : 'Vote recorded successfully'}
        
        else:
            result = {'result' : 'Vote contained invalid answer'}

    print(result)
    return result

# Outputs the vote count as a JSON object
# http://localhost:5000/results
@app.route('/results')
def results():

    # Get objectID of test election
    elec = election.find_one({'details' : 'test'})
    output = elec['choices']

    print(output)
    return jsonify(output)