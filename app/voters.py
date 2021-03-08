from flask import current_app as app
from . import voter, ballot, election

@app.route('/voterstest')
def voterstest():
    return "<h1>Welcome to voters</h1>"