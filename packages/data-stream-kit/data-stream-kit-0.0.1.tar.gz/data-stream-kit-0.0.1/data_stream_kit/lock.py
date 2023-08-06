# -*- coding:utf-8 -*-

# @Time      :2022/7/15 15:07
# @Author    :huangkewei

import time

from redis import Redis
from pottery import Redlock

import logging
from datetime import datetime
from sqlalchemy import select, insert, delete, func, and_
from sqlalchemy.exc import IntegrityError, OperationalError

from .sqla_decorator.manager import session
from .sqla_decorator.models import LogLock
from .sqla_decorator.utils.db import sqlalchemy_result_format
from .sqla_decorator.manager import SessionContextManager


logger = logging.getLogger(__name__)


class LockMysql:
    """
    mysql分布式锁
    """

    def __init__(self, lock_session):

        self.init_database_ = False

        self.current_thread_id = -1
        self.lock_session = lock_session

    def lock(self, script_name, time_out=10):
        """ 获取锁 """
        if self.current_thread_id == -1:
            current_thread_id = session.execute("select connection_id() as con_id;")
            current_thread_id = sqlalchemy_result_format(current_thread_id)

            self.current_thread_id = current_thread_id[0]['con_id']

        data = {
            'script_name': script_name,
            'thread_id': self.current_thread_id,
            'create_time': datetime.now()
        }
        select_sql = select([LogLock.script_name, LogLock.thread_id, LogLock.create_time]).where(
            LogLock.script_name == script_name)
        delete_sql = delete(LogLock).where(LogLock.script_name == script_name)

        while True:
            try:
                # 尝试加锁
                data['create_time'] = datetime.now()
                insert_sql = insert(LogLock).values(data)

                res = session.execute(insert_sql)
                session.commit()

                return True
            except IntegrityError as ie:
                # 主键冲突
                res = session.execute(select_sql)
                res = sqlalchemy_result_format(res)
                # 若主键冲突，且没有查到对应的记录，则等待0.5s，跳过下面的判断
                # tidb会出现的情况，可能是由于tidb是分布式的，在某一个节点上查询不到对应的数据，
                # 需要等待一会，数据同步之后，才能查出来
                if not res:
                    time.sleep(0.5)
                    continue
                log_create_time = res[0]['create_time']
                use_lock_time = (datetime.now() - log_create_time).seconds

                lock_thread_id = res[0]['thread_id']
                thread_status_sql = 'select ID from information_schema.processlist where ID = %s' % lock_thread_id
                thread_status = session.execute(thread_status_sql)
                thread_status = sqlalchemy_result_format(thread_status)

                time_out = min(60, time_out)

                # 判断lock是否超时，若超时，则删除lock，否则，继续尝试获取锁
                if (use_lock_time >= 15 and not thread_status) or \
                        (use_lock_time >= time_out):
                    session.execute(delete_sql)
                    session.commit()
                    logger.info('delete timeout lock')

                else:
                    time.sleep(0.01)

            except OperationalError as oe:
                time.sleep(0.01)
                logger.error(oe)

    def unlock(self, script_name):
        """ 解锁 """
        try:
            where_condi = and_(LogLock.script_name == script_name,
                               LogLock.thread_id == self.current_thread_id)

            select_sql = select([LogLock.script_name, LogLock.thread_id, LogLock.create_time]). \
                where(where_condi)
            delete_sql = delete(LogLock).where(where_condi)

            # 查询数据，查看数据是否存在
            res = session.execute(select_sql)
            session.commit()

            res = sqlalchemy_result_format(res)
            if res:
                session.execute(delete_sql)
                session.commit()

            else:
                logger.info('lock timeout. deleted.')
        except OperationalError as oe:
            logger.error(oe)

    def init_database(self):
        """
        初始化日志锁表，若不存在则创建一个
        """

        create_sql = r"""create table `log_lock`(
	`record_pk` int NOT NULL AUTO_INCREMENT,
	`script_name` varchar(100) DEFAULT NULL COMMENT '处理脚本的名称',
	`thread_id` varchar(100) DEFAULT NULL COMMENT '线程id',
	`create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
	PRIMARY KEY (`record_pk`),
	UNIQUE KEY `uniq_index` (`script_name`) ,
	KEY `idx_script` (`script_name`,`record_pk`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3;"""
        show_tables = r"""SHOW TABLES LIKE 'log_lock';"""  # 查询指定表是否存在

        try:
            ret = session.execute(show_tables).fetchall()  # 检测日志表是否存在
            if not ret:
                # 未查询到表创建
                session.execute(create_sql)
            session.commit()
            is_ok = True
        except Exception as e:
            session.rollback()

            logger.exception(e)
            self.err_msg = str(e)
            is_ok = False
        finally:
            session.close()

        return is_ok

    def _lock(self, name, time_out: int = 20):
        def _decorator(func):
            @self.lock_session
            def _wrapper(*args, **kwargs):
                try:
                    if not self.init_database_:
                        self.init_database_ = self.init_database()
                    self.lock(name, time_out)
                    res = func(*args, **kwargs)
                    self.unlock(name)
                    return res
                except Exception as e:

                    raise e

            return _wrapper
        return _decorator


class LockRedis:
    """
    redis 锁
    """

    def __init__(self, lock_session):
        self.r = lock_session  # redis.from_url(url=LOCK_URI)

        self.red_lock = Redlock(key='name', masters={self.r})

    def acquire_entry(self, name: str, time_out: int = 10, **kwargs) -> bool:
        if self.red_lock.key == 'name':
            self.red_lock = Redlock(key=name, masters={self.r})

        res = self.red_lock.acquire(timeout=time_out)

        return res

    def release_entry(self, name: str) -> bool:
        res = self.red_lock.release()

        return not bool(res)

    def locked(self) -> bool:
        return bool(self.red_lock.locked())

    def _lock(self, name, time_out: int = 20):
        def _decorator(func):
            def _wrapper(*args, **kwargs):
                try:
                    self.acquire_entry(name, time_out)
                    res = func(*args, **kwargs)
                    self.release_entry(name)
                    return res
                except Exception as e:

                    raise e

            return _wrapper

        return _decorator


class Lock:
    """

    """

    def __init__(self, lock_session):
        self.lock_type = self.get_lock_type(lock_session)
        logger.info('使用 %s 锁' % self.lock_type.__name__)

        self.lock_instan = self.lock_type(lock_session)

    def get_lock_type(self, lock_session):
        if isinstance(lock_session, SessionContextManager):
            return LockMysql
        elif isinstance(lock_session, Redis):
            return LockRedis

    def __call__(self, name, time_out):
        return self.lock_instan._lock(name, time_out)

