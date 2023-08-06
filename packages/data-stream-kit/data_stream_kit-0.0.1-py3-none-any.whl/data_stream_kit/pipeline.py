# -*- coding:utf-8 -*-

import time
import logging
import atexit
from sqlalchemy import update, insert, select, delete, func, and_
from sqlalchemy.inspection import inspect
from datetime import datetime, timedelta
from redis import from_url, Redis
from functools import partial

from .lock import Lock
from .sqla_decorator.manager import session
from .sqla_decorator.utils.db import sqlalchemy_result_format, sqlalchemy_data_commit, check_models_len
from .sqla_decorator.utils.tool import get_mac_address, list_data_cut, generate_uuid, get_host_ip, get_hostname
from .sqla_decorator.models import make_log_model, Base
from .sqla_decorator.manager import SessionContextManager

logger = logging.getLogger(__name__)

"""
使用说明
继承PipelineBase， 重写data_clean方法
    需要配置的有：select_session(必须), insert_session(必须), log_session, lock_session
    log_session, lock_session可以不配置。
        若log_session未配置，则默认等于insert_session
        若lock_session未配置，则默认等于log_session
"""


def check_mysql_set():
    """测试是否为mysql 且 支持set 变量"""

    sql = "SET @num = - 1, @num =  @num + 1;"
    try:
        session.execute(sql)
        status = True
    except Exception as e:
        logger.error(e)
        status = False

    return status


def get_primary_key(data_model: Base):
    """
    获取主键
    :param data_model:
    :return:
    """
    list_primary_key = []
    for primary_key in inspect(data_model).primary_key:
        primary_key_name = primary_key.name
        list_primary_key.append(primary_key_name)

    assert list_primary_key, 'models 不存在主键'
    _primary_key = list_primary_key[0]
    return _primary_key


def get_model_table_name(data_model: Base):
    """
    获取表名
    :param data_model:
    :return:
    """
    # __tablename__ = data_model.__tablename__
    selectable = inspect(data_model).selectable
    _tablename = str(selectable)

    return _tablename


def init_session(session_obj, alias='temp'):
    """
    初始化数据库链接
    """
    if isinstance(session_obj, str):
        if 'mysql' in session_obj:
            session_ = SessionContextManager(url=session_obj, alias=alias)
        elif 'redis' in session_obj:
            session_ = from_url(session_obj)
        else:
            raise '数据库链接格式有误'
        return session_
    elif isinstance(session_obj, (SessionContextManager, Redis)):
        return session_obj
    else:
        logger.error('数据库链接格式有误')
        raise '数据库链接格式有误'


