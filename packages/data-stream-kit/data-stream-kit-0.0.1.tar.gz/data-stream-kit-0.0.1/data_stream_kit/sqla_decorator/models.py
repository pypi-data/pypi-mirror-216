# -*- coding:utf-8 -*-

# @Time      :2022/8/5 10:47
# @Author    :huangkewei

from sqlalchemy import Column, Float, Index, Integer, String, text
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.util import immutabledict

Base = declarative_base()
metadata = Base.metadata


class DataCleanRunningLogV2(Base):
    __abstract__ = True

    record_pk = Column(Integer, primary_key=True)
    start_pk = Column(Integer, comment='开始处理的编号')
    end_pk = Column(Integer, comment='结束处理的编号')
    select_time = Column(Float(asdecimal=True), comment='查询数据用时')
    deal_time = Column(Float(asdecimal=True), comment='处理数据用时')
    insert_time = Column(Float(asdecimal=True), comment='插入数据用时')
    count = Column(Integer, server_default=text("'0'"), comment='每次插入的数据')
    status = Column(Integer, server_default=text("'0'"),
                    comment='标记该段数据是否成功处理 0 初始状态 1处理成功 2等待处理3处理失败')
    mac_address = Column(String(40), comment='处理脚本所在电脑的网卡地址')
    host_ip = Column(String(40), comment='处理脚本所在电脑的ip地址')
    hostname = Column(String(40), comment='处理脚本所在电脑的hostname')
    script_name = Column(String(100), comment='处理脚本的名称')
    hash = Column(String(40), index=True, comment='用于日志记录更新')
    create_time = Column(DATETIME(fsp=6), nullable=False, server_default=text("CURRENT_TIMESTAMP(6)"),
                         comment='日志创建时间')
    update_time = Column(DATETIME(fsp=6), nullable=False,
                         server_default=text("CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)"),
                         comment='日志更新时间')


class LogLock(Base):
    __tablename__ = 'log_lock'
    __table_args__ = (
        Index('idx_script', 'script_name', 'record_pk'),
    )

    record_pk = Column(Integer, primary_key=True)
    script_name = Column(String(100), unique=True, comment='处理脚本的名称')
    thread_id = Column(String(100), comment='线程id')
    create_time = Column(DATETIME(fsp=6), nullable=False, server_default=text("CURRENT_TIMESTAMP(6)"))


def make_log_model(table_name):
    if table_name in metadata.tables:
        all_table = dict(metadata.tables)
        all_table.pop(table_name)
        metadata.tables = immutabledict(all_table)

    table_name_lst = table_name.split('_')
    table_class_name = ''.join([name.title() for name in table_name_lst])
    table_class = type(table_class_name, (DataCleanRunningLogV2,), {'__tablename__': table_name})

    return table_class
