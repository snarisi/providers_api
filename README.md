## Providers API

To create the database:

```
psql -h localhost -d postgres
postgres=# create database providers_api;
```

To migrate the database:

```
make migrate
```

To seed the database:

```
make seed-database
```

To install dependencies:

```
make setup
```

To run:

```
make run
```

To run tests:

```
make test
```
