from flask import current_app as app
from . import voter, ballot, election

@app.route('/electionstest')
def electionstest():
    return "<h1>Welcome to elections</h1>"