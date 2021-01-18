# py-server
A test web server written using Flask/Python and prints 'Hello World'.

###How to set up/run

1) Make sure to have virtualenv installed:

​	a) Install **pip** first

    sudo apt-get install python3-pip

​	b) Install **virtualenv** using pip3

    sudo pip3 install virtualenv 

​	c) Go to the root directory and create a virtual environment 

    cd py-server
    virtualenv venv 

>you can use any name insted of **venv**



Now your virtual environment is installed! To activate/deactivate it, do the following:

**Activate**:    

    source venv/bin/activate

**Deactivate/exit**:

    deactivate

2) While the virtual environment or 'venv' is active, run the following commands to install Flask and other
dependencies

    pip install flask

3) To run the Flask web app, type in the command below

    flask run