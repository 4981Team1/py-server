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
# @require_jwt_token
def ballots():
    output = { 'success': False, 'error': '' }
    body = request.get_json(force=True)

    if 'voter_id' not in body or 'election_id' not in body or 'choice' not in body:
        output['error'] = 'Required: voter_id, election_id, choice'
        return jsonify(output), 400
    
    voter_id = body["voter_id"]
    election_id = body["election_id"]
    choice = int(body["choice"])

    found = voter.find_one({'_id': ObjectId(voter_id)})
    elections = found['elections']
    
    if election_id not in elections:
        output['error'] = f'Voter not eligible to vote in {election_id}'
        return jsonify(output), 400
    
    existing_ballots = ballot.count_documents({'election_id': election_id, 'voter_id': voter_id}, limit=1)
    if existing_ballots != 0:
        output['error'] = f'Voter already voted in {election_id}'
        return jsonify(output), 400

    e = election.find_one({'_id' : ObjectId(election_id)})
    num_choices = len(e['choices'])
    if choice < 0 or choice >= num_choices:
        output['error'] = f'Invalid choice {choice}'
        return jsonify(output), 400
    
    new_ballot = {'choice' : choice, 'election_id' : election_id, 'voter_id' : voter_id }
    ballot.insert_one(new_ballot)
    election.update_one({'_id': election_id}, {"$inc": {f'choices.{choice}.count': 1}})

    output = { 'success': True, 'error': '' }
    return jsonify(output)