# Purpose
This repo provides a minimal,`docker-compose`-ready, Flask application, which is ready to be deployed to Heroku.

The structure of the Flask app is based mostly on [Miguel's Flasky](https://github.com/miguelgrinberg/flasky).

# Limitations
* You can't run the Flask app on a windows machine without docker because of the `gunicorn`
dependency. The dependency is only used if `APP_MODE` is set to `production`. The limitation doesn't apply if you run the app with docker :)


# Usage
* Clone
  * `git clone git@github.com:jorotenev/flask_docker.git`
  * `mv flask_docker <YOUR_PROJECT_NAME>`
  * `cd <YOUR_PROJECT_NAME>`
  * `rm -rf .git && git init` - make a fresh git repo for your project

Then you can either use the terminal or PyCharm
to run the app:

### With just the terminal

* Rename the `env` file to `.env`
`mv env .env` (if you run in production, remember to pass explicitly the environment variables from this file)
* And then just do
`docker-compose build`
This will pull the necessary docker images
*   `docker-compose up`
will start the Flask app
* You can access the app from your browser at `localhost:5000`
* Voila.

### With PyCharm and Docker Compose
* `Pycharm -> Settings -> Project Interpreter -> (gears button) -> Add remote -> Docker Compose`
* Select Docker Compose and then click "New" to set up a New connection to Docker (use the defaults; leaving the certs folder empty worked for me). Click ok to go back to the `Configure Remote Python Interpreter`
* Make sure the `docker-compose.yaml` from this repo is added under the Configuration file(s)
* Choose `web` as a Service. Press ok
* Add a new run configuration (Run -> Edit configurations)
  * Select the `manage.py` file as the Script file
  * Set `runserver` for the Script parameters
  * Set the `APP_MODE=development` and `SECRET_KEY=<whatever>` environment variables
* Press ok. If you **Run** this configuration, you will start the flask app through PyCharm. You can also put breakpoints and **Debug** :)



## Running tests
### From the terminal

* `docker-compose run --rm web python manage.py test`

### From PyCharm
* Add a new run configuration and select Python tests -> Unittests
* Select the `tests/` folder from this repo as `Target->Path`
* Set the `APP_MODE=testing` and the `SECRET_KEY=<..>` env variables
* Run this configuration to run the tests
* Alternatively, instead of adding Unittests you can add a new Python run configuration and instead of setting `runserver` as the script parameter, set `test`.


# Deploy to Heroku
[Heroku docs](https://devcenter.heroku.com/articles/git#creating-a-heroku-remote)

* install and login into [heroku-cli](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
* `heroku create` - creates a new heroku app
* make changes to the app & commit them
* `heroku config:set APP_MODE=production`
* `heroku config:set SECRET_KEY=<something really secret>`
* `git push heroku master`

# References
* [Miguel Grinberg's](https://github.com/miguelgrinberg/flasky)
* [Flask-Script + Gunicorn](http://stackoverflow.com/questions/14566570/how-to-use-flask-script-and-gunicorn)


# Contribute
Pull requests are more than welcomed :see_no_evil: