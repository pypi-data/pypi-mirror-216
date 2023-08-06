import logging
import sys
from pathlib import Path

from paramiko import SSHClient
from tqdm import tqdm

from .base_utils import user_yes_no

MB_PER_BYTE = 1000000


def create_ssh_client(
    server_address: str,
    username: str,
    logger: logging.Logger = logging.getLogger("dummy"),
) -> SSHClient:
    logger.info(f"Attempting to ssh into {server_address} as user {username}...")
    client = SSHClient()
    client.load_system_host_keys()
    client.connect(server_address, username=username)
    logger.info(f"Succesfully ssh:d into {server_address} as user {username}.")
    return client


def run_ssh_command(
    cmd: str,
    client: SSHClient,
    block_until_finished: bool = False,
    continuous_output: bool = False,  # NOTE: Stdout will be consumed.
    debug_mode: bool = False,
    logger: logging.Logger = logging.getLogger("dummy"),
):
    logger.debug(f"> {cmd}")
    if debug_mode:
        if not user_yes_no("Run command on host machine?"):
            sys.exit(0)

    stdin, stdout, stderr = client.exec_command(cmd, get_pty=continuous_output)

    if continuous_output:
        for line in iter(stdout.readline, ""):
            logger.info(f"[Remote] {line.rstrip()}")

    if block_until_finished:
        exit_status = stdout.channel.recv_exit_status()
        logger.info(f"Command finished with exit status {exit_status}.")

    return stdin, stdout, stderr


def fetch_file(
    client: SSHClient,
    remote_filepath: Path,
    host_target_filepath: Path,
    logger: logging.Logger = logging.getLogger("dummy"),
) -> None:
    if host_target_filepath.is_dir():
        host_target_filepath = host_target_filepath / remote_filepath.name
    assert host_target_filepath.parent.is_dir()

    # Create file transfer progress bar.
    progress_bar = tqdm()

    def sftp_get_transfer_callback_fn(x, y):
        progress_bar.set_description(
            (
                f"Transfered {x / MB_PER_BYTE :.2f} out of {y / MB_PER_BYTE :.2f} Mb "
                f"({x/y*100:.1f}%)"
            )
        )

    logger.info(
        (
            f"Attempting to download {remote_filepath} from remote to "
            f"{host_target_filepath} on host."
        )
    )
    sftp_client = client.open_sftp()
    sftp_client.get(
        str(remote_filepath),
        localpath=str(host_target_filepath),
        callback=sftp_get_transfer_callback_fn,
    )
    progress_bar.close()

    assert host_target_filepath.is_file()
    logger.info(
        (
            f"Successfully downloaded {remote_filepath} from remote to "
            f"{host_target_filepath} on host."
        )
    )
