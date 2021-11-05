# sudo service postgresql restart
# pg_lsclusters 11 main start
# psql -p 5532 -U postgres
# psql -h 0.0.0.0 -U postgres mashroodb


CREATE DATABASE mashroodb;
ALTER USER postgres WITH PASSWORD 'grutil001';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mashroodb TO postgres;
GRANT ALL PRIVILEGES ON DATABASE bankapidb TO postgres;
