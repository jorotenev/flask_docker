# flask_docker
This repo contains skeleton code for a barebone Flask app. The app can be ran via docker-compose too.

# Run
## To run with docker-compose
The `pipenv` image is used. Since there's only a `latest` tag, below I reference a specific [image build](https://hub.docker.com/r/kennethreitz/pipenv/builds/btyyzsg7po9kakddpc2lsrm/).
* `docker image pull kennethreitz/pipenv@sha256:e5ee93444c52f36791f799e611d01b6950d819c676723a13c160a918c7f2d786`
* `docker-compose up`
## Manually
* Install [pipenv](https://github.com/pypa/pipenv#installation)
* `$ pipenv install`
* `$ pipenv shell`
* make an `.env_dev` file at the root of the repo with the following structure
```
SECRET_KEY=not-that-secret
```
* Set the following environmental variables
```
DOT_ENV_FILE=.env_dev
FLASK_ENV=development
```
* To run the flask app (see below the Note for PyCharm users)
`$ flask run --host=0.0.0.0`

#### Note for PyCharm users
When running via PyCharm and assuming that pipenv is used, you need to select the correct Python [interpreter](https://www.jetbrains.com/help/pycharm/configuring-language-interpreter.html).
```
$ pipenv shell
(para_api-tKuPD0ya) $ which python
/home/georgi/.local/share/virtualenvs/para_api-tKuPD0ya/bin/python
```

When creating a run configuration, select as "Module name" (the default is to execute a script) `flask` and as Parameters `run --host=0.0.0.0`. For older versions of the IDE, see [this](https://stackoverflow.com/questions/22081065/create-a-pycharm-configuration-that-runs-a-module-a-la-python-m-foo)

## Test
`unittest` is used for the tests.
To run them via PyCharm
* You need the '.env_test' file placed in the repo root with
```
SECRET_KEY=not-that-secret
```

* Create a new Python test run configuration with the `/tests` as the __Path__ target and the root of the repo as a working directory
* Run the configuration with `FLASK_ENV=testing`