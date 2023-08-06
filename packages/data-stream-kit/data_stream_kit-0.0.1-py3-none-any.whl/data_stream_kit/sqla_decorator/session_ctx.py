# -*- coding: utf-8 -*-

"""
# Created on 2021/9/29 5:08 下午
---------
Summary:

连接session  上线 可实现 协程 线程 进程 隔离
---------
# @Author  : zhuyaowen
# @Email  : zhuyaowen@chinasofti.com

"""

import inspect
import sys
from functools import partial

from sqlalchemy.exc import InvalidRequestError
from werkzeug.local import LocalProxy
from werkzeug.local import LocalStack

_ctx_err_msg = """\
Working outside of session_ctx.
数据库操作前请先添加修饰器 db_session

"""


def _get_session_wrapper_stack():
    stack_lst = inspect.stack()
    stack_lst.reverse()

    for stack_info in stack_lst:
        func_name = stack_info.function
        if func_name == '__session_context_wrapper':
            return stack_info

    return


def _lookup_object(name):
    top = _ctx_stack.top
    if top is None:
        raise RuntimeError(_ctx_err_msg)
    # stack_info = _get_session_wrapper_stack()
    # print(id(stack_info.frame))
    return getattr(top, name)


def check_lookup_object():
    top = _ctx_stack.top
    if top is None:
        return False
    return True


def _get_lookup_object(engine_id=0):
    session_lst = _ctx_stack._session_lst
    if not session_lst:
        return

    if not engine_id:
        return session_lst[-1]
    # print(session_lst)
    for sess in session_lst:
        if sess.engine_id == engine_id:
            return sess

    return


def check_wrapper_session():
    return check_lookup_object()


def get_wrapper_session(engine_id=0):
    return _get_lookup_object(engine_id=engine_id)


class LocalStackEx(LocalStack):

    @property
    def _session_lst(self):
        """The topmost item on the stack.  If the stack is empty,
        `None` is returned.
        """
        try:
            return self._local.stack
        except (AttributeError, IndexError):
            return []


# context locals
_ctx_stack = LocalStackEx()

ctx_session = LocalProxy(partial(_lookup_object, "session"))
ctx_session_id = LocalProxy(partial(_lookup_object, "session_id"))
_sentinel = object()


class SessionContext(object):
    """The Session context binds an application object
    """

    def __init__(self, session):
        self.session = session
        self.session_id = id(session)
        self.engine = session.engine
        self.engine_id = id(self.engine)
        # print(self.session_id)
        self._refcnt = 0

    def push(self):
        """Binds the app context to the current context."""
        self._refcnt += 1
        if hasattr(sys, "exc_clear"):
            sys.exc_clear()
        try:
            if self.session.autocommit:
                self.session.begin()
        except InvalidRequestError:
            pass
        _ctx_stack.push(self)

    def pop(self, exc=_sentinel):
        """Pops the app context."""
        try:
            self._refcnt -= 1
            if self._refcnt <= 0:
                if exc is _sentinel:
                    exc = sys.exc_info()[1]
        finally:
            if self.session.autocommit:
                self.session.flush()
            """
            This clears all items and ends any transaction in progress.

        If this session were created with ``autocommit=False``, a new
        transaction is immediately begun.  Note that this new transaction does
        not use any connection resources until they are first needed.

            """
            # 不能直接调用self.session.close()
            # autocommit=False 会重新创建一个空事务 导致改表死锁
            # self.session.close()
            _last_item = getattr(self.session, '_last_item', '')
            print(_last_item)
            if _last_item not in {'rollback', 'commit'}:
                # 防止重复提交
                self.session.rollback()  # 防止事务未提交
            rv = _ctx_stack.pop()
        assert rv is self, "Popped wrong app context.  (%r instead of %r)" % (rv, self)

    def __enter__(self):
        self.push()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.pop(exc_value)
