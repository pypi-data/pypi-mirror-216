__all__ = [
    '__version__',
    'create_app',
]

from pathlib import Path
from typing import Any, Dict, Optional, Union

from flask import Flask
from flask_cors import CORS

# This import prevents the error, ImportError: cannot import name
# 'attach_enctype_error_multidict' from partially initialized module
# 'flask.debughelpers' (most likely due to a circular import)
from flask import debughelpers  # noqa: F401

from . import _warnings  # noqa: F401
from . import _logging

from acondbs.__about__ import __version__

DEFAULT_CONFIG_DICT: Dict[str, Any] = dict(
    SECRET_KEY="dev",
    SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)


def create_app(config_path: Optional[Union[Path, str]] = None, **kwargs: Any) -> Flask:
    _logging.configure_logging()

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(**DEFAULT_CONFIG_DICT)

    if config_path is not None:
        config_path = Path(config_path)
        if not config_path.is_absolute():
            # If `config_path` is relative, it is considered relative
            # to the current working directory.
            config_path = Path.cwd().joinpath(config_path)

            # Note: `app.config.from_pyfile()` treats a relative path
            # either a) relative to the top directory of the app,
            # i.e., the directory in which this file is, if
            # `instance_relative_config` is `False`, or b) relative to
            # the "instance folder", a specific directory described in
            # https://flask.palletsprojects.com/en/1.1.x/config/#instance-folders),
            # if `instance_relative_config` is `True`.

        app.config.from_pyfile(str(config_path), silent=False)

    if kwargs:
        app.config.from_mapping(**kwargs)

    from . import db

    db.init_app(app)

    from . import blueprint

    blueprint.init_app(app)

    from . import models

    models.init_app(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    app.logger.info('"app" initialized')
    return app
