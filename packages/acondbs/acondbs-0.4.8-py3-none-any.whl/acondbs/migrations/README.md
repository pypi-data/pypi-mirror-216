# Alembic Migration Environment

This folder is the [Alembic Migration Environment](https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment).

## Example

```bash
# cd to one dicrectory above this package, i.e., three directories above from here

export FLASK_APP="acondbs:create_app('$PWD/acondbs/tests/sample/config.py')"
export FLASK_DEBUG=1

cd acondbs/

rm -f tests/sample/product.sqlite3

flask db upgrade

flask import-csv tests/sample/csv/

flask db migrate -m 'message'
# flask db revision -m 'message' # create an emtpy migration

# new migration version is created in acondbs/migrations/versions/

# edit it if necessary, e.g., use op.alter_column()

flask db upgrade

flask export-csv tests/sample/csv/
```
