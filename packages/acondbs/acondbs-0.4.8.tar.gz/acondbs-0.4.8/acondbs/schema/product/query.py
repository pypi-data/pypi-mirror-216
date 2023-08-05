import graphene

from acondbs.models import Field as FieldModel
from acondbs.models import Product as ProductModel
from acondbs.models import ProductRelation as ProductRelationModel
from acondbs.models import ProductRelationType as ProductRelationTypeModel
from acondbs.models import ProductType as ProductTypeModel
from acondbs.schema.filter_ import PFilterableConnectionField

from . import type_

all_products_field = PFilterableConnectionField(type_.Product.connection)
all_product_types_field = PFilterableConnectionField(type_.ProductType.connection)  # fmt: skip
all_product_relations_field = PFilterableConnectionField(type_.ProductRelation.connection)  # fmt: skip
all_product_relation_types_field = PFilterableConnectionField(type_.ProductRelationType.connection)  # fmt: skip
all_product_file_paths_field = PFilterableConnectionField(type_.ProductFilePath.connection)  # fmt: skip
all_fields_field = PFilterableConnectionField(type_.Field.connection)


def resolve_product(parent, info, **kwargs):
    filter = [getattr(ProductModel, k) == v for k, v in kwargs.items()]
    # e.g., [ProductModel.type_id == 1, ProductModel.name == 'map_001']

    return type_.Product.get_query(info).filter(*filter).one_or_none()


product_field = graphene.Field(
    type_.Product,
    product_id=graphene.Int(),
    type_id=graphene.Int(),
    name=graphene.String(),
    resolver=resolve_product,
)


def resolve_product_type(parent, info, **kwargs):
    filter = [getattr(ProductTypeModel, k) == v for k, v in kwargs.items()]
    # e.g., [ProductTypeModel.type_id == 1, ProductTypeModel.name == 'map']

    return type_.ProductType.get_query(info).filter(*filter).one_or_none()


product_type_field = graphene.Field(
    type_.ProductType,
    type_id=graphene.Int(),
    name=graphene.String(),
    resolver=resolve_product_type,
)


def resolve_product_relation(parent, info, **kwargs):
    filter = [getattr(ProductRelationModel, k) == v for k, v in kwargs.items()]
    return type_.ProductRelation.get_query(info).filter(*filter).one_or_none()


product_relation_field = graphene.Field(
    type_.ProductRelation,
    relation_id=graphene.Int(),
    resolver=resolve_product_relation,
)


def resolve_product_relation_type(parent, info, **kwargs):
    filter = [getattr(ProductRelationTypeModel, k) == v for k, v in kwargs.items()]
    return type_.ProductRelationType.get_query(info).filter(*filter).one_or_none()


product_relation_type_field = graphene.Field(
    type_.ProductRelationType,
    type_id=graphene.Int(),
    name=graphene.String(),
    resolver=resolve_product_relation_type,
)


def resolve_field(parent, info, **kwargs):
    filter = [getattr(FieldModel, k) == v for k, v in kwargs.items()]
    # e.g., [FieldModel.field_id == 1, FieldModel.name == 'contact']

    return type_.Field.get_query(info).filter(*filter).one_or_none()


field_field = graphene.Field(
    type_.Field,
    field_id=graphene.Int(),
    name=graphene.String(),
    resolver=resolve_field,
)