class PipelineBase:
    def __init__(self,
                 select_data_models,
                 auto_increment_pk='record_pk',
                 log_table_name='data_clean_running_log',
                 script_version='v1',
                 limit=1000,
                 partitions=10,
                 lock_name='',
                 select_session='',
                 insert_session='',
                 log_session='',
                 lock_session='',
                 ):
        """
        :param select_data_models: 查询表的model，必须
        :param auto_increment_pk:  对应的自增主键，默认为record_pk
        :param log_table_name:   日志表名，可根据设置的表名创建一个新的日志表，默认为data_clean_running_log
        :param script_version:  版本号，默认为v1
        :param limit:  一次查询的数据量，默认为1000
        :param partitions:  查询一批数据的大小，默认为10
        :param lock_name: lock锁名， 默认为self._script_name
        :param select_session:  数据源，必须
        :param insert_session:  目标源，必须
        :param log_session:  日志表数据库连接，默认放在目标源
        :param lock_session:  锁表数据库连接，默认等于日志源，mysql/redis
        """

        # 同步程序唯一标识 _script_name
        self.err_msg = None
        self._select_data_models = select_data_models
        self._select_columns = None
        self._table_name = ''
        self.script_version = script_version
        self._script_name = ''

        self.auto_increment_pk = auto_increment_pk  # 自增主键

        # 主机信息
        self._mac_address = get_mac_address()  # 获取主机mac
        self._host_ip = get_host_ip()  # 获取主机ip
        self._hostname = get_hostname()  # 获取主机hostname

        self._quit = False  # 程序退出状态，若为True，则退出同步程序
        self._pk_info_group_lst = []  # 临时缓存日志信息
        self._old_pk_info_group_lst = []

        # 日志表信息
        self.start_pk = 0
        self.end_pk = 0
        self.select_time = 0
        self.deal_time = 0
        self.insert_time = 0
        self._status = 1
        self.update_hash = ''

        self.log_table_name = log_table_name
        self.DataCleanRunningLog = make_log_model(log_table_name)

        self.old_data_status = True  # 刚启动会进行判断是否存在之前状态为2 的未处理的数据
        self._support_set_status = None  # 是否支持纯sql查询pk段

        # 数据量参数
        self._limit = limit
        self._partitions = partitions

        self.data_commit_mode = 'ignore'  # 数据提交模式

        # 初始化数据库链接
        self.select_session = select_session
        self.insert_session = insert_session
        self.log_session = log_session
        self.lock_session = lock_session
        self._init_session()
        self.run_log_func(self.init_database)

        # redis/mysql lock
        self.lock_name = lock_name if lock_name else self.script_name
        self.lock = Lock(self.lock_session)

        # 注册管道退出函数
        self._atexit_register()

    @property
    def script_name(self):
        """
        生成 数据同步唯一脚本名
        :return:
        """
        if self._script_name:
            return self._script_name
        self._script_name = '#'.join((self.select_table_name, self._name, self.script_version))
        return self._script_name

    @property
    def _name(self):
        return self.__class__.__name__

    @property
    def select_table_name(self):
        return self._select_data_models.__tablename__

    @property
    def support_set_status(self):
        if self._support_set_status is None:
            self._support_set_status = check_mysql_set()
        return self._support_set_status

    def _init_session(self):
        if not self.log_session:
            self.log_session = self.insert_session

        if not self.lock_session:
            self.lock_session = self.log_session

        self.select_session = init_session(self.select_session, alias='select')
        self.insert_session = init_session(self.insert_session, alias='insert')
        self.log_session = init_session(self.log_session, alias='log')
        self.lock_session = init_session(self.lock_session, alias='lock')

    def start_pipeline(self):
        # 开始运行管道时，先修改之前未处理的日志状态
        self.run_log_func(self.exit_pipeline)

    def _atexit_register(self):
        exit_run = partial(self.run_log_func, func=self.exit_pipeline)
        atexit.register(exit_run)

    def exit_pipeline(self):
        try:
            # 管道退出时，将当前脚本未处理的日志状态改为3
            l = self.DataCleanRunningLog
            where_ = and_(l.mac_address == self._mac_address,
                          l.host_ip == self._host_ip,
                          l.hostname == self._hostname,
                          l.script_name == self._script_name,
                          l.status == 2)
            update_status_sql = update(l). \
                where(where_). \
                values(status=3)
            session.execute(update_status_sql)
            logger.info('已修改未处理的日志状态')
        except Exception as e:
            session.rollback()
            logger.exception(e)
        finally:
            session.commit()

    def run_select_func(self, func, *args, **kwargs):
        @self.select_session
        def _run_select_func():
            return func(*args, **kwargs)

        return _run_select_func()

    def run_log_func_with_lock(self, func, *args, **kwargs):
        @self.lock(self.lock_name, time_out=60)
        @self.log_session
        def _run_log_func():
            return func(*args, **kwargs)

        return _run_log_func()

    def run_log_func(self, func, *args, **kwargs):
        @self.log_session
        def _run_log_func():
            return func(*args, **kwargs)

        return _run_log_func()

    def run_insert_func(self, func, *args, **kwargs):
        @self.insert_session
        def _run_insert_func():
            return func(*args, **kwargs)

        return _run_insert_func()

    def init_database(self):
        """
        初始化日志表，若不存在则创建一个

        :return:
        """
        create_sql = r"""
        CREATE TABLE `%s` (
          `record_pk` int(10) NOT NULL AUTO_INCREMENT,
          `start_pk` int(10) DEFAULT NULL COMMENT '开始处理的编号',
          `end_pk` int(10) DEFAULT NULL COMMENT '结束处理的编号',
          `select_time` double DEFAULT NULL COMMENT '查询数据用时',
          `deal_time` double DEFAULT NULL COMMENT '处理数据用时',
          `insert_time` double DEFAULT NULL COMMENT '插入数据用时',
          `count` int(10) DEFAULT '0' COMMENT '每次插入的数据',
          `status` int(10) DEFAULT '0' COMMENT '标记该段数据是否成功处理 0 初始状态 1处理成功 2等待处理 3处理失败',
          `mac_address` varchar(40) DEFAULT NULL COMMENT '处理脚本所在电脑的网卡地址',
          `host_ip` varchar(40) DEFAULT NULL COMMENT '处理脚本所在电脑的ip地址',
          `hostname` varchar(40) DEFAULT NULL COMMENT '处理脚本所在电脑的hostname',
          `script_name` varchar(100) DEFAULT NULL COMMENT '处理脚本的名称',
          `hash` varchar(40) DEFAULT NULL COMMENT '用于日志记录更新',
          `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '日志创建时间',
          `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '日志更新时间',
          PRIMARY KEY (`record_pk`),
          KEY `idx_status` (`script_name`, `end_pk`, `status`) USING BTREE,
          KEY `idx_host` (`mac_address`, `host_ip`, `hostname`, `script_name`) USING BTREE,
          KEY `idx_hash` (`hash`) USING HASH
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;""" % self.log_table_name
        show_tables = r"""SHOW TABLES LIKE '%s';""" % self.log_table_name  # 查询指定表是否存在

        try:
            logger.info('检查日志表: %s 是否存在.', self.log_table_name)
            ret = session.execute(show_tables).fetchall()  # 检测日志表是否存在
            if not ret:
                # 未查询到表创建
                logger.info('未查询到日志表，创建日志表: %s.', self.log_table_name)
                session.execute(create_sql)
            session.commit()
            logger.info('已创建日志表: %s.', self.log_table_name)
            is_ok = True
        except Exception as e:
            session.rollback()

            logger.exception(e)
            self.err_msg = str(e)
            is_ok = False
        finally:
            session.close()

        return is_ok

    def get_data_pk(self, limit=1000, partitions=100):
        """
        获取数据的pk段

        1. 判断是否有未同步的数据
        2. 判断是否存在未处理的数据
        3. 查询后续的数据（加锁/解锁）

        :return:
        """

        # 检查旧日志数据
        if self.old_data_status:
            if not self._old_pk_info_group_lst:
                self._old_pk_info_group_lst = self.run_log_func_with_lock(self.get_data_pk_old)
            if self._old_pk_info_group_lst:
                info = self._old_pk_info_group_lst.pop(0)
                self.start_pk = info['start_pk']
                self.end_pk = info['end_pk']
                self.update_hash = info['update_hash']
                return self.start_pk, self.end_pk, self.update_hash

        # 检查日志数据
        if not self._pk_info_group_lst:
            self._pk_info_group_lst = self.run_log_func_with_lock(self.get_data_pk_all,
                                                                  limit=limit,
                                                                  partitions=partitions)
        if not self._pk_info_group_lst:
            return None, None, None
        info = self._pk_info_group_lst.pop(0)
        self.start_pk = info['start_pk']
        self.end_pk = info['end_pk']
        self.update_hash = info['hash']
        return self.start_pk, self.end_pk, self.update_hash

    def get_data_pk_old(self):
        """
        从日志表获取旧数据

        :return:
        """
        if not self.old_data_status:
            return []
        # now = datetime.now()
        # old_time_2h = now + timedelta(minutes=-120)
        # old_time_2h_str = old_time_2h.strftime('%Y-%m-%d %H:%M:%S')  # 获取2小时之前的时间
        # now_time_str = now.strftime('%Y-%m-%d %H:%M:%S')

        # 查询日志表中是否存在未处理数据
        results = session.query(self.DataCleanRunningLog) \
            .filter(self.DataCleanRunningLog.status == 3,
                    # self.DataCleanRunningLog.op_time < old_time_2h_str,
                    self.DataCleanRunningLog.script_name == self.script_name) \
            .order_by(self.DataCleanRunningLog.end_pk.desc()) \
            .limit(50).with_for_update().all()

        results = sqlalchemy_result_format(results)
        if results:
            # 查询到存在未处理数据,更新处理时间
            record_pk_lst = [cell['record_pk'] for cell in results]
            option = {'status': 2}

            stmt = update(self.DataCleanRunningLog). \
                where(self.DataCleanRunningLog.record_pk.in_(record_pk_lst)). \
                values(**option)
            session.execute(stmt)
        session.commit()

        if not results:
            self.old_data_status = False
            return []

        output = [{
            'start_pk': call['start_pk'],
            'end_pk': call['end_pk'],
            'update_hash': call['hash']
        } for call in results]

        return output

    def get_data_pk_all(self, limit=1000, partitions=100):
        """
        获取新数据，并更新日志表
        :return:
        """

        # 查询日志表中 最大pk
        results = session.query(self.DataCleanRunningLog) \
            .filter(self.DataCleanRunningLog.script_name == self.script_name) \
            .order_by(self.DataCleanRunningLog.end_pk.desc()) \
            .limit(1).with_for_update().all()

        results = sqlalchemy_result_format(results)
        if results:
            old_end_pk = results[0]['end_pk'] + 1
        else:
            old_end_pk = 1

        # 从数据列表中 获取查询pk段
        if self.support_set_status:
            # sql  模式  相比self.get_select_pk_group 性能提升10倍
            pk_results = self.run_select_func(self.get_select_pk_group_down_sample_sql,
                                              start_pk=old_end_pk,
                                              limit=limit,
                                              partitions=partitions)
        else:
            # 不兼容 模式
            pk_results = self.run_select_func(self.get_select_pk_group,
                                              start_pk=old_end_pk,
                                              limit=limit,
                                              partitions=partitions)

        if not pk_results:
            self._quit = True
            output = []
        else:
            output = self.run_log_func(self.insert_data_to_running_log, pk_results)

        return output

    def get_select_pk_group_down_sample_sql(self, start_pk, limit, partitions=10):
        """
        纯sql 语句实现 并且通过数据库降采样聚合返回 只适用于mysql
        查询性能提升5-10倍   在几十个节点的场景下能有效避免锁等待

        :param start_pk: 起始pk
        :param limit:    一个批次的数据量
        :param partitions: 一次查询的批次数
        :return: pk段列表
        """

        if not limit:
            limit = 1
        total = limit * partitions

        _primary_key = get_primary_key(self._select_data_models)

        table_name = get_model_table_name(self._select_data_models)

        set_sql = """SET @num = -1, @pk_interval = {pk_interval};"""
        session.execute(set_sql.format(pk_interval=limit))  # 初始化连接变量

        select_sql = """
            SELECT
            min({increment_pk}) as min_pk,
            max({increment_pk}) as max_pk
            FROM
        	(
        	SELECT
        		{increment_pk},
        		@num := @num + 1 ,
        		@num DIV @pk_interval AS __div_num 
        	FROM
        		{table_name} 
        	WHERE
        		{increment_pk} >= {start_pk} 
        	ORDER BY
        		{increment_pk} 
        	LIMIT {total}
        	) AS __a GROUP BY __div_num;
        	"""

        select_sql = select_sql.format(increment_pk=_primary_key,
                                       table_name=table_name,
                                       total=total,
                                       start_pk=start_pk)

        results = session.execute(select_sql)

        results = sqlalchemy_result_format(results)
        output = []

        if results:

            for data in results:
                start_pk = data.get('min_pk')
                end_pk = data.get('max_pk')
                output.append((start_pk, end_pk))
            output.sort(key=lambda x: x[0])

        return output

    def get_select_pk_group(self, start_pk, limit, partitions=10):
        """

        :param start_pk:
        :param limit:
        :param partitions:
        :return:
        """

        if not limit:
            limit = 1
        total = limit * partitions
        _primary_key = get_primary_key(self._select_data_models)

        increment_pk_models = getattr(self._select_data_models, _primary_key)
        # _updated_at = getattr(self._select_data_models, self.field_updated_at)
        query = session.query(increment_pk_models) \
            .filter(increment_pk_models >= start_pk)
        # if _updated_at:
        #     # 限制 只清洗30S前抓取数据
        #     mysql_now = self.generate_mysql_time()
        #     query = query.filter(_updated_at < mysql_now)
        query = query.order_by(increment_pk_models) \
            .limit(total)
        results = query.all()
        results = sqlalchemy_result_format(results)
        output = []

        if results:
            group_datas = list_data_cut(results, step=limit)
            for data in group_datas:
                start_pk = data[0][self.auto_increment_pk]
                end_pk = data[-1][self.auto_increment_pk]
                output.append((start_pk, end_pk))
            output.sort(key=lambda x: x[0])

        return output

    def insert_data_to_running_log(self, datas):
        """
        插入日志

        :param datas: pk段数据
        :return:  日志数据
        """
        data_lst = []
        for data in datas:
            start_pk = data[0]
            end_pk = data[1]
            update_hash = generate_uuid()
            data_lst.append({
                "start_pk": start_pk,
                "end_pk": end_pk,
                "script_name": self.script_name,
                "mac_address": self._mac_address,
                "host_ip": self._host_ip,
                "hostname": self._hostname,
                "status": 2,
                "hash": update_hash,
                "count": self._limit
            })
        sqlalchemy_data_commit(models=self.DataCleanRunningLog,
                               data_lst=data_lst,
                               mode='insert',
                               auto_commit=True)

        return data_lst

    def select_data_by_pk(self, start_pk, end_pk):
        """
        根据pk段查询数据

        :return:
        """
        if self._quit or start_pk is None:
            return
        increment_pk_models = getattr(self._select_data_models, self.auto_increment_pk)
        field = self._select_columns or (self._select_data_models,)
        select_sql = select(field) \
            .where(and_(increment_pk_models >= start_pk,
                        increment_pk_models <= end_pk)) \
            .order_by(increment_pk_models)

        results = session.execute(select_sql)
        results = sqlalchemy_result_format(results)
        return results

    def update_data_by_hash(self, update_hash, **kwargs):
        """
        清洗完成后，更新日志状态

        :param update_hash: 需要更新的hash值
        :param kwargs: 状态值，以及各种时间
        :return:
        """
        if not update_hash:
            return
        _status = kwargs.get('status') or 1
        select_time = kwargs.get('select_time') or 0
        deal_time = kwargs.get('deal_time') or 0
        insert_time = kwargs.get('insert_time') or 0

        option = {'deal_time': deal_time,
                  'insert_time': insert_time,
                  'select_time': select_time,
                  'status': _status}
        option.update(kwargs)

        stmt = update(self.DataCleanRunningLog) \
            .where(self.DataCleanRunningLog.hash == update_hash) \
            .values(**option)
        session.execute(stmt)

        session.commit()

    def data_commit(self, data):
        """
        提交数据
        如果批量提交失败 需要手动解决
        """
        mode = self.data_commit_mode
        insert_data = data
        status = True
        if not insert_data:
            return status
        now = time.time()
        try:
            for tables_model, data_lst in insert_data:
                status = sqlalchemy_data_commit(models=tables_model,
                                                data_lst=data_lst,
                                                mode=mode,
                                                auto_commit=True)
                assert status
                logger.info('插入成功,models:{} ,{}条 time:{}'.format(tables_model.__tablename__,
                                                                      len(data_lst),
                                                                      round(time.time() - now, 5)))
                now = time.time()

        except Exception as e:
            logger.error(e)
            session.rollback()
            status = False

        return status

    def check_log_status(self):
        """
        最后验证是否还存在状态为2的日志

        1. 插入完成日志
        2. 判断应该脚本的日志是否大于设置的数量
        3. 若大于则执行更新状态函数

        self._quit 可设置为0, 1, 2
            0： 运行管道中
            1： 执行到完成，且未检查是否存在状态为2的日志
            2： 执行到完成，且检查过

        """

        logger.info('检查日志状态')
        l = self.DataCleanRunningLog
        script_name_finished = self.script_name + '_finished'
        insert_sql = insert(l).values([{'script_name': script_name_finished}])
        select_sql = select([func.count(l.script_name).label('cnt')]).where(l.script_name == script_name_finished)

        session.execute(insert_sql)
        session.commit()

        while True:
            res = session.execute(select_sql)
            res = sqlalchemy_result_format(res)
            cnt = int(res[0]['cnt'])
            if cnt < self._replicas:
                time.sleep(1)
                continue
            break

        self.run_log_func_with_lock(self.update_log_status)

    def update_log_status(self):
        """
        更新日志状态方法
        1. 修改 self.old_data_status 状态，
        2. 判断其他进程是否更新过了， 若更新过了，则跳过更新
        3. 若没有，则将所有日志状态中2改为3

        """
        self.old_data_status = True

        l = self.DataCleanRunningLog
        script_name_finished = self.script_name + '_finished'
        select_sql = select([func.count(l.script_name).label('cnt')]).where(l.script_name == script_name_finished)
        res = session.execute(select_sql)
        res = sqlalchemy_result_format(res)
        if not res:
            # 打印日志，其他脚本已执行
            logger.info('其他进程已更新状态。')
            return

        delete_sql = delete(l).where(l.script_name == script_name_finished)
        session.execute(delete_sql)
        session.commit()

        update_sql = update(l).where(and_(l.script_name == self.script_name,
                                          l.status == 2)).values(status=3)
        session.execute(update_sql)
        session.commit()

    def source_work(self):
        """
        mysql source 主函数

        :return: 数据、对应的hash、查询时间
        """

        now = time.time()
        self._status = 3
        start_pk, end_pk, _ = self.get_data_pk(limit=self._limit, partitions=self._partitions)  # 获取数据pk段
        results = self.run_select_func(self.select_data_by_pk, start_pk, end_pk)
        self.select_time = time.time() - now

        return results

    def sink_work(self, datas):

        try:
            now = time.time()
            status = self.run_insert_func(self.data_commit, datas)
            self.insert_time = time.time() - now

            assert status, '数据更新失败'
            self._status = 1
        except Exception as e:
            self._status = 3

    def print_info(self):
        msg = '{}   start_pk:{} end_pk:{}   select_time:{}  deal_time:{}  insert_time:{}'.format(
            self.script_name,
            str(self.start_pk),
            str(self.end_pk),
            str(round(self.select_time, 5)),
            str(round(self.deal_time, 5)),
            str(round(self.insert_time, 5))
        )
        logger.info(msg)

    def data_clean(self, datas):
        """
        数据清洗，子类实现

        返回格式：
        return [(model, data_lst), ...]
        """
        raise NotImplemented

    def run(self):
        self.start_pipeline()

        while not self._quit:
            try:
                results = self.source_work()
                if not results:
                    continue

                deal_time = time.time()
                datas = self.data_clean(datas=results)
                self.deal_time = time.time() - deal_time

                self.sink_work(datas)

                self.print_info()

            except Exception as e:
                logger.exception(e)

            finally:
                self.run_log_func(self.update_data_by_hash,
                                  update_hash=self.update_hash,
                                  select_time=self.select_time,
                                  deal_time=self.deal_time,
                                  insert_time=self.insert_time,
                                  status=self._status)
