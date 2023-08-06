import csv
from datetime import datetime
import hashlib
from lib2to3.pytree import Node
import math
import shutil
import sys
import pathlib
import logging
import argparse
from typing import Dict, Optional
from os import listdir, scandir
from os.path import join, exists, isfile, getsize
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
from ablean.components.util.logger import Logger
from ablean.components.config.lean_config_manager import LeanConfigManager
from ablean.constants import DATA_HASH_FILE, DEFAULT_LEAN_CONFIG_FILE_NAME

DATE_FORMAT = "%Y%m%d"
OPTION_DATE_START_POS = -len('20220523_quote_european.zip')
OPTION_DATE_END_POS = -len('_quote_european.zip')
OTHER_DATE_START_POS = -len('20220523_quote.zip')
OTHER_DATE_END_POS = -len('_quote.zip')


def get_file_hash(local_file: str):
    md5_object = hashlib.md5()
    block_size = 64 * md5_object.block_size
    with open(local_file, 'rb') as f:
        chunk = f.read(block_size)
        while chunk:
            md5_object.update(chunk)
            chunk = f.read(block_size)
    return md5_object.hexdigest()


def scantree(path):
    """Recursively yield DirEntry objects for given directory."""
    for entry in scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)  # see below for Python 2.x
        else:
            yield entry


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


class DataManager:
    def __init__(
        self,
        lean_config_manager: LeanConfigManager,
        logger: Logger,
    ):
        self.lean_config_manager = lean_config_manager
        self.logger = logger
        self.progress = None
        self.progress_task = None
        self._load_config()

    def _load_data_hash(self, filename: str = DATA_HASH_FILE):
        filename = join(self.output_path, filename)
        if exists(filename):
            with open(filename, mode='r') as infile:
                reader = csv.reader(infile)
                return {rows[0]: rows[1] for rows in reader}
        else:
            return {}

    def _scp_get(
        self, scp: SCPClient, remote_path: str, local_path: str, recursive: bool = False
    ):
        if self.progress is not None:
            self.progress.stop()
        self.progress = self.logger.progress()
        self.progress_task = self.progress.add_task(remote_path)
        try:
            scp.get(remote_path, local_path, recursive)
        except KeyboardInterrupt as e:
            if self.progress is not None:
                self.progress.stop()
            raise e
        pass

    def _download_data_file(
        self,
        scp: SCPClient,
        remote_file: str,
        local_file: str,
        hash: str = None,
    ):
        remote_file = f"{self.remote_path}/{remote_file}".replace('//', '/')
        local_file = f"{self.output_path}/{local_file}".replace('//', '/')
        if not exists(local_file):
            local_path = pathlib.Path(local_file).parent.resolve()
            local_path.mkdir(parents=True, exist_ok=True)
        elif get_file_hash(local_file) == hash:
            self.logger.info(f'{local_file} is OK!')
            return

        if hash is None:
            self._scp_get(scp, remote_file, local_file)
        else:
            temp_file = f"{self.output_path}/{hash}.tmp".replace('//', '/')
            self._scp_get(scp, remote_file, temp_file)
            shutil.move(temp_file, local_file)

    def _create_data_hash(self, hash_table: Dict):
        for path in ['option', 'future', 'crypto']:
            path = join(self.output_path, path)
            if not exists(path):
                continue
            for item in scantree(path):
                if not item.path.endswith(".zip"):
                    continue
                self._update_file_hash(item.path, hash_table)
                self.logger.info(f"init {item.path} hash")

    def _get_file_key(self, local_file: str):
        return local_file[len(self.output_path) :].replace('\\', '/')

    def _update_file_hash(self, local_file: str, hash_table: Dict):
        md5 = get_file_hash(local_file)
        key = self._get_file_key(local_file)
        hash_table[key] = md5
        pass

    def _save_data_hash(self, hash_table: Dict):
        filename = join(self.output_path, DATA_HASH_FILE)
        with open(filename, mode='w') as outfile:
            for k, v in hash_table.items():
                outfile.write(f"{k},{v}\n")

    def _on_data(self, filename: str, size: int, send: int):
        if size >= send:
            send_size = convert_size(send)
            file_size = convert_size(size) + ' ' * 5
            desc = f'{send_size}/{file_size}'
            self.progress.update(
                self.progress_task,
                completed=(send / float(size) * 100),
                description=desc,
            )

    def _load_config(self):
        config = self.lean_config_manager.get_lean_config()
        self.output_path = config["data-folder"]
        self.remote_path = config["remote-data-folder"]
        self.ssh_host = config["ssh-host"]
        self.ssh_port = config["ssh-port"]
        self.ssh_user = config["ssh-user"]
        self.ssh_password = config["ssh-pwd"]
        self.update_second_data = config["update-second-data"]

    def _create_scp(self):
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(
            self.ssh_host,
            port=self.ssh_port,
            username=self.ssh_user,
            password=self.ssh_password,
            compress=True,
        )
        return SCPClient(ssh.get_transport(), progress=self._on_data)

    def update_data(
        self,
        update_second_data=False,
        force_update=False,
        data_path: str = None,
        date_start=Optional[datetime],
        date_end=Optional[datetime],
        market: str = None,
    ):
        self._load_config()
        if data_path is not None:
            self.output_path = data_path
        self.logger.info(f"update data from {self.ssh_host}")
        local_hash = self._load_data_hash()
        if force_update or len(local_hash) == 0:
            self._create_data_hash(local_hash)
            self._save_data_hash(local_hash)

        scp = self._create_scp()
        self._download_data_file(scp, DATA_HASH_FILE, f'server_{DATA_HASH_FILE}')
        remote_hash = self._load_data_hash(f'server_{DATA_HASH_FILE}')
        update_second_data = update_second_data or self.update_second_data
        
        for k, v in remote_hash.items():
            if k in local_hash and v == local_hash[k]:
                continue
            if 'second' in k and not update_second_data:
                continue
            
            if market is not None:
                if k[len('/crypto/'):len('/crypto/')+len(market)] != market:
                    continue

            if k.endswith('european.zip'):
                file_date = datetime.strptime(
                    k[OPTION_DATE_START_POS:OPTION_DATE_END_POS], DATE_FORMAT
                )
            else:
                file_date = datetime.strptime(
                    k[OTHER_DATE_START_POS:OTHER_DATE_END_POS], DATE_FORMAT
                )

            if date_start is not None and file_date < date_start:
                continue

            if date_end is not None and file_date > date_end:
                continue

            self.logger.info(f"download: {k}")
            self._download_data_file(scp, k, k, v)
            local_hash[k] = v
        self._save_data_hash(local_hash)

    def update_lean(self, output: str):
        self._load_config()
        scp = self._create_scp()
        self.logger.info("download lean.json")
        self._scp_get(scp, '/mnt/data/share/lean/lean.json', output)
        self.logger.info("download launcher")
        self._scp_get(scp, '/mnt/data/share/lean/launcher', output, True)
