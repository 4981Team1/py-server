from flask import make_response, redirect, render_template, request, url_for, jsonify
from flask import current_app as app
from . import voter, ballot, election
from bson.objectid import ObjectId

# GET all elections' info: 
# http://localhost:5000/elections
# 
# GETs election info based on given ID
# http://localhost:5000/elections/<election_id>
@app.route('/elections/<election_id>', defaults={'details': None, 'choices': None}, methods = ['GET'])
def get_elections(election_id):
    output = {}

    # GET /elections
    if request.method == 'GET':
        election_id = request.args("")

        # Getting a single election
        # Check if there's an id parameter for looking up specific election
        if election_id:
            filt = {"_id": ObjectId(election_id)}

            # Check if there's an election with the corresponding ID
            if election.count_documents(filt, limit=1) != 0: 
                found = election.find_one(filt)
                output = {
                    '_id': str(found['_id']),
                    'details': found['details'],
                    'choices': found['choices']
                    }
        
        # Getting all elections
        # No id parameter means getting all elections info instead
        else:
            elections = election.find()
            output = [{
                '_id': str(election['_id']),
                'details': election['details'],
                'choices': election['choices']} for election in elections]

    print(output)
    return jsonify(output)

# POST create a new election
# /elections
# Incoming JSON data:
# { details="", choices=[]}
# e.g choices=["a", "b", "c"]
@app.route('/elections', methods = ['POST'])
def post_elections():
    output = {
            '_id': "",
            'success': False
        }

    # POST /elections
    if request.method == 'POST':
        details = request.json["details"]
        choices = request.json["choices"]

        # Create new election if details and choices exist
        if details and choices: 
            output = insert_election(details, choices)
    
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

    output = {}

    new_choices = [{
        'option': str(choice),
        'count': 0} for choice in choices]
    insert = { 'choices': new_choices, 'details': details }
    new_elec = election.insert_one(insert)
    
    # Check if the new election is inserted successfully
    filt = {"_id": ObjectId(new_elec.inserted_id)}
    new = election.find_one(filt)
    output = {
        '_id': str(new['_id']),
        'success': True
    }

    return output

