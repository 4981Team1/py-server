# py-server
A basic Flask web app that does the following:

* Shows all the current users: `localhost:5000`
* Creates a new user based on given URL parameters: `localhost:5000?user=[USERNAME]&email=[EMAIL]`

For example, going to `localhost:5000?user=mikhaela&email=test@email.com` creates a user named "mikhaela" with "test@email.com" as their email.

### Installing and setting up

1. Make sure to have MySQL server and client installed in your machine. For OS-specific set-up instructions, please refer to this link: https://dev.mysql.com/doc/mysql-getting-started/en/

   **Note**: If it's your first time setting up the MySQL server, you'll be prompted to enter a password for the server itself. Make sure to remember this password.

2. Run MySQL client. Create a local MySQL database named **testflask**. You can copy the first two lines of `database.sql` for the queries.

3. Clone this repository

```
git clone https://github.com/4981Team1/py-server.git
```

3. On your terminal, make and run the deploy script

```
$ cd py-server
$ make deploy
$ ./deploy
```

This deploy script will install [venv](https://docs.python.org/3/library/venv.html) and the required dependencies to run the web app.

4. Duplicate the file **.env.example** and rename it as `.env`. 

5. Inside .env, replace **[USER]** and **[PASSWORD]** with the same credentials you use to run MySQL client. For example, if your username is "root" and your password is "password":

   ```
   SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:password@localhost/testflask
   ```

   

### Running the web app

1. Go to the root directory.
2. Run the web app by running the deploy script again: `./deploy`
3. Another way to run the web app is to run it through a virtual environment or *venv* which should be already installed when running the deploy script for the first time. Activate/deactivate the virtual environment by running the following:
   * **Activate**:    `source venv/bin/activate`
   * **Deactivate/exit**: `deactivate`

While the venv is active, you can run the web app by typing in: `flask run`