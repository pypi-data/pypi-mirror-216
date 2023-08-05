import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from acondbs.models import GitHubOrg as GitHubOrgModel
from acondbs.models import GitHubOrgMembership as GitHubOrgMembershipModel
from acondbs.models import GitHubToken as GitHubTokenModel
from acondbs.models import GitHubUser as GitHubUserModel
from acondbs.schema.connection import CountedConnection
from acondbs.schema.filter_ import PFilterableConnectionField


class GitHubOAuthAppInfo(graphene.ObjectType):
    client_id = graphene.String()
    authorize_url = graphene.String()
    redirect_uri = graphene.String()


class AuthPayload(graphene.ObjectType):
    token = graphene.String()


class GitHubToken(SQLAlchemyObjectType):
    class Meta:
        model = GitHubTokenModel
        interfaces = (relay.Node,)
        exclude_fields = [
            "token",
        ]
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory

    token_masked = graphene.String()

    def resolve_token_masked(parent, info):
        return "X" * 15


class GitHubUser(SQLAlchemyObjectType):
    class Meta:
        model = GitHubUserModel
        interfaces = (relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory


class GitHubOrg(SQLAlchemyObjectType):
    class Meta:
        model = GitHubOrgModel
        interfaces = (relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory


class GitHubOrgMembership(SQLAlchemyObjectType):
    class Meta:
        model = GitHubOrgMembershipModel
        interfaces = (relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory
