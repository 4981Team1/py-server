from flask import make_response, redirect, render_template, request, url_for, jsonify
from flask import current_app as app
# from .models import db, Users # not currently used
from . import voter, ballot, election
# # Turns debugging on (auto reload)
# app.run(debug=True)

# Grabs all voters
# http://localhost:5000/
@app.route('/')
def voter_records():
    # Creates a new election if there's no exising election document in DB
    filt = {'details' : 'test'}
    update = { "$setOnInsert": { 'choices': ['a', 'b', 'c'], 'details': 'test' }}
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

# Records the MOST RECENT vote made by a voter into their ballot.
# If they haven't voted before, a new Ballot document will be created.
# Otherwise, the ballot will be updated only with their most recent choice.
# 
# http://localhost:5000/vote?name=[NAME]&choice=[CHOICE]
# e.g. http://localhost:5000/vote?name=grover&choice=a
@app.route('/vote')
def vote():
    
    # Get url params
    name = request.args.get('name')
    choice = request.args.get('choice')
    
    # Get objectID of test election
    elec_id = str(election.find_one({'details' : 'test'})['_id']) #need to convert objectid to string
    # print(elec_id)

    # Get voterID of the voter specified by params
    voter_id = str(voter.find_one({'name' : name})['_id'])

    # Upsert new ballot document
    filt = {'election_id' : elec_id, 'voter_id' : voter_id}
    new_ballot = {"$set": {'choice' : choice, 'election_id' : elec_id, 'voter_id' : voter_id }}
    # ballot.insert_one(new_ballot)
    ballot.update_one(filt, new_ballot, upsert=True)
    result = {'result' : 'Voted successfully'}
    return result

# Outputs the vote count as a JSON object
# http://localhost:5000/results
@app.route('/results')
def results():

    # Get objectID of test election
    elec = election.find_one({'details' : 'test'})
    elec_id = str(elec['_id']) #need to convert objectid to string
    elec_choices = elec['choices']

    ballots = ballot.find({'election_id' : elec_id})
    votes = [b['choice'] for b in ballots] # getting all the votes from the ballots
    # print(votes)

    # Contains vote count
    output = [{c : votes.count(c)} for c in elec_choices]
        
    print(output)
    return jsonify(output)