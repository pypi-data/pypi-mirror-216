import graphene

from acondbs.models import Log as LogModel
from acondbs.schema.filter_ import PFilterableConnectionField

from . import type_

all_logs_field = PFilterableConnectionField(type_.Log.connection)


def resolve_log(parent, info, **kwargs):
    filter = [getattr(LogModel, k) == v for k, v in kwargs.items()]
    return type_.Log.get_query(info).filter(*filter).one_or_none()


log_field = graphene.Field(type_.Log, id_=graphene.Int(), resolver=resolve_log)
