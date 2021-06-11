# CPSC 304 Team 49: BiblioStream

BiblioStream is an application utilizing a relational database focused on providing users with the ability to check the availability of shows/movies on various streaming platforms using a number of other parameters such as actors, language, country, etc.

## Environment Setup

In order to run this application, a Python environment is necessary. In order to make dependency installation easier, this project utilizes the `pip` package [`pipenv`](https://pipenv.pypa.io/en/latest/).

From the root of the project:

1. Run `pip install pipenv`
2. Run `pipenv install`

This creates a virtual environment and installs all the packages required by the project

To add new dependencies, instead of running `pip install ${dependency}`, instead run:

```
pipenv install ${dependency}
```

This should create an entry in the `Pipfile` and automatically update the `Pipfile.lock`.

_Note: Please push these files whenever any new dependencies are added in order for other developers to have the latest required dependencies installed_

To reset the python virtual environment, run the following command in a bash shell:

```
./reset-pipenv.sh
```

## Running the application

To launch the application, from the root of the project, run:

```
pipenv run python src/main.py ${filepath-to-dbconfig.yaml}
```

_Note: Please provide filepath to the dbconfig.yaml containing credentials to connect to postgres database_

## Acknowledgements

This project is conceived and created for CPSC 304 by:

- Anam Hira
- Keshav Gupta
- Yaash Jain
