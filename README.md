# py-server
### Installing and setting up

1. Make sure to have MongoDB installed in your local machine. For OS-specific set-up instructions, please refer to this link: https://docs.mongodb.com/manual/administration/install-community/

   **Note:** If you prefer to use a GUI for managing MongoDB databases , we suggest checking out [Robo 3T](https://robomongo.org/download).

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



### Running the server

1. Go to the root directory.
2. Run the web app by running the deploy script again: `./deploy`
3. Another way to run the web app is to run it through a virtual environment or *venv* which should be already installed when running the deploy script for the first time. Activate/deactivate the virtual environment by running the following:
   * **Activate**:    `source venv/bin/activate`
   * **Deactivate/exit**: `deactivate`

While the venv is active, you can run the web app by typing in: `flask run`



### API

Refer to [API.md](./API.md) or to our SwaggerHub [API doc](https://app.swaggerhub.com/apis-docs/agoryelov/vote-api/1.0.0)

