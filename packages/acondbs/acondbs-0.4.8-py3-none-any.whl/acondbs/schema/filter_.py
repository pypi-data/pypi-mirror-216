"""define filters

Define filters by using graphene-sqlalchemy-filter:
https://github.com/art1415926535/graphene-sqlalchemy-filter

example:
https://github.com/art1415926535/graphene-sqlalchemy-filter/blob/1.10.2/examples/clients_and_records/filters.py

"""
import graphene
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet

from acondbs.models import GitHubToken as GitHubTokenModel
from acondbs.models import GitHubUser as GitHubUserModel
from acondbs.models import Product as ProductModel
from acondbs.models import ProductType as ProductTypeModel


class ProductFilter(FilterSet):
    type_name = graphene.String()

    class Meta:
        model = ProductModel
        fields = {
            "type_id": [
                "eq",
            ],
        }

    @staticmethod
    def type_name_filter(info, query, value):
        # "Filters that require join":
        # https://github.com/art1415926535/graphene-sqlalchemy-filter/tree/1.10.2#filters-that-require-join
        query = query.join(ProductTypeModel)
        filter_ = ProductTypeModel.name == value
        return query, filter_


class ProductTypeFilter(FilterSet):
    class Meta:
        model = ProductTypeModel
        fields = {}


class GitHubTokenFilter(FilterSet):
    class Meta:
        model = GitHubTokenModel
        fields = {
            "scope": [
                "ilike",
            ],
        }


class GitHubUserFilter(FilterSet):
    org_member = graphene.Boolean()

    class Meta:
        model = GitHubUserModel
        fields = {}

    @staticmethod
    def org_member_filter(info, query, value):
        filter_ = GitHubUserModel.memberships.any() if value else None
        return query, filter_


class PFilterableConnectionField(FilterableConnectionField):
    filters = {
        ProductModel: ProductFilter(),
        ProductTypeModel: ProductTypeFilter(),
        GitHubTokenModel: GitHubTokenFilter(),
        GitHubUserModel: GitHubUserFilter(),
    }
