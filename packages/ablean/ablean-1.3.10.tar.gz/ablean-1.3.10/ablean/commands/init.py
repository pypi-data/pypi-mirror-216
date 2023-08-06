from distutils.command.config import config
import json
from pathlib import Path
from typing import Optional

import click

from ablean.myclick import LeanCommand, PathParameter
from ablean.constants import (
    DEFAULT_DATA_DIRECTORY_NAME,
    DEFAULT_LEAN_CONFIG_FILE_NAME,
    GUI_PRODUCT_SUBSCRIPTION_IDS,
)
from ablean.container import container
from ablean.models.errors import MoreInfoError


@click.command(cls=LeanCommand)
@click.option(
    "--data-dir",
    "-d",
    type=PathParameter(file_okay=False, dir_okay=True),
    help="data_directory",
)
@click.option("--host", "-h", required=True, type=str, help="ssh user id")
@click.option("--port", "-p", type=int, default=22, help="ssh port")
@click.option("--user", "-u", required=True, type=str, help="ssh user ")
@click.option("--pwd", "-w", required=True, type=str, help="ssh user pasword")
def init(data_dir: Optional[Path], host: str, port: int, user: str, pwd: str):

    logger = container.logger()
    lean_config_manager = container.lean_config_manager()
    try:
        lean_root = lean_config_manager.get_cli_root_directory()
        logger.warn(f"lean already inited, lean_root at {str(lean_root)}")
        return
    except MoreInfoError:
        pass

    lean_root = Path.cwd()
    if data_dir is None:
        data_dir = lean_root / "data"
        if not data_dir.exists():
            data_dir.mkdir()

    lean_config = {
        "data-folder": str(data_dir).replace('\\', '/'),
        "remote-data-folder": None,
        "update-second-data": None,
        "ssh-host": host,
        "ssh-port": port,
        "ssh-user": user,
        "ssh-pwd": pwd,
    }

    lean_config_path = lean_root / DEFAULT_LEAN_CONFIG_FILE_NAME
    lean_config_path.write_text(json.dumps(lean_config))
    try:
        container.data_manager().update_lean(str(lean_root))
        lean_config_manager.set_properties(lean_config)
    except Exception:
        lean_config_path.unlink()
        raise
    logger.info(f"ablean init completed, lean_root at {str(lean_root)}")
