# Purpose
This repo provides a minimal seed Flask application, which is ready to be deployed on Heroku. By using Vagrant in combination with Docker-Compose, it is possible to collaborate easily with other developers without worrying about differences in development environments.   
The structure of the Flask app is based mostly on [Miguel's Flasky](https://github.com/miguelgrinberg/flasky). 

# Requirements
You need VirtualBox &  Vagrant.
* `sudo apt-get install virtualbox -y`
* `sudo apt-get install vagrant -y`

If you plan to use PyCharm, there are some [known issues](https://youtrack.jetbrains.com/issue/IDEA-157108#tab=Comments) for some versions with loading the environmental variables from the .env file. PyCharm >=2016.2.3 doesn't seem to have issues with that.

# Usage
* After installing VirtualBox and Vagrant, clone the repo and go to it  
`git clone git@github.com:jorotenev/flask_vagrant_docker.git`  
`cd flask_vagrant_docker`
* Rename the `env` file to `.env`  
`mv env .env`
* And then just do  
`vagrant up`  
* Login into the virtual machine with  
`vagrant ssh`  
 You will be in the project folder  
*  `docker-compose build`  
will pull the necessary docker images and install the python requirements.
*   `docker-compose up`  
will start the containers.  
* You can access the app from your browser at `192.168.33.10:5000`. Voila.  

The `vagrant up` command will download a vagrant box, launch a virtual machine from it and provision it with the `vagrant_setup.sh` script. The script installs docker, docker-compose, the heroku-toolkit. It will also add couple of handy aliases in the `.bashrc` of the guest machine. They will be available in the guest machines' terminal by simply typing `shell`, `drop_and_init_db`, `init_db` or `drop_db` when in the project folder - these commands will be ran against the `manage.py` file using the`web` container, defined in the `docker-compose.yaml`. 
 `shell` will open a python interpreter with the Flask app available - e.g. from within the virtual machine it's possible to do  
 `vagrant@ubuntu-14:/home/georgi/Projects/flask_seed$ shell`  
 `>>> models.User.query.all()`  
 `["user1@gmail.com", "user2@gmail.com"]`

 `init_db` and `drop_db` initialise the db or drop it. `drop_and_init_db` first drops the db and then inits it :)  

The `docker-compose build` command will download any necessary images (e.g. for postgres db or redis) and `docker-compose up` will launch the containers defined in the `docker-compose.yaml`.

# How to setup PyCharm
* Make sure that on top of the Vagrantfile, you set the path to your PyCharm's system folder. For example, if you are using Ubuntu, and using PyCharm 2016.2, you'd do:  
`pycharm_folders =  ["~/.PyCharm2016.2/system/tmp"]`  (array is used in case you have more than one PyCharm installations.
* If the virtual machine is already running after changing the variable, do `vagrant reload`  
* Then open PyCharm, `File->Settings->Project Interpeter->Add Remote` and select `Docker-Compose`. 
	* In the window, press __New__ to create a new Server. 
	* Add `tcp://192.168.33.10:2375`, where the IP is the same as the one defined in the Vagrantfile. Press Ok to add the server. 
	* Then for the __Configuration__ select the `docker-compose.yaml` from the project directory. 
	* For service name, enter `web` (that's the name of the service, as defined in the docker-compose.yaml file and it'd be the one used to run our flask app).
	* For python path just enter `python`.
	* Press Ok to conclude the process of adding the remote interpreter.

Please note, that for PyCharm to work together with the Docker-Compose inside Vagrant, we took some shortcuts. In the Vagrantfile we set that our host project folder should be synced to the same path on the guest machine. Meaning, that if on your host machine, the flask project is at `/home/me/flask_app/`, then the same path will exist on the guest machine with the same content as the one on the host machine. Also, the PyCharm's system folder will exist on the virtual machine. [link 1](https://youtrack.jetbrains.com/issue/PY-19023), [link 2](http://stackoverflow.com/a/36370813/4509634) 

## Run/Debug configuration
It is possible to run the python app by ssh-ing into the virtual machine and doing `docker-compose up` - this will start all containers and show us their logs. However, that's not optimal. It'd be nice if we can use PyCharm as if we are using the host interpreter.  
* Go to `Run->Edit Configurations`

* Either edit an existing __Python__ run configuration or add a new one, with the following settings:  
Script: choose the `manage.py` from the project.  
Script parameters: `runserver`   (as specified in `manage.py` via Flask-Script)  
Pyhton Interpreter: Select the Remote Python Docker Compose interpreter you just added.  

Press Apply. Now you can run/debug the app by simply selecting the run configuration from the top right corner of PyCharm and then pressing the Run or Debug button. Note, that you can duplicate the configuration and replace the `runserver` parameter with either `init_db`, `drop_db`, `drop_and_init_db` or even `test`. This way, you can initialise or drop the db straight from the IDE; `test` will run the tests from the tests/ folder.


## Tests
PyCharm has nice interface to run tests and get visual feedback on their output.  
To use it, go to the Edit Configurations menu again, and press the plus button. Select Python Tests -> UnitTests.

Choose the `Folder` option and then select the `tests/` folder of the project. Add as a pattern test_*.py, which will run the tests in all files starting with `test_` and put the checkbox on `Run subclasses of UnitTest only`.  
In the Run configurations, the test configuration you just added is now available.

## Environment variables 
In the `env` file it is indicated which vars should be set in which environment.  
`APP_SETTINGS` should be set in all environments - the allowed values are `development` `testing` `staging` `production`.  
To enable __Flask-Cache__, just set the `CACHE_REDIS_PORT` variable in the config.py to `6379`. The cache is initalisied in `app/__init__.py -> initFlaskCache()` - there you can set a different cache backend. Flask-Cache with Redis can be initialised in different ways, depending on what env vars you pass to it - e.g. you can just give it a host name and port, or just the backend url. This is useful because when developing locally, we can use the redis from Docker, on production we can use the url given to us from the environemnt.  
__Rollbar__: to enable the exception handling, just set the `ROLLBAR_ACCESS_TOKEN`. If not set, rollbar will not be initialised, and when `app/utils.py -> [logException() | logMessage()]` are used, they will just be `print()`-ed

# Deploy to Heroku
Deploying to Heroku is easy. All you need to do is ssh into the virtual machine:  
* `vagrant ssh`  
* Then login to Heroku. You will be prompted to enter your Heroku account credentials.  
`heroku login`  
* The project folder should have a git repo. If it doesn't make one via 
`git init`  
`git add .` (make sure that you renamed the `env` file to `.env`, otherwise it will be version controlled by git)  
`git commit -m "First commit"`
* Then you need to create a Heroku app    
`heroku create`
* Now it is a good time to go to the Heroku dashboard, open the app you just made, and set the environment variables. `APP_SETTINGS` and `SECRET_KEY` are mandatory. 
* Install add-ons  
The app assumes that some add-ons are installed on Heroku:  
    * Heroku Postgres - the database. The `DATABASE_URL` will be set automatically, after installing the [Heroku Postgres add-on](https://elements.heroku.com/addons/heroku-postgresql)
    
    The app supports the following add-ons (optional add-ons):  
	* Heroku Redis - for caching. Install the [Heroku Redis add-on](https://elements.heroku.com/addons/heroku-redis). The `REDIS_URL` env variable will be set automatically.
	* Rollbar - for exception handling.  Register with Rollbar/install the add-on and set the `ROLLBAR_ACCESS_TOKEN`. 

* And then you can deploy with  
`git push heroku master`  
The `heroku create` command added a remote to your git repo.

Note, that the Procfile and runtime.txt are needed when deploying to Heroku, in addition to requirements.txt. The Procfile defines the servies, the runtime specifies the python version and the requirements.txt the needed packages.  
`gunicorn_wsgi.py` defines the production server. `gunicorn.ini` is the [config file](http://docs.gunicorn.org/en/stable/settings.html#config-file) for Gunicorn.

# SSL
Check out [Sabayon](https://github.com/dmathieu/sabayon) - it let's you add a Let's Encrypt certificate to your website for free.
You deploy the Sabayon app to a different dyno, which set's the ACMA challenge token on our Flask dyno. In the app/main/views.py there's code to handle the challenge.
# TODO
* Package the web (app) container to an image.
* [PyCharm Problem](https://youtrack.jetbrains.com/issue/IDEA-157108#tab=Comments) Changing the .env file requires restarting PyCharm for the changes to take effect for versions below PyCharm 2016.2.3
# References
* [Miguel Grinberg's](https://github.com/miguelgrinberg/flasky)
* [Flask-Script + Gunicorn](http://stackoverflow.com/questions/14566570/how-to-use-flask-script-and-gunicorn)
