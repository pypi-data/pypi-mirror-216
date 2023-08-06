# -*- coding: utf-8 -*-

"""
# Created on 2021/11/14 11:03 下午
---------
Summary:

---------
# @Author  : zhuyaowen
# @Email  : zhuyaowen@chinasofti.com

"""

import logging

from sqlalchemy.orm.session import Session

from .db import sqlalchemy_result_format
from .explain import MysqlExplainElement, SqliteExplainElement, PostgresqlExplainElement
from ..session_ctx import ctx_session

session: Session = ctx_session
logger = logging.getLogger(__name__)


def query_count_explain(query, db_type='mysql'):
    if db_type == 'mysql':

        _explain = MysqlExplainElement
    elif db_type == 'postgresql':

        _explain = PostgresqlExplainElement
    elif db_type == 'sqlite':

        _explain = SqliteExplainElement
    else:

        _explain = MysqlExplainElement

    explain_results = session.execute(_explain(query)).fetchall()
    explain_results = sqlalchemy_result_format(explain_results)

    count = 0

    for d in explain_results:
        rows = d['rows'] or 0  # mysql  # TODO
        count += rows
    return count


def query_sqlite_count(query):
    return query_count_explain(query, db_type='sqlite')


def query_mysql_count(query):
    return query_count_explain(query, db_type='mysql')


def query_postgresql_count(query):
    return query_count_explain(query, db_type='postgresql')
