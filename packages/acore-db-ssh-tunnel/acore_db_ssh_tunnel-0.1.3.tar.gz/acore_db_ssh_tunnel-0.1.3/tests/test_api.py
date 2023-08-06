# -*- coding: utf-8 -*-

from acore_db_ssh_tunnel import api


def test():
    _ = api
    _ = api.ssh_tunnel_lib
    _ = api.create_ssh_tunnel
    _ = api.list_ssh_tunnel_pid
    _ = api.list_ssh_tunnel
    _ = api.test_ssh_tunnel
    _ = api.kill_ssh_tunnel
    _ = api.create_engine


if __name__ == "__main__":
    from acore_db_ssh_tunnel.tests import run_cov_test

    run_cov_test(__file__, "acore_db_ssh_tunnel.api", preview=False)
