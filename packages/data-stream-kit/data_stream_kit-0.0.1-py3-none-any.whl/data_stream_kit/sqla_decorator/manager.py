# -*- coding: utf-8 -*-

"""
# Created on 2021/9/29 5:10 下午
---------
Summary:

---------
# @Author  : zhuyaowen
# @Email  : zhuyaowen@chinasofti.com

"""

import logging
from functools import wraps, partial

from sqlalchemy.exc import OperationalError, ResourceClosedError, IntegrityError, StatementError
from sqlalchemy.orm.session import Session

from .engine import SqlaEngine, create_db_engine, DEFAULT_CONNECTION_NAME
from .session_ctx import SessionContext, check_wrapper_session, get_wrapper_session, ctx_session

logger = logging.getLogger(__name__)

_sessions = {}

_session_ctx_err_msg = """
alias=`{}` 连接不存在  请先初始化数据库连接 
"""


def session_retries(func):
    # 连接中断 重连一次

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError as e:
            if 'Illegal mix of collations' in str(e):
                # Mysql 查询存在不同字符集 重置编码
                # SET collation_connection = @@collation_database;

                kwargs['__Illegal_mix_of_collations'] = True
                return func(*args, **kwargs)

            if e.connection_invalidated:
                logger.error(e)
                # close_session()

                # 失去连接 重试一次
                return func(*args, **kwargs)

            raise e
        except ResourceClosedError as e:
            logger.error(e)
            return func(*args, **kwargs)
        except StatementError as e:
            if 'Connection is closed' in str(e):
                logger.error(e)
                return func(*args, **kwargs)
            raise e

        except IntegrityError as e:
            # logger.error(e)
            if check_wrapper_session():
                session.rollback()
            raise e
        except Exception as e:
            raise e

    return wrapper


class SessionContextManager(object):

    def __init__(self, url,
                 create_table=False,
                 create_table_metadata=None,
                 alias=DEFAULT_CONNECTION_NAME,
                 pool_size=10,
                 max_overflow=20,
                 pool_recycle=3600,
                 pool_pre_ping=False,
                 pool_reset_on_return=None,
                 echo=False,
                 autocommit=False,
                 **kwargs):

        """Create a new :class:`_engine.Engine` instance.

    The standard calling form is to send the :ref:`URL <database_urls>` as the
    first positional argument, usually a string
    that indicates database dialect and connection arguments::

        engine = create_engine("postgresql://scott:tiger@localhost/test")

    .. note::

        Please review :ref:`database_urls` for general guidelines in composing
        URL strings.  In particular, special characters, such as those often
        part of passwords, must be URL encoded to be properly parsed.

    Additional keyword arguments may then follow it which
    establish various options on the resulting :class:`_engine.Engine`
    and its underlying :class:`.Dialect` and :class:`_pool.Pool`
    constructs::

        engine = create_engine("mysql://scott:tiger@hostname/dbname",
                                    encoding='latin1', echo=True)

    The string form of the URL is
    ``dialect[+driver]://user:password@host/dbname[?key=value..]``, where
    ``dialect`` is a database name such as ``mysql``, ``oracle``,
    ``postgresql``, etc., and ``driver`` the name of a DBAPI, such as
    ``psycopg2``, ``pyodbc``, ``cx_oracle``, etc.  Alternatively,
    the URL can be an instance of :class:`~sqlalchemy.engine.url.URL`.

    ``**kwargs`` takes a wide variety of options which are routed
    towards their appropriate components.  Arguments may be specific to
    the :class:`_engine.Engine`, the underlying :class:`.Dialect`,
    as well as the
    :class:`_pool.Pool`.  Specific dialects also accept keyword arguments that
    are unique to that dialect.   Here, we describe the parameters
    that are common to most :func:`_sa.create_engine()` usage.

    Once established, the newly resulting :class:`_engine.Engine` will
    request a connection from the underlying :class:`_pool.Pool` once
    :meth:`_engine.Engine.connect` is called, or a method which depends on it
    such as :meth:`_engine.Engine.execute` is invoked.   The
    :class:`_pool.Pool` in turn
    will establish the first actual DBAPI connection when this request
    is received.   The :func:`_sa.create_engine` call itself does **not**
    establish any actual DBAPI connections directly.

    .. seealso::

        :doc:`/core/engines`

        :doc:`/dialects/index`

        :ref:`connections_toplevel`
        
    :param alias: 别名
    
    :param alias: create_table_metadata: 建表元数据信息
    
    :param autoflush: The autoflush setting to use with newly created
     :class:`.Session` objects.
     
    :param autocommit: The autocommit setting to use with newly created
     :class:`.Session` objects.
     
    :param expire_on_commit=True: the
     :paramref:`_orm.Session.expire_on_commit` setting to use
     with newly created :class:`.Session` objects.

    :param case_sensitive: if False, result column names
       will match in a case-insensitive fashion, that is,
       ``row['SomeColumn']``.

    :param connect_args: a dictionary of options which will be
        passed directly to the DBAPI's ``connect()`` method as
        additional keyword arguments.  See the example
        at :ref:`custom_dbapi_args`.

    :param convert_unicode=False: if set to True, causes
        all :class:`.String` datatypes to act as though the
        :paramref:`.String.convert_unicode` flag has been set to ``True``,
        regardless of a setting of ``False`` on an individual :class:`.String`
        type.  This has the effect of causing all :class:`.String` -based
        columns to accommodate Python Unicode objects directly as though the
        datatype were the :class:`.Unicode` type.

        .. deprecated:: 1.3

            The :paramref:`_sa.create_engine.convert_unicode` parameter
            is deprecated and will be removed in a future release.
            All modern DBAPIs now support Python Unicode directly and this
            parameter is unnecessary.

    :param creator: a callable which returns a DBAPI connection.
        This creation function will be passed to the underlying
        connection pool and will be used to create all new database
        connections. Usage of this function causes connection
        parameters specified in the URL argument to be bypassed.

        This hook is not as flexible as the newer
        :meth:`_events.DialectEvents.do_connect` hook which allows complete
        control over how a connection is made to the database, given the full
        set of URL arguments and state beforehand.

        .. seealso::

            :meth:`_events.DialectEvents.do_connect` - event hook that allows
            full control over DBAPI connection mechanics.

            :ref:`custom_dbapi_args`

    :param echo=False: if True, the Engine will log all statements
        as well as a ``repr()`` of their parameter lists to the default log
        handler, which defaults to ``sys.stdout`` for output.   If set to the
        string ``"debug"``, result rows will be printed to the standard output
        as well. The ``echo`` attribute of ``Engine`` can be modified at any
        time to turn logging on and off; direct control of logging is also
        available using the standard Python ``logging`` module.

        .. seealso::

            :ref:`dbengine_logging` - further detail on how to configure
            logging.


    :param echo_pool=False: if True, the connection pool will log
        informational output such as when connections are invalidated
        as well as when connections are recycled to the default log handler,
        which defaults to ``sys.stdout`` for output.   If set to the string
        ``"debug"``, the logging will include pool checkouts and checkins.
        Direct control of logging is also available using the standard Python
        ``logging`` module.

        .. seealso::

            :ref:`dbengine_logging` - further detail on how to configure
            logging.


    :param empty_in_strategy:   No longer used; SQLAlchemy now uses
        "empty set" behavior for IN in all cases.

    :param enable_from_linting: defaults to True.  Will emit a warning
        if a given SELECT statement is found to have un-linked FROM elements
        which would cause a cartesian product.

        .. versionadded:: 1.4

        .. seealso::

            :ref:`change_4737`

    :param encoding: **legacy Python 2 value only, where it only applies to
        specific DBAPIs, not used in Python 3 for any modern DBAPI driver.
        Please refer to individual dialect documentation for client encoding
        behaviors.**  Defaults to the string value ``utf-8``.  This value
        refers **only** to the character encoding that is used when SQLAlchemy
        sends or receives data from a :term:`DBAPI` that does not support
        Python Unicode and **is only used under Python 2**, only for certain
        DBAPI drivers, and only in certain circumstances. **Python 3 users
        please DISREGARD this parameter and refer to the documentation for the
        specific dialect in use in order to configure character encoding
        behavior.**

        .. note:: The ``encoding`` parameter deals only with in-Python
           encoding issues that were prevalent with **some DBAPIS only**
           under **Python 2 only**.  Under Python 3 it is not used by
           any modern dialect. For  DBAPIs that require
           client encoding configurations, which are most of those outside
           of SQLite, please consult specific :ref:`dialect documentation
           <dialect_toplevel>` for details.

        All modern DBAPIs that work in Python 3 necessarily feature direct
        support for Python unicode strings.   Under Python 2, this was not
        always the case.  For those scenarios where the DBAPI is detected as
        not supporting a Python ``unicode`` object under Python 2, this
        encoding is used to determine the source/destination encoding.  It is
        **not used** for those cases where the DBAPI handles unicode directly.

        To properly configure a system to accommodate Python ``unicode``
        objects, the DBAPI should be configured to handle unicode to the
        greatest degree as is appropriate - see the notes on unicode pertaining
        to the specific target database in use at :ref:`dialect_toplevel`.

        Areas where string encoding may need to be accommodated
        outside of the DBAPI, nearly always under **Python 2 only**,
        include zero or more of:

        * the values passed to bound parameters, corresponding to
          the :class:`.Unicode` type or the :class:`.String` type
          when ``convert_unicode`` is ``True``;
        * the values returned in result set columns corresponding
          to the :class:`.Unicode` type or the :class:`.String`
          type when ``convert_unicode`` is ``True``;
        * the string SQL statement passed to the DBAPI's
          ``cursor.execute()`` method;
        * the string names of the keys in the bound parameter
          dictionary passed to the DBAPI's ``cursor.execute()``
          as well as ``cursor.setinputsizes()`` methods;
        * the string column names retrieved from the DBAPI's
          ``cursor.description`` attribute.

        When using Python 3, the DBAPI is required to support all of the above
        values as Python ``unicode`` objects, which in Python 3 are just known
        as ``str``.  In Python 2, the DBAPI does not specify unicode behavior
        at all, so SQLAlchemy must make decisions for each of the above values
        on a per-DBAPI basis - implementations are completely inconsistent in
        their behavior.

    :param execution_options: Dictionary execution options which will
        be applied to all connections.  See
        :meth:`~sqlalchemy.engine.Connection.execution_options`

    :param future: Use the 2.0 style :class:`_future.Engine` and
        :class:`_future.Connection` API.

        .. versionadded:: 1.4

        .. seealso::

            :ref:`migration_20_toplevel`

    :param hide_parameters: Boolean, when set to True, SQL statement parameters
        will not be displayed in INFO logging nor will they be formatted into
        the string representation of :class:`.StatementError` objects.

        .. versionadded:: 1.3.8

        .. seealso::

            :ref:`dbengine_logging` - further detail on how to configure
            logging.

    :param implicit_returning=True:  Legacy flag that when set to ``False``
        will disable the use of ``RETURNING`` on supporting backends where it
        would normally be used to fetch newly generated primary key values for
        single-row INSERT statements that do not otherwise specify a RETURNING
        clause.  This behavior applies primarily to the PostgreSQL, Oracle,
        SQL Server backends.

        .. warning:: this flag originally allowed the "implicit returning"
           feature to be *enabled* back when it was very new and there was not
           well-established database support.  In modern SQLAlchemy, this flag
           should **always be set to True**.  Some SQLAlchemy features will
           fail to function properly if this flag is set to ``False``.

    :param isolation_level: this string parameter is interpreted by various
        dialects in order to affect the transaction isolation level of the
        database connection.   The parameter essentially accepts some subset of
        these string arguments: ``"SERIALIZABLE"``, ``"REPEATABLE READ"``,
        ``"READ COMMITTED"``, ``"READ UNCOMMITTED"`` and ``"AUTOCOMMIT"``.
        Behavior here varies per backend, and
        individual dialects should be consulted directly.

        Note that the isolation level can also be set on a
        per-:class:`_engine.Connection` basis as well, using the
        :paramref:`.Connection.execution_options.isolation_level`
        feature.

        .. seealso::

            :attr:`_engine.Connection.default_isolation_level`
            - view default level

            :paramref:`.Connection.execution_options.isolation_level`
            - set per :class:`_engine.Connection` isolation level

            :ref:`SQLite Transaction Isolation <sqlite_isolation_level>`

            :ref:`PostgreSQL Transaction Isolation <postgresql_isolation_level>`

            :ref:`MySQL Transaction Isolation <mysql_isolation_level>`

            :ref:`session_transaction_isolation` - for the ORM

    :param json_deserializer: for dialects that support the
        :class:`_types.JSON`
        datatype, this is a Python callable that will convert a JSON string
        to a Python object.  By default, the Python ``json.loads`` function is
        used.

        .. versionchanged:: 1.3.7  The SQLite dialect renamed this from
           ``_json_deserializer``.

    :param json_serializer: for dialects that support the :class:`_types.JSON`
        datatype, this is a Python callable that will render a given object
        as JSON.   By default, the Python ``json.dumps`` function is used.

        .. versionchanged:: 1.3.7  The SQLite dialect renamed this from
           ``_json_serializer``.


    :param label_length=None: optional integer value which limits
        the size of dynamically generated column labels to that many
        characters. If less than 6, labels are generated as
        "_(counter)". If ``None``, the value of
        ``dialect.max_identifier_length``, which may be affected via the
        :paramref:`_sa.create_engine.max_identifier_length` parameter,
        is used instead.   The value of
        :paramref:`_sa.create_engine.label_length`
        may not be larger than that of
        :paramref:`_sa.create_engine.max_identfier_length`.

        .. seealso::

            :paramref:`_sa.create_engine.max_identifier_length`

    :param listeners: A list of one or more
        :class:`~sqlalchemy.interfaces.PoolListener` objects which will
        receive connection pool events.

    :param logging_name:  String identifier which will be used within
        the "name" field of logging records generated within the
        "sqlalchemy.engine" logger. Defaults to a hexstring of the
        object's id.

        .. seealso::

            :ref:`dbengine_logging` - further detail on how to configure
            logging.

            :paramref:`_engine.Connection.execution_options.logging_token`



    :param max_identifier_length: integer; override the max_identifier_length
        determined by the dialect.  if ``None`` or zero, has no effect.  This
        is the database's configured maximum number of characters that may be
        used in a SQL identifier such as a table name, column name, or label
        name. All dialects determine this value automatically, however in the
        case of a new database version for which this value has changed but
        SQLAlchemy's dialect has not been adjusted, the value may be passed
        here.

        .. versionadded:: 1.3.9

        .. seealso::

            :paramref:`_sa.create_engine.label_length`

    :param max_overflow=10: the number of connections to allow in
        connection pool "overflow", that is connections that can be
        opened above and beyond the pool_size setting, which defaults
        to five. this is only used with :class:`~sqlalchemy.pool.QueuePool`.

    :param module=None: reference to a Python module object (the module
        itself, not its string name).  Specifies an alternate DBAPI module to
        be used by the engine's dialect.  Each sub-dialect references a
        specific DBAPI which will be imported before first connect.  This
        parameter causes the import to be bypassed, and the given module to
        be used instead. Can be used for testing of DBAPIs as well as to
        inject "mock" DBAPI implementations into the :class:`_engine.Engine`.

    :param paramstyle=None: The `paramstyle <https://legacy.python.org/dev/peps/pep-0249/#paramstyle>`_
        to use when rendering bound parameters.  This style defaults to the
        one recommended by the DBAPI itself, which is retrieved from the
        ``.paramstyle`` attribute of the DBAPI.  However, most DBAPIs accept
        more than one paramstyle, and in particular it may be desirable
        to change a "named" paramstyle into a "positional" one, or vice versa.
        When this attribute is passed, it should be one of the values
        ``"qmark"``, ``"numeric"``, ``"named"``, ``"format"`` or
        ``"pyformat"``, and should correspond to a parameter style known
        to be supported by the DBAPI in use.

    :param pool=None: an already-constructed instance of
        :class:`~sqlalchemy.pool.Pool`, such as a
        :class:`~sqlalchemy.pool.QueuePool` instance. If non-None, this
        pool will be used directly as the underlying connection pool
        for the engine, bypassing whatever connection parameters are
        present in the URL argument. For information on constructing
        connection pools manually, see :ref:`pooling_toplevel`.

    :param poolclass=None: a :class:`~sqlalchemy.pool.Pool`
        subclass, which will be used to create a connection pool
        instance using the connection parameters given in the URL. Note
        this differs from ``pool`` in that you don't actually
        instantiate the pool in this case, you just indicate what type
        of pool to be used.

    :param pool_logging_name:  String identifier which will be used within
       the "name" field of logging records generated within the
       "sqlalchemy.pool" logger. Defaults to a hexstring of the object's
       id.


       .. seealso::

            :ref:`dbengine_logging` - further detail on how to configure
            logging.


    :param pool_pre_ping: boolean, if True will enable the connection pool
        "pre-ping" feature that tests connections for liveness upon
        each checkout.

        .. versionadded:: 1.2

        .. seealso::

            :ref:`pool_disconnects_pessimistic`

    :param pool_size=5: the number of connections to keep open
        inside the connection pool. This used with
        :class:`~sqlalchemy.pool.QueuePool` as
        well as :class:`~sqlalchemy.pool.SingletonThreadPool`.  With
        :class:`~sqlalchemy.pool.QueuePool`, a ``pool_size`` setting
        of 0 indicates no limit; to disable pooling, set ``poolclass`` to
        :class:`~sqlalchemy.pool.NullPool` instead.

    :param pool_recycle=-1: this setting causes the pool to recycle
        connections after the given number of seconds has passed. It
        defaults to -1, or no timeout. For example, setting to 3600
        means connections will be recycled after one hour. Note that
        MySQL in particular will disconnect automatically if no
        activity is detected on a connection for eight hours (although
        this is configurable with the MySQLDB connection itself and the
        server configuration as well).

        .. seealso::

            :ref:`pool_setting_recycle`

    :param pool_reset_on_return='rollback': set the
        :paramref:`_pool.Pool.reset_on_return` parameter of the underlying
        :class:`_pool.Pool` object, which can be set to the values
        ``"rollback"``, ``"commit"``, or ``None``.

        .. seealso::

            :paramref:`_pool.Pool.reset_on_return`

    :param pool_timeout=30: number of seconds to wait before giving
        up on getting a connection from the pool. This is only used
        with :class:`~sqlalchemy.pool.QueuePool`. This can be a float but is
        subject to the limitations of Python time functions which may not be
        reliable in the tens of milliseconds.

        .. note: don't use 30.0 above, it seems to break with the :param tag

    :param pool_use_lifo=False: use LIFO (last-in-first-out) when retrieving
        connections from :class:`.QueuePool` instead of FIFO
        (first-in-first-out). Using LIFO, a server-side timeout scheme can
        reduce the number of connections used during non- peak   periods of
        use.   When planning for server-side timeouts, ensure that a recycle or
        pre-ping strategy is in use to gracefully   handle stale connections.

          .. versionadded:: 1.3

          .. seealso::

            :ref:`pool_use_lifo`

            :ref:`pool_disconnects`

    :param plugins: string list of plugin names to load.  See
        :class:`.CreateEnginePlugin` for background.

        .. versionadded:: 1.2.3

    :param query_cache_size: size of the cache used to cache the SQL string
     form of queries.  Set to zero to disable caching.

     The cache is pruned of its least recently used items when its size reaches
     N * 1.5.  Defaults to 500, meaning the cache will always store at least
     500 SQL statements when filled, and will grow up to 750 items at which
     point it is pruned back down to 500 by removing the 250 least recently
     used items.

     Caching is accomplished on a per-statement basis by generating a
     cache key that represents the statement's structure, then generating
     string SQL for the current dialect only if that key is not present
     in the cache.   All statements support caching, however some features
     such as an INSERT with a large set of parameters will intentionally
     bypass the cache.   SQL logging will indicate statistics for each
     statement whether or not it were pull from the cache.

     .. note:: some ORM functions related to unit-of-work persistence as well
        as some attribute loading strategies will make use of individual
        per-mapper caches outside of the main cache.


     .. seealso::

        :ref:`sql_caching`

     .. versionadded:: 1.4

    """  # noqa

        self.session = None
        self.session_id = 0
        self.client_id = 0
        self._url = url
        self._kwargs = kwargs
        self._alias = alias
        self.client: SqlaEngine = create_db_engine(url,
                                                   alias=alias,
                                                   create_table=create_table,
                                                   pool_size=pool_size,
                                                   max_overflow=max_overflow,
                                                   pool_recycle=pool_recycle,
                                                   pool_pre_ping=pool_pre_ping,
                                                   pool_reset_on_return=pool_reset_on_return,
                                                   echo=echo,
                                                   autocommit=autocommit,
                                                   **kwargs)

        self.bind(self.client)
        self._add_sessions()

    def _add_sessions(self):
        if self._alias not in _sessions:
            _sessions[self._alias] = self

    def __call__(self, func=None,
                 *,
                 alias=DEFAULT_CONNECTION_NAME):
        """

        :param alias:  连接别名

        :return:
        """

        # 修饰器连接池
        if func is None:
            return partial(self.__call__,
                           alias=alias)

        def start_handler_hook():
            """
            调用方法前准备
            :return:
            """

        def end_handler_hook():
            """
            方法执行结束调用
            :return:
            """

        def _filter_kwargs(kwargs):
            if '__Illegal_mix_of_collations' in kwargs:
                kwargs.pop('__Illegal_mix_of_collations')
            return kwargs

        def check_mysql_collation_connection(kwargs):
            # mysql8 存在编码字符集问题问题
            if '__Illegal_mix_of_collations' in kwargs:
                mysql_collations_status = kwargs['__Illegal_mix_of_collations']

            else:
                mysql_collations_status = False

            return mysql_collations_status

        def mysql_set_collation_connection():
            sql = 'SET collation_connection = @@collation_database;'
            session.execute(sql)

        # 修饰器连接池
        @session_retries
        def _session_context_wrapper(*args, **kwargs):
            try:
                mysql_collations_status = check_mysql_collation_connection(kwargs)
                _session_wrap = get_wrapper_session(self.client_id)
                kwargs = _filter_kwargs(kwargs)

                if not _session_wrap:
                    # 第一次创建 申请一个数据库连接
                    _session = self.create_session()
                    with SessionContext(_session):
                        if mysql_collations_status:
                            mysql_set_collation_connection()
                        return func(*args, **kwargs)
                else:
                    if mysql_collations_status:
                        mysql_set_collation_connection()
                    return func(*args, **kwargs)
            except Exception as e:

                raise e

        return _session_context_wrapper

    def bind(self, db_engine: SqlaEngine):
        """
        绑定db_engine
        # 初始化

        """
        if not isinstance(db_engine, SqlaEngine):
            # TODO raise err
            raise Exception
        self.client = db_engine
        self.client_id = id(self.client)
        self.session = self.create_session()
        self.session_id = id(self.session)

    def create_session(self):

        return self.client.session

    @property
    def engine(self):
        return self.client.engine


class DbSession:

    def __call__(self, func=None,
                 *,
                 alias=DEFAULT_CONNECTION_NAME):
        """

        :param alias:  连接别名

        :return:
        """

        # 修饰器连接池
        if func is None:
            return partial(self.__call__,
                           alias=alias)

        session_ctx = _sessions.get(alias)
        if not session_ctx:
            raise RuntimeError(_session_ctx_err_msg.format(alias))

        @session_ctx
        def _wrapper_function(*args, **kwargs):

            return func(*args, **kwargs)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return _wrapper_function(*args, **kwargs)

        return wrapper


db_session = DbSession()

session: Session = ctx_session
# 指定类型 方便ide联想输入
