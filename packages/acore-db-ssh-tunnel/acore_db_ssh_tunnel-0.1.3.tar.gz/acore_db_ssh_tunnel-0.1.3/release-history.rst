.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.3 (2023-06-27)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- add ``acore_db_ssh_tunnel.api.create_engine`` to public API.

**Minor Improvements**

- fix type hint in ``list_ssh_tunnel`` and ``kill_ssh_tunnel``.


0.1.2 (2023-06-16)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- Fix a bug that the ``create_ssh_tunnel`` cannot be run in Python IDE, but has to run in a terminal at the first time. Because you have to manually enter pass phrase and enter 'yes' to trust the host.


0.1.1 (2023-06-15)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release
- Add the following public api:
    - ``acore_db_ssh_tunnel.api.ssh_tunnel_lib``
    - ``acore_db_ssh_tunnel.api.create_ssh_tunnel``
    - ``acore_db_ssh_tunnel.api.list_ssh_tunnel_pid``
    - ``acore_db_ssh_tunnel.api.list_ssh_tunnel``
    - ``acore_db_ssh_tunnel.api.test_ssh_tunnel``
    - ``acore_db_ssh_tunnel.api.kill_ssh_tunnel``
