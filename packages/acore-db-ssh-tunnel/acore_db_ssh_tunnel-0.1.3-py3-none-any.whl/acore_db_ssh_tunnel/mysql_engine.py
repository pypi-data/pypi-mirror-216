# -*- coding: utf-8 -*-

import sqlalchemy as sa


def create_engine(
    host: str,
    port: int,
    username: str,
    password: str,
    db_name: str,
    **kwargs,
) -> sa.engine.Engine:
    """
    Create a mysql engine.
    """
    url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}"
    return sa.create_engine(url, **kwargs)
