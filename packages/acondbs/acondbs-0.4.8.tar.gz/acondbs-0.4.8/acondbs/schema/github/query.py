import graphene

from acondbs.github.ops import get_github_oauth_app_info
from acondbs.schema.filter_ import PFilterableConnectionField
from acondbs.schema.funcs import get_git_hub_viewer_from_info

from . import type_

all_git_hub_orgs_field = PFilterableConnectionField(type_.GitHubOrg.connection)
all_git_hub_users_field = PFilterableConnectionField(type_.GitHubUser.connection)
all_git_hub_tokens_field = PFilterableConnectionField(type_.GitHubToken.connection)


def resolve_git_hub_o_auth_app_info(parent, info):
    info = get_github_oauth_app_info()
    return type_.GitHubOAuthAppInfo(
        client_id=info["client_id"],
        authorize_url=info["authorize_url"],
        redirect_uri=info["redirect_uri"],
    )


git_hub_o_auth_app_info_field = graphene.Field(
    type_.GitHubOAuthAppInfo, resolver=resolve_git_hub_o_auth_app_info
)


def resolve_git_hub_viewer(parent, info):
    user = get_git_hub_viewer_from_info(info)
    return user


git_hub_viewer_field = graphene.Field(type_.GitHubUser, resolver=resolve_git_hub_viewer)
