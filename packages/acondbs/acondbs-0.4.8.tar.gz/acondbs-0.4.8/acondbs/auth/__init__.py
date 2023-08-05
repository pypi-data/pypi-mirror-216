from typing import Optional

from flask import request

from acondbs.models import AccountAdmin, GitHubToken, GitHubUser


def is_signed_in() -> bool:
    token = _get_token_from_http_headers()
    if not token:
        return False

    token_model = GitHubToken.query.filter_by(token=token).one_or_none()
    if not token_model:
        return False

    return True


def is_admin() -> bool:
    if not is_signed_in():
        return False

    token = _get_token_from_http_headers()
    if not token:
        return False

    user_model = (
        GitHubUser.query.join(GitHubToken)
        .filter(GitHubToken.token == token)
        .one_or_none()
    )

    if not user_model:
        return False

    admin_model = AccountAdmin.query.filter_by(
        git_hub_login=user_model.login
    ).one_or_none()

    if not admin_model:
        return False

    return True


def _get_token_from_http_headers() -> Optional[str]:
    auth_header = request.headers.get('Authorization')
    # e.g., 'Bearer "xxxx"', "Bearer 'xxxx'",  or 'Bearer xxxx'

    if not auth_header:
        return None

    token = auth_header.split()[1].strip('"\'')
    # e.g., "xxxx"

    return token
