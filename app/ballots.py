from flask import current_app as app
from . import voter, ballot, election

@app.route('/ballotstest')
def ballotstest(v):   
    return "<h1>Welcome to ballots<h1>"