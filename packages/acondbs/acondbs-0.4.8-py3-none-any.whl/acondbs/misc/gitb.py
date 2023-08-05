"""Git operations
"""
import warnings
from pathlib import Path
from typing import Optional, Union

import git


def commit(path: Union[str, Path], message: Optional[str] = None) -> None:
    """commit all changes in a git repository to git

    If the path is not a git repository, unless it is empty, it will
    be initialized as a new repository.

    Parameters
    ----------
    path : str
        The path to a git repository
    message : str, optional
        Commit message.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If `path` is not a directory

    """

    path = Path(path)
    if not path.is_dir():
        raise ValueError("path is not a directory: {}".format(path))

    if is_git_repo(path):
        repo = git.Repo(path)
    else:
        if not list(path.iterdir()):
            warnings.warn('the directory is empty. nothing to commit: {}'.format(path))
            return
        repo = git.Repo.init(path)

    if not repo.is_dirty(untracked_files=True):
        warnings.warn('the repo is clean. nothing to commit: {}'.format(path))
        return

    repo.git.add(A=True)

    if not message:
        message = 'commit all'
    repo.index.commit(message)


def pull(path: Union[str, Path]) -> None:
    """pull from a tracking branch

    Equivalent to execute "git pull" in the path.

    Parameters
    ----------
    path : str
        The path to a git repository

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If `path` is not a directory
        If `path` is not a git repo
        If the repo has no tracking branch

    """

    path = Path(path)
    if not path.is_dir():
        raise ValueError("path is not a directory: {}".format(path))

    if not is_git_repo(path):
        raise ValueError("path is not a git repo: {}".format(path))

    repo = git.Repo(path)

    tracking_branch = repo.active_branch.tracking_branch()

    if not tracking_branch:
        raise ValueError("repo has no tracking branch: {}".format(path))

    remote = repo.remotes[tracking_branch.remote_name]
    remote.pull()


def push(path: Union[str, Path]) -> None:
    """push to a upstream branch

    Equivalent to execute "git push" in the path.

    Parameters
    ----------
    path : str
        The path to a git repository

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If `path` is not a directory
        If `path` is not a git repo
        If the repo has no tracking branch

    """

    path = Path(path)
    if not path.is_dir():
        raise ValueError("path is not a directory: {}".format(path))

    if not is_git_repo(path):
        raise ValueError("path is not a git repo: {}".format(path))

    repo = git.Repo(path)

    tracking_branch = repo.active_branch.tracking_branch()

    if not tracking_branch:
        raise ValueError("repo has no tracking branch: {}".format(path))

    remote = repo.remotes[tracking_branch.remote_name]
    remote.push()


def is_git_repo(path: Union[str, Path]) -> bool:
    """test if a folder is a git repository

    copied from https://stackoverflow.com/a/39956572/7309855

    """
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:  # type: ignore
        return False
