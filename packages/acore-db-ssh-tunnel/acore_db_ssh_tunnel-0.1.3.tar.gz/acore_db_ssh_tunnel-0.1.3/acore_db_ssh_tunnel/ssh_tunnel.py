# -*- coding: utf-8 -*-

"""
This module is a SSH Tunnel management automation tool.

To connect to a RDS database in a private subnet from your local laptop,
you need to use a jump host (EC2 instance) as a bridge. You can create a
SSH tunnel with the jump host's public IP and your AWS pem key file,
then use 127.0.0.1 as the database host.

Reference:

- SSH Tunneling: Examples, Command, Server Config: https://www.ssh.com/academy/ssh/tunneling-example
- AWS Key Pairs: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html

[CN]

本模块是用来管理 SSH Tunnel 的自动化脚本. 通常出于安全考虑, 数据库一般都位于私网中. 为了
从本地开发电脑连接到数据库, 你可以使用跳板机. 先用 SSH 和跳板机建立一个 tunnel, 然后将
127.0.0.1 作为数据库的 host, 这样所有的流量都会被自动转发到跳板机, 然后再转发到数据库.

.. note::

    本模块不考虑用一个 pem 秘钥开启多个 SSH Tunnel 连接到不同跳板机的情况. 我们假设同一时间
    一个秘钥只能创建一个 SSH Tunnel.
"""
import sys
import typing as T
import subprocess
from pathlib import Path

import sqlalchemy as sa


def create_ssh_tunnel(
    path_pem_file,
    db_host: str,
    db_port: int,
    jump_host_username: str,
    jump_host_public_ip: str,
    verbose: bool = True,
    print_func: T.Callable = print,
):
    """
    Create an SSH Tunnel.

    创建一个 SSH Tunnel 连接到数据库. 建议完成后使用 :func:`test_ssh_tunnel` 函数进行测试.

    :param path_pem_file: AWS SSH pem 秘钥的路径.
    :param db_host: 数据库的 endpoint, 在此情况下一般是私网的 IP. 如果是 AWS RDS, 则是 RDS 的 endpoint.
    :param db_port: 数据库的端口. 在本项目中数据库是 MySQL, 所以端口通常是 3306.
    :param jump_host_username: 跳板机的操作系统用户名, 用与创建 SSH 连接.
    :param jump_host_public_ip: 跳板机的公网 IP 地址.
    :param verbose: 是否打印详细的 SSH Tunnel 命令.
    :param print_func: 打印函数. 默认是 print, 你可以用自定义的 logger 来替换它.
    """
    path_pem_file = Path(path_pem_file).absolute()
    if path_pem_file.exists() is False:
        raise FileNotFoundError(f"pem file not found at {path_pem_file}.")
    args = [
        "ssh",
        "-i",
        f"{path_pem_file}",
        "-f",
        "-N",
        "-L",
        f"{db_port}:{db_host}:{db_port}",
        f"{jump_host_username}@{jump_host_public_ip}",
        "-v",
    ]
    ssh_cmd = " ".join(args)
    if verbose:
        print_func(f"Open ssh tunnel by running the following command:")
        print_func(f"  {ssh_cmd}")

    res = subprocess.run(args)
    if res.returncode == 0:
        print_func("SSH Tunnel created successfully.")
        return

    # something wrong, let's check if you have to do it in terminal
    res = subprocess.run(args, capture_output=True)
    error_message = res.stderr.decode("utf-8")
    error_keyword = "can't open /dev/tty: Device not configured"
    if error_keyword in error_message:
        print_func(
            "You may need to run this script in terminal, NOT in Python IDE. "
            "Enter the following command in terminal to create SSH tunnel: "
        )
        print_func(f"  {ssh_cmd}")
    else:
        print_func("Failed to create SSH Tunnel.")


def list_ssh_tunnel_pid(
    path_pem_file,
) -> T.List[str]:
    """
    List the PID of SSH Tunnel processes.

    找出在本地机器上已有的 SSH Tunnel 的 PID (process id, 即进程 ID). 其原理是用
    `ps aux <https://www.linode.com/docs/guides/use-the-ps-aux-command-in-linux/>`_
    命令以 BSD 的格式列出所有进程, 而这个进程一定是包含 ``ssh`` 的. 然后再用 python 捕获
    这些进程列表, 这些进程里包含 pem 文件路径的就一定是我们要找的 SSH Tunnel 进程.

    :param path_pem_file: AWS SSH pem 秘钥的路径.

    :return: SSH Tunnel 进程的 PID 列表.
    """
    path_pem_file = str(Path(path_pem_file).absolute())
    pipe = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
    res = subprocess.run(["grep", "ssh"], stdin=pipe.stdout, capture_output=True)
    pid_list = []
    for line in res.stdout.decode("utf-8").strip().split("\n"):
        if path_pem_file in line:
            words = [word.strip() for word in line.split(" ") if word.strip()]
            pid = words[1]
            pid_list.append(pid)
    return pid_list


def list_ssh_tunnel(
    path_pem_file,
    print_func: T.Callable = print,
):
    """
    List the SSH Tunnel processes.

    列出在本地机器上用特定 pem 秘钥创建的 SSH Tunnel. 其原理请参考 :func:`list_ssh_tunnel_pid`.

    :param path_pem_file: AWS SSH pem 秘钥的路径.
    :param print_func: 打印函数. 默认是 print, 你可以用自定义的 logger 来替换它.
    """
    path_pem_file = str(Path(path_pem_file).absolute())
    pipe = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
    res = subprocess.run(["grep", "ssh"], stdin=pipe.stdout, capture_output=True)
    lines = list()
    for line in res.stdout.decode("utf-8").strip().split("\n"):
        if path_pem_file in line:
            lines.append(line)

    if len(lines):
        print_func("List SSH tunnel ...")
        print_func("")
        for line in lines:
            print_func(line)
    else:
        print_func("There's NO existing SSH tunnel.")


def kill_ssh_tunnel(
    path_pem_file,
    verbose: bool = True,
    print_func: T.Callable = print,
):
    """
    Kill the SSH Tunnel processes.

    关闭所有在本地机器上用特定 pem 秘钥创建的 SSH Tunnel. 其原理是用
    :func:`list_ssh_tunnel_pid` 函数找到这些 SSH Tunnel 的进程 ID 然后将其杀死.

    Reference:

    - How to close this ssh tunnel? https://stackoverflow.com/questions/9447226/how-to-close-this-ssh-tunnel

    :param path_pem_file: AWS SSH pem 秘钥的路径.
    :param verbose: 是否打印详细的 SSH Tunnel 命令.
    :param print_func: 打印函数. 默认是 print, 你可以用自定义的 logger 来替换它.

    :return: SSH Tunnel 进程的 PID 列表.
    """
    pid_list = list_ssh_tunnel_pid(path_pem_file)
    if len(pid_list):
        for pid in pid_list:
            if verbose:
                print_func(f"Found pid {pid}, try to kill it")
            subprocess.run(["kill", pid])
    else:
        if verbose:
            print_func("There's NO existing SSH tunnel to kill.")


def test_ssh_tunnel(
    engine: sa.Engine,
    sql: str = "SELECT 1;",
    verbose: bool = True,
    print_func: T.Callable = print,
) -> bool:
    """
    Test if the SSH Tunnel is working.

    测试 SSH Tunnel 是否正常工作. 其原理是用 SQLAlchemy 创建一个数据库连接, 然后执行一个简单
    SQL 命令.

    :param engine: 已经创建好的 Sqlalchemy 的 Engine 对象. 这里注意 host 一定是 127.0.0.1.
        如果你有额外的参数, 例如 timeout 时长, 你可以字啊创建 Engine 的时候用 ``connect_args``
        参数指定.
    :param sql: 测试用的 SQL 命令. 默认是 ``SELECT * FROM acore_auth.realmlist LIMIT 1;``.
    :param verbose: 是否打印详细的 SSH Tunnel 命令.
    :param print_func: 打印函数. 默认是 print, 你可以用自定义的 logger 来替换它.

    :return: 如果 SSH Tunnel 正常工作, 返回 True, 否则返回 False.
    """
    if verbose:
        print_func(
            "Test SSH Tunnel Connection, if you see a "
            "dictionary record means that it works:"
        )
        print_func("")
    try:
        with engine.connect() as connect:
            sql_stmt = sa.text(sql)
            result = connect.execute(sql_stmt)
            if verbose:
                print_func(result.mappings().one())
        return True
    except TimeoutError:
        return False
