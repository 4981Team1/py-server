from flask import current_app as app
from . import voter, ballot, election

@app.route('/voterstest')
def voterstest():
    return "<h1>Welcome to voters</h1>"

# Helper function for finding elections a user is eligible for 
# but hasn't voted on yet.
# Returns array of votable elections' electionIDs
def find_votable_elections(elecs, vid):
    """
    Helper function for finding elections a user is eligible for but hasn't voted on yet.\n
    Returns:\n
    array of votable elections' electionIDs
    """

    output = []
    for eid in elecs:
        elec = election.find_one({'_id' : ObjectId(eid)})
        filt = {'election_id' : eid, 'voter_id' : vid}

        if ballot.count_documents(filt, limit=1) == 0:
            output.append(eid);
    
    return output;