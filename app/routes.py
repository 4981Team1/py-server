from flask import make_response, redirect, render_template, request, url_for
from flask import current_app as app
from .models import db, Users

# # Turns debugging on (auto reload)
# app.run(debug=True)

@app.route('/', methods=['GET'])
def user_records():
    """Create a user via query string parameters."""
    username = request.args.get('user')
    email = request.args.get('email')
    if username and email:
        existing_user = Users.query.filter(
            Users.username == username or Users.email == email
        ).first()
        if existing_user:
            return render_template(
                'update_user.html',
                title = "Update User",
                username = username,
                email = email)
            # return make_response(
            #     # Ask if you would like to update or delete
            #     f'{username} ({email}) already created!'
            # )
        new_user = Users(
            username=username,
            email=email
        )  # Create an instance of the User class
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()  # Commits all changes
        redirect(url_for('user_records'))
    return render_template(
        'users.html',
        users=Users.query.all(),
        title="Show Users"
    )

@app.route('/update_user', methods=['POST'])
def update_user():
    id = Users.id
    username = request.form['username']
    email = request.form['email']
    if username and email:
        existing_user = Users.query.filter(
            Users.id == id
        ).first()
        existing_user.username = username
        existing_user.email = email
        db.session.commit() # Updates username and email
    return render_template(
        'users.html',
        users=Users.query.all(),
        title="Show Users"
    )

@app.route('/delete_user', methods=['POST'])
def delete_user():
    id = Users.id
    user = Users.query.filter(
        Users.id == id
    ).first()
    db.session.delete(user)
    db.session.commit() # Deletes user
    return render_template(
        'users.html',
        users=Users.query.all(),
        title="Show Users"
    )
