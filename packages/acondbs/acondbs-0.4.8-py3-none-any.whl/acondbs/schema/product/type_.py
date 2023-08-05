import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy.enums import _convert_sa_to_graphene_enum

# from acondbs.models import FieldType as FieldTypeModel  # enum
from acondbs.models import AttributeBoolean as AttributeBooleanModel
from acondbs.models import AttributeDate as AttributeDateModel
from acondbs.models import AttributeDateTime as AttributeDateTimeModel
from acondbs.models import AttributeFloat as AttributeFloatModel
from acondbs.models import AttributeInteger as AttributeIntegerModel
from acondbs.models import AttributeTime as AttributeTimeModel
from acondbs.models import AttributeUnicodeText as AttributeUnicodeTextModel
from acondbs.models import Field as FieldModel
from acondbs.models import Product as ProductModel
from acondbs.models import ProductFilePath as ProductFilePathModel
from acondbs.models import ProductRelation as ProductRelationModel
from acondbs.models import ProductRelationType as ProductRelationTypeModel
from acondbs.models import ProductType as ProductTypeModel
from acondbs.models import TypeFieldAssociation as TypeFieldAssociationModel
from acondbs.models import saEnumFieldType  # SQLAlchemy Enum
from acondbs.schema.connection import CountedConnection
from acondbs.schema.filter_ import PFilterableConnectionField

# FieldType is an enum. It is manually converted to a graphene enum
# here. An enum will be usually automatically converted. However, the
# automatic conversion causes an error if the automatic conversion
# of the same enum happens multiple times as described in
# https://github.com/graphql-python/graphene-sqlalchemy/issues/211.

# It is possible to use graphene.Enum.from_enum() as
# FieldType = graphene.Enum.from_enum(FieldTypeModel)

# However, instead, a private function _convert_sa_to_graphene_enum()
# is used here because this function desirably converts field names to
# the upper case, e.g., "UnicodeText" to "UNICODE_TEXT"
FieldType = _convert_sa_to_graphene_enum(saEnumFieldType)


class Product(SQLAlchemyObjectType):
    class Meta:
        model = ProductModel
        interfaces = (relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory


class ProductType(SQLAlchemyObjectType):
    """A product type"""

    class Meta:
        model = ProductTypeModel
        interfaces = (graphene.relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory


class ProductRelation(SQLAlchemyObjectType):
    """A relation from one product to another"""

    class Meta:
        model = ProductRelationModel
        interfaces = (graphene.relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory


class ProductRelationType(SQLAlchemyObjectType):
    """A type of relations between products"""

    class Meta:
        model = ProductRelationTypeModel
        interfaces = (graphene.relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory


class ProductFilePath(SQLAlchemyObjectType):
    class Meta:
        model = ProductFilePathModel
        interfaces = (relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory


class Field(SQLAlchemyObjectType):
    class Meta:
        model = FieldModel
        interfaces = (relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory
        exclude_fields = ("type_",)

    # Set "type_" manually to avoid an issue on enum as suggested in
    # https://github.com/graphql-python/graphene-sqlalchemy/pull/98#issuecomment-481497115
    # see also https://github.com/graphql-python/graphene-sqlalchemy/issues/211

    type_ = FieldType()


class TypeFieldAssociation(SQLAlchemyObjectType):
    class Meta:
        model = TypeFieldAssociationModel
        interfaces = (relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory


class AttributeUnicodeText(SQLAlchemyObjectType):
    """A unicode text attribute of a product"""

    class Meta:
        model = AttributeUnicodeTextModel
        interfaces = (relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory


class AttributeBoolean(SQLAlchemyObjectType):
    """A boolean attribute of a product"""

    class Meta:
        model = AttributeBooleanModel
        interfaces = (relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory


class AttributeInteger(SQLAlchemyObjectType):
    """An integer attribute of a product"""

    class Meta:
        model = AttributeIntegerModel
        interfaces = (relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory


class AttributeFloat(SQLAlchemyObjectType):
    """A float attribute of a product"""

    class Meta:
        model = AttributeFloatModel
        interfaces = (relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory


class AttributeDate(SQLAlchemyObjectType):
    """A date attribute of a product"""

    class Meta:
        model = AttributeDateModel
        interfaces = (relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory


class AttributeDateTime(SQLAlchemyObjectType):
    """A date time attribute of a product"""

    class Meta:
        model = AttributeDateTimeModel
        interfaces = (relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory


class AttributeTime(SQLAlchemyObjectType):
    """A time attribute of a product"""

    class Meta:
        model = AttributeTimeModel
        interfaces = (relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory
