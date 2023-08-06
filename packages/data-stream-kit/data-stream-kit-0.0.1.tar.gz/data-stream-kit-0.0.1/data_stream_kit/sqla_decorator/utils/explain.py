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
from ..session_ctx import ctx_session

try:
    from sqlalchemy.engine.result import ResultProxy, RowProxy
except ImportError:
    # sqlalchemy 1.4以上用法
    from sqlalchemy.engine.cursor import CursorResult as ResultProxy
    from sqlalchemy.engine.row import RowProxy

from sqlalchemy.ext.compiler import compiles

try:
    from sqlalchemy.ext.declarative.api import DeclarativeMeta
except ImportError:
    from sqlalchemy.ext.declarative import DeclarativeMeta

from sqlalchemy.sql.expression import Executable, ClauseElement
from sqlalchemy.dialects import mysql, postgresql, sqlite

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

session: Session = ctx_session
logger = logging.getLogger(__name__)


# TODO explain query
class ExplainElement(Executable, ClauseElement):
    db_type = None

    def __init__(self, stmt, analyze=False, **kwargs):
        # self.statement = _literal_as_text(stmt)
        # str(q.statement.compile(dialect=postgresql.dialect()))
        # self.sql = str(stmt.statement.compile(compile_kwargs={"literal_binds": True}))
        self.sql = self.generate_sql(stmt)
        self.analyze = analyze
        # helps with INSERT statements
        self.inline = getattr(stmt, 'inline', None)

    def generate_sql(self, stmt):
        # 将query 转换成 sql
        kwargs = {"compile_kwargs": {"literal_binds": True}}
        if self.db_type == 'mysql':
            kwargs['dialect'] = mysql.dialect()

        elif self.db_type == 'postgresql':
            kwargs['dialect'] = postgresql.dialect()

        elif self.db_type == 'sqlite':
            kwargs['dialect'] = sqlite.dialect()

        return str(stmt.statement.compile(**kwargs))


class MysqlExplainElement(ExplainElement):
    db_type = 'mysql'


class SqliteExplainElement(ExplainElement):
    db_type = 'sqlite'


class PostgresqlExplainElement(ExplainElement):
    db_type = 'postgresql'


@compiles(MysqlExplainElement, 'mysql')
def mysql_explain(element, compiler):
    text = "EXPLAIN "
    if element.analyze:
        text += "ANALYZE "
    text += element.sql

    # allow EXPLAIN for INSERT/UPDATE/DELETE, turn off
    # compiler flags that would otherwise start treating this
    # like INSERT/UPDATE/DELETE (gets confused with RETURNING
    # or autocloses cursor which we don't want)
    compiler.isinsert = compiler.isupdate = compiler.isdelete = False

    return text


@compiles(PostgresqlExplainElement, 'postgresql')
def pg_explain(element, compiler, **kw):
    text = "EXPLAIN "
    if element.analyze:
        text += "ANALYZE "
    text += element.sql

    # allow EXPLAIN for INSERT/UPDATE/DELETE, turn off
    # compiler flags that would otherwise start treating this
    # like INSERT/UPDATE/DELETE (gets confused with RETURNING
    # or autocloses cursor which we don't want)
    compiler.isinsert = compiler.isupdate = compiler.isdelete = False

    return text


@compiles(SqliteExplainElement, 'sqlite')
def sqlite_explain(element, compiler, **kw):
    text = "EXPLAIN "
    if element.analyze:
        text += "ANALYZE "
    text += element.sql

    # allow EXPLAIN for INSERT/UPDATE/DELETE, turn off
    # compiler flags that would otherwise start treating this
    # like INSERT/UPDATE/DELETE (gets confused with RETURNING
    # or autocloses cursor which we don't want)
    compiler.isinsert = compiler.isupdate = compiler.isdelete = False

    return text


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
        rows = d['rows'] or 0
        count += rows
    return count


def query_sqlite_explain(query):
    return query_count_explain(query, db_type='sqlite')


def query_mysql_explain(query):
    return query_count_explain(query, db_type='mysql')


def query_postgresql_explain(query):
    return query_count_explain(query, db_type='postgresql')
