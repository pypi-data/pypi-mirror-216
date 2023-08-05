import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from acondbs.models import WebConfig as WebConfigModel
from acondbs.schema.connection import CountedConnection


class WebConfig(SQLAlchemyObjectType):
    """Web configuration"""

    class Meta:
        model = WebConfigModel
        interfaces = (graphene.relay.Node,)
        connection_class = CountedConnection
