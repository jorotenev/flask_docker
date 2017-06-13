# Purpose
This repo provides a minimal seed Flask application, which is ready to be deployed on Heroku. By using Vagrant in combination with Docker-Compose, it is possible to collaborate easily with other developers without worrying about differences in development environments.   
The structure of the Flask app is based mostly on [Miguel's Flasky](https://github.com/miguelgrinberg/flasky). 

# Requirements

If you plan to use PyCharm, there are some [known issues](https://youtrack.jetbrains.com/issue/IDEA-157108#tab=Comments) for some versions with loading the environmental variables from the .env file. PyCharm >=2016.2.3 doesn't seem to have issues with that.

# Usage
* Clone
`git clone git@github.com:jorotenev/flask_vagrant_docker.git`  
`cd flask_vagrant_docker`
* Rename the `env` file to `.env`  
`mv env .env`
* And then just do  
`docker-compose build`  
will pull the necessary docker images and install the python requirements.
*   `docker-compose up`  
will start the containers.  
* You can access the app from your browser at `localhost:5000`. Voila.  



# References
* [Miguel Grinberg's](https://github.com/miguelgrinberg/flasky)
* [Flask-Script + Gunicorn](http://stackoverflow.com/questions/14566570/how-to-use-flask-script-and-gunicorn)


# Contribute
Pull requests are more than welcomed :see_no_evil: