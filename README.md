# flask_docker
This repo contains skeleton code for a barebone Flask app. The app can be ran via docker-compose too.

# Run

## To run with docker-compose
The `pipenv` image is used. Since there's only a `latest` tag, below I reference a specific [image build](https://hub.docker.com/r/kennethreitz/pipenv/builds/btyyzsg7po9kakddpc2lsrm/).
* `docker-compose up`
## Manually
* Install [pipenv](https://github.com/pypa/pipenv#installation)
* `$ pipenv install`
* pipenv will output the folder of the new interpreter
* In PyCharm, add a new interpreted and point to the folder from above + Scripts/pyhton
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

**Make sure to set the Working directory folder in the run config to the project folder.**
## Test
Example for `unittest`.  
To run them via PyCharm
* You need the '.env_test' file placed in the repo root with the `SECRET_KEY` and `FLASK_ENV=testing` env vars  

```
FLASK_ENV=testing
SECRET_KEY=somesecret
```
* Create a new Python test run configuration with the `/tests` as the __Path__ target and the root of the repo as a working directory
