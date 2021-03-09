from flask import current_app as app
from . import voter, ballot, election

@app.route('/voterstest')
def voterstest():
    return "<h1>Welcome to voters</h1>"

# TODO: Create Voter - POST /voters
# TODO: Get Voter - GET /voters/:id
# TODO: Get Elections for a Voter - GET /voters/:voterId/elections
# TODO: Add Election for a Voter - POST /voters/:voterId/elections
# TODO: Remove Election from a Voter - DELETE /voters/:voterId/elections/:electionId
# TODO: Delete Voter - DELETE /voters/:id

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
            votable.append(eid);
        
        # If a ballot made by the user EXISTS for the current election,
        # add electionID into "non-votable" elections list.
        else:
            non_votable.append(eid)

    output = {
        'votable' : votable
        'non_votable' : non_votable
    }
            
    
    return output;