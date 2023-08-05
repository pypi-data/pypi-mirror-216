"""Declare SQLAlchemy ORM models

In this package, ORM (Object-relational mapping) models are declared.
One model is mapped to one table in the DB. Models are declared as
Python classes inheriting the Model class in Flask-SQLAlchemy.

"Declaring Models" in Flask-SQLAlchemy doc:
https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

"Declare a Mapping" in SQLAlchemy doc:
https://docs.sqlalchemy.org/en/14/orm/tutorial.html#declare-a-mapping

"""
__all__ = [
    'AccountAdmin',
    'GitHubOrg',
    'GitHubOrgMembership',
    'GitHubToken',
    'GitHubUser',
    'Log',
    'FieldType',
    'saEnumFieldType',
    'AttributeBoolean',
    'AttributeDate',
    'AttributeDateTime',
    'AttributeFloat',
    'AttributeInteger',
    'AttributeTime',
    'AttributeUnicodeText',
    'Field',
    'Product',
    'ProductFilePath',
    'ProductRelation',
    'ProductRelationType',
    'ProductType',
    'TypeFieldAssociation',
    'WebConfig',
    'init_app',
]


from flask import Flask

from .account import AccountAdmin
from .github import GitHubOrg, GitHubOrgMembership, GitHubToken, GitHubUser
from .misc import Log
from .product import FieldType  # enum
from .product import saEnumFieldType  # SQLAlchemy Enum
from .product import (
    AttributeBoolean,
    AttributeDate,
    AttributeDateTime,
    AttributeFloat,
    AttributeInteger,
    AttributeTime,
    AttributeUnicodeText,
    Field,
    Product,
    ProductFilePath,
    ProductRelation,
    ProductRelationType,
    ProductType,
    TypeFieldAssociation,
)
from .web import WebConfig


def init_app(app: Flask) -> None:
    """Initialize the Flask application object

    This function is called by `create_app()` of Flask

    Parameters
    ----------
    app : Flask
        The Flask application object, an instance of `Flask`
    """

    _add_owners_to_db_as_admins(app)
    # remove_git_hub_tokens_with_invalid_decryption_key(app)


def _add_owners_to_db_as_admins(app: Flask) -> None:
    import sqlalchemy

    from acondbs.db.sa import sa

    # Test if tables are defined. For example, tables are not defined
    # when a migration version is being created.
    with app.app_context():
        try:
            _ = AccountAdmin.query.all()
        except sqlalchemy.exc.OperationalError:
            return

    with app.app_context():
        owners = app.config.get("ACONDBS_OWNERS_GITHUB_LOGINS", "")
        # e.g., "octocat,dojocat"

        owners = {e.strip() for e in owners.split(",")}
        # e.g., {"octocat", "dojocat"}

        # remove empty strings
        owners = {e for e in owners if e}

        # sort so that "admin_id" is deterministic in tests
        owners = sorted(owners)

        for owner in owners:
            if (
                admin := AccountAdmin.query.filter_by(git_hub_login=owner).one_or_none()
            ) is None:
                admin = AccountAdmin(git_hub_login=owner)
                sa.session.add(admin)
        sa.session.commit()


def remove_git_hub_tokens_with_invalid_decryption_key(app: Flask) -> None:
    from acondbs.db.sa import sa

    with app.app_context():
        token_ids = [e[0] for e in sa.session.query(GitHubToken.token_id).all()]
        for token_id in token_ids:
            try:
                token = GitHubToken.query.filter_by(  # noqa: F841
                    token_id=token_id
                ).one()
            except ValueError:
                sql = f"delete from {GitHubToken.__tablename__} where token_id={token_id};"
                sa.engine.execute(sql)
