import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from acondbs.models import Log as LogModel
from acondbs.schema.connection import CountedConnection


class Log(SQLAlchemyObjectType):
    """Record of errors, etc."""

    class Meta:
        model = LogModel
        interfaces = (graphene.relay.Node,)
        connection_class = CountedConnection
