from flask import make_response, redirect, render_template, request, url_for, jsonify
from flask import current_app as app
from bson.objectid import ObjectId
from . import voter, ballot, election

# GET all ballots' info: 
# http://localhost:5000/ballots
# @app.route('/ballots', methods=['GET'])
# def ballots():
#     if request.method == 'GET':
#         ballots = ballot.find()
#         output = [{
#             '_id': str(bal['_id']),
#             'election_id': bal['election_id'],
#             'voter_id': bal['voter_id'],
#             'choice' : bal['choice']} for bal in ballots]
    
#     print(output)
#     return jsonify(output)

# Records the vote made by a voter into their ballot.
# If they haven't voted before, a new Ballot document will be created.
# Otherwise, an error message will occur.
# 
# POST http://localhost:5000/ballots
@app.route('/ballots', methods = ['POST'])
def ballots():   
    voter_id = request.json["voter_id"]
    election_id = request.json["election_id"]
    choice = request.json["choice"]

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

# Helper function for recording votes
def record_vote(vid, eid, choice):
    """Helper function for recording new votes"""

    # Checking if user has already voted for that election
    output = {'success' : False}
    elec = election.find_one({'_id' : ObjectId(eid)})
    length = len(elec['choices'])

    filt = {'election_id' : eid, 'voter_id' : vid}
    if ballot.count_documents(filt, limit=1) == 0:

        # checking if user voted for a valid choice
        if int(choice) < length - 1 and int(choice) > -1:
            # Create new ballot if user hasn't voted yet
            new_ballot = {'choice' : choice, 'election_id' : eid, 'voter_id' : vid }
            ballot.insert_one(new_ballot)

            # Incrementing tally count
            election.update_one({'_id': elec['_id']}, {"$inc": {'choices.'+choice+'.count': 1}})
            output = {'success' : True}
    
    return output