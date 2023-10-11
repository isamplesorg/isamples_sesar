# iSamples SESAR
Deep integration between the SESAR Postgresql schema and the iSamples data model.

## Environment setup
To set up python, follow the instructions in [the python setup guide](docs/python_setup.md.html).

## Poetry setup
Follow the installation instructions in [the poetry documentation](https://python-poetry.org/docs/#installation).

## Activate the python virtual environment
`poetry shell`, then once it's activated `poetry install`

## Setup the database
Create the database

```
psql postgres
CREATE DATABASE isb_sesar;
CREATE USER isb_sesar WITH ENCRYPTED PASSWORD 'some_password';
GRANT ALL PRIVILEGES ON DATABASE isb_sesar TO isb_sesar;
```
Import the dump file into the newly created database

```
pg_restore -d isb_sesar ./sesardb-schemaonly.dump
```

## Run the main script
`python main.py -d "postgresql+psycopg2://isb_writer:password@localhost/isb_sesar"`

## Run the test script
`pytest --db-url="postgresql+psycopg2://username:password@DB_HOST/DB_NAME"`