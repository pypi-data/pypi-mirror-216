# -*- coding: utf-8 -*-

"""
针对 Azerothcore 魔兽世界数据库优化后的 SSH Tunnel 工具. 跟通用工具不同之处在于:

- 用的 pymysql driver
- 由于是 MySQL, 所以 port 默认是 3306
- 由于是 acore 数据库, 测试用 sql 命令则是
"""

import typing as T

from .mysql_engine import create_engine
from .ssh_tunnel import test_ssh_tunnel as _test_ssh_tunnel


def test_ssh_tunnel(
    db_port: int,
    db_username: str,
    db_password: str,
    db_name: str,
    timeout: int = 5,
    sql: str = "SELECT * FROM acore_auth.realmlist LIMIT 1;",  # you can also use "SELECT 1;"
    verbose: bool = True,
    print_func: T.Callable = print,
) -> bool:
    """
    Test if the SSH Tunnel is working.

    测试 SSH Tunnel 是否正常工作. 其原理是用 SQLAlchemy 创建一个数据库连接, 然后执行一个简单
    SQL 命令.

    :param db_port: 数据库的端口. 在本项目中数据库是 MySQL, 所以端口通常是 3306.
        之所以不需要 db_host 的原因是我们使用了 SSH tunnel, 所以 db_host 是 127.0.0.1.
    :param db_username: 数据库用户名.
    :param db_password: 数据库密码.
    :param db_name: 数据库名.
    :param timeout: 测试的连接超时秒.
    :param sql: 测试用的 SQL 命令. 默认是 ``SELECT * FROM acore_auth.realmlist LIMIT 1;``.
    :param verbose: 是否打印详细的 SSH Tunnel 命令.
    :param print_func: 打印函数. 默认是 print, 你可以用自定义的 logger 来替换它.

    :return: 如果 SSH Tunnel 正常工作, 返回 True, 否则返回 False.
    """
    engine = create_engine(
        host="127.0.0.1",
        port=db_port,
        username=db_username,
        password=db_password,
        db_name=db_name,
        connect_args={"connect_timeout": timeout},
    )
    return _test_ssh_tunnel(
        engine=engine,
        sql=sql,
        verbose=verbose,
        print_func=print_func,
    )
