
.. .. image:: https://readthedocs.org/projects/acore-db-ssh-tunnel/badge/?version=latest
    :target: https://acore-db-ssh-tunnel.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/acore_db_ssh_tunnel-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/acore_db_ssh_tunnel-project/actions?query=workflow:CI

.. .. image:: https://codecov.io/gh/MacHu-GWU/acore_db_ssh_tunnel-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/acore_db_ssh_tunnel-project

.. image:: https://img.shields.io/pypi/v/acore-db-ssh-tunnel.svg
    :target: https://pypi.python.org/pypi/acore-db-ssh-tunnel

.. image:: https://img.shields.io/pypi/l/acore-db-ssh-tunnel.svg
    :target: https://pypi.python.org/pypi/acore-db-ssh-tunnel

.. image:: https://img.shields.io/pypi/pyversions/acore-db-ssh-tunnel.svg
    :target: https://pypi.python.org/pypi/acore-db-ssh-tunnel

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/acore_db_ssh_tunnel-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/acore_db_ssh_tunnel-project

------

.. .. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://acore-db-ssh-tunnel.readthedocs.io/en/latest/

.. .. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://acore-db-ssh-tunnel.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/acore_db_ssh_tunnel-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/acore_db_ssh_tunnel-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/acore_db_ssh_tunnel-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/acore-db-ssh-tunnel#files


Welcome to ``acore_db_ssh_tunnel`` Documentation
==============================================================================
出于安全考虑, 通常数据库都会被部署到私网中, 是不允许直接从公网访问的. 为了能让开发者从工具配置齐全的开发电脑连接到数据库, 通常采用跳板机 + `SSH Tunnel <https://www.ssh.com/academy/ssh/tunneling>`_ 技术实现. 具体方法是用 SSH 和 EC2 的秘钥在本地机器上建立一个 tunnel, 所有本来要发送到 Database domain 的流量都发送到 127.0.0.1, 然后 SSH 会自动将流量发送到跳板机, 然后堡垒机再发送到 Database.

本项目将创建, 关闭, 查看, 以及测试 SSH Tunnel 的方法封装成了一个 Python package, 以便于在 Python 代码中使用.

**用例**

.. code-block:: python

    from acore_db_ssh_tunnel import api

    def create_ssh_tunnel():
        api.create_ssh_tunnel(
            path_pem_file=path_pem_file,
            db_host=db_host,
            db_port=db_port,
            jump_host_username=jump_host_username,
            jump_host_public_ip=jump_host_public_ip,
        )


    def list_ssh_tunnel():
        api.list_ssh_tunnel(path_pem_file)


    def test_ssh_tunnel():
        api.test_ssh_tunnel(
            db_port=db_port,
            db_username=db_username,
            db_password=db_password,
            db_name=db_name,
        )


    def kill_ssh_tunnel():
        api.kill_ssh_tunnel(path_pem_file)


    # edit the following variables to your own
    db_host = "my-server.1a2b3c4d5e6f.us-east-1.rds.amazonaws.com"
    db_port = 3306
    db_username = "admin"
    db_password = "admin"
    db_name = "my_database"
    jump_host_username = "ubuntu"
    jump_host_public_ip = "111.111.111.111"
    path_pem_file = "/Users/myusername/ec2-key.pem"

    # create_ssh_tunnel() # run this first
    # list_ssh_tunnel() # then this
    # test_ssh_tunnel() # then this
    # kill_ssh_tunnel() # then clean up


.. _install:

Install
------------------------------------------------------------------------------

``acore_db_ssh_tunnel`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install acore-db-ssh-tunnel

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade acore-db-ssh-tunnel
