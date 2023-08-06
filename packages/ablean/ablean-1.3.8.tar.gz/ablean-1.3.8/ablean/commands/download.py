from datetime import date, datetime
from pathlib import Path
from typing import Optional

import click
from ablean.myclick import LeanCommand, PathParameter
from ablean.container import container


@click.command(cls=LeanCommand, requires_lean_config=True)
@click.option(
    "--data-dir",
    type=PathParameter(exists=False, file_okay=False, dir_okay=True),
    help="下载数存放目录",
)
@click.option(
    "--second-data",
    is_flag=True,
    default=False,
    help="是否更新秒级数据",
)
@click.option(
    "--force-update",
    is_flag=True,
    default=False,
    help="强制更新所有数据",
)
@click.option(
    '--date-start', type=click.DateTime(formats=["%Y-%m-%d"]), default=str(date.min)
)
@click.option(
    '--date-end', type=click.DateTime(formats=["%Y-%m-%d"]), default=str(date.max)
)
@click.option('--market', type=str)
def download(
    data_dir: Optional[Path],
    second_data: bool,
    force_update: bool,
    date_start: Optional[datetime],
    date_end: Optional[datetime],
    market: str,
):
    """Download backtest data"""
    container.data_manager().update_data(
        second_data,
        force_update,
        None if data_dir is None else str(data_dir),
        date_start,
        date_end,
        market,
    )
