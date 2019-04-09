# flask_docker
This repo contains skeleton code for a barebone Flask app. The app can be ran via docker-compose too.

# Run
1. You need an `.env` file at the root of the repo with the following contents 
```
FLASK_ENV=development
SECRET_KEY=somesecret
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=8080
```
The `FlASK_RUN_x` are optional.
## To run with docker-compose
The `pipenv` image is used. Since there's only a `latest` tag, below I reference a specific [image build](https://hub.docker.com/r/kennethreitz/pipenv/builds/btyyzsg7po9kakddpc2lsrm/).
* `docker image pull kennethreitz/pipenv@sha256:e5ee93444c52f36791f799e611d01b6950d819c676723a13c160a918c7f2d786`
* `docker-compose up`
## Manually
* Install [pipenv](https://github.com/pypa/pipenv#installation)
* `$ pipenv install`
* `$ pipenv shell`
* To run the flask app (see below the Note for PyCharm users)
`$ flask run`

#### Note for PyCharm users
When running via PyCharm and assuming that pipenv is used, you need to select the correct Python [interpreter](https://www.jetbrains.com/help/pycharm/configuring-language-interpreter.html).
```
$ pipenv shell
(some_app-tKuPD0ya) $ which python
/home/georgi/.local/share/virtualenvs/some_app-tKuPD0ya/bin/python
```

When creating a run configuration, select as "Module name" (the default is to execute a script) `flask` and as Parameters `run`. For older versions of the IDE, see [this](https://stackoverflow.com/questions/22081065/create-a-pycharm-configuration-that-runs-a-module-a-la-python-m-foo)

## Test
Example for `unittest`.  
To run them via PyCharm
* You need the '.env_test' file placed in the repo root with the `SECRET_KEY` and `FLASK_ENV=testing` env vars  

```
FLASK_ENV=testing
SECRET_KEY=somesecret
```
* Create a new Python test run configuration with the `/tests` as the __Path__ target and the root of the repo as a working directory
