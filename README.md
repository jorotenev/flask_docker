
# Run
* Install [pipenv](https://github.com/pypa/pipenv#installation)
* `$ pipenv install`
* `$ pipenv shell`
* make an `.env_dev` file at the root of the repo with the following structure
```
APP_STAGE=development
SECRET_KEY=not-that-secret
```
* Set the following environmental variables
```
DOT_ENV_FILE=.env_dev
FLASK_APP=manage.py # the "new" way flask discovers apps
```
* To run the API (see below the Note for PyCharm users)
`$ flask run --host=0.0.0.0`

#### Note for PyCharm users
When running via PyCharm and assuming that pipenv is used, you need to select the correct python interpreter.
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
APP_STAGE=testing
SECRET_KEY=not-that-secret
```
* Create a new Python test run configuration with the `/tests` as the __Path__ target and the root of the repo as a working directory
* Run the configuration