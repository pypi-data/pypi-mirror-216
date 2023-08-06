# -*- coding: utf-8 -*-

"""
# Created on 2021/11/14 11:03 下午
---------
Summary:

---------
# @Author  : zhuyaowen
# @Email  : zhuyaowen@chinasofti.com

"""

import json
import logging
from datetime import datetime

from sqlalchemy import update, and_, case, select, desc
from sqlalchemy.orm.session import Session

from ..session_ctx import ctx_session

try:
    from sqlalchemy.engine.row import Row
    from sqlalchemy.engine.result import ChunkedIteratorResult
    sqlalchemy_version = '1.4'
except ModuleNotFoundError:
    sqlalchemy_version = '1.3'

try:
    from sqlalchemy.engine.result import ResultProxy, RowProxy, ChunkedIteratorResult
except ImportError:
    # sqlalchemy 1.4以上用法
    from sqlalchemy.engine.cursor import CursorResult as ResultProxy
    from sqlalchemy.engine.row import RowProxy
    from sqlalchemy.engine.result import ChunkedIteratorResult

from sqlalchemy.ext.compiler import compiles

try:
    from sqlalchemy.ext.declarative.api import DeclarativeMeta
except ImportError:
    from sqlalchemy.ext.declarative import DeclarativeMeta

from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.expression import Insert

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

session: Session = ctx_session
logger = logging.getLogger(__name__)


@compiles(Insert)
def sqlalchemy_hook_string(insert, compiler, **kw):
    s = compiler.visit_insert(insert, **kw)

    if 'append_string' in insert.kwargs:
        # hook  sql  在sql语句后添加 ON DUPLICATE KEY UPDATE
        s = s + " " + insert.kwargs['append_string']

    if 'sqlalchemy_replace_string' in insert.kwargs:
        # INSERT INTO  自动替换成 REPLACE INTO
        s = s.replace("INSERT INTO", "REPLACE INTO")
    return s


def generate_models_field(models, keys: list):
    """
    根据传入key 值生成待查询字段
    :param models:
    :param keys:
    :return:
    """
    fields = [getattr(models, k) for k in keys if hasattr(models, k)]

    return fields


def sqlalchemy_join_result_format(results):
    if not results or not isinstance(results, list):
        return results

    join_models_len = len(results[0])

    datas = []

    for n in range(join_models_len):

        d_lst = [d[n] for d in results]
        v = d_lst[0]
        if isinstance(type(v), DeclarativeMeta):
            d_lst = sqlalchemy_result_format(d_lst)

        datas.append(d_lst)

    res = list(zip(*datas))
    return res


def sqlalchemy_result_field_format(data):
    keys = []

    if isinstance(data, RowProxy):
        keys = data.keys()

    elif 'sqlalchemy.util._collections.result' in str(type(data)):
        meta_attrs = type(data).__dict__
        _real_fields = meta_attrs.get("_real_fields") or []
        keys.extend(_real_fields)
    else:
        meta_attrs = type(data).__dict__
        for k, v in meta_attrs.items():
            if k.startswith('__') or type(v) is not InstrumentedAttribute:
                continue
            keys.append(k)

    return keys


def sqlalchemy_result_format(results, format_datetime=False):
    if isinstance(type(results), DeclarativeMeta):
        results = [results, ]

    elif isinstance(results, (ResultProxy, Query, ChunkedIteratorResult)):
        if hasattr(results, 'fetchall'):
            results = results.fetchall()
        else:
            results = results.all()

    if not results or not isinstance(results, list):
        return results

    if hasattr(results[0], '_data') and hasattr(results[0]._data[0], 'metadata'):
        results = [d[0] for d in results]

    keys = sqlalchemy_result_field_format(results[0])

    output = []
    for result in results:
        option = {}
        if result is None:
            output.append(option)
            continue
        for k in keys:
            v = getattr(result, k)

            if format_datetime:
                option[k] = format_datetime_to_str(v)
            else:
                option[k] = v

        output.append(option)
    return output


def result_to_dict_1_4(res):
    result = res.all()
    if not result:
        return []

    if sqlalchemy_version == '1.4' and \
            isinstance(result[0], Row):
        return result_to_dict_1_3(result)
        result = [d[0] for d in result]


    format_res = []
    for one in result:
        res = vars(one)
        if '_sa_instance_state' in res:
            del res['_sa_instance_state']

        format_res.append(res)

    return format_res


def result_to_dict_1_3(result):
    result = [dict(row) for row in result]

    return result


def sqlalchemy_result_format_new(result):
    if isinstance(result, Query) or \
            (sqlalchemy_version == '1.4' and isinstance(result, ChunkedIteratorResult)):
        return result_to_dict_1_4(result)
    else:
        return result_to_dict_1_3(result)


def sqlalchemy_data_commit(models,
                           data_lst: list,
                           mode='ignore',
                           on_duplicate_key='',
                           auto_commit=False,
                           filter_args: set = None,
                           ignore_exception=True):
    """
    通用入库模块
    调用本方法必须用@db_session 修饰
    """
    status = True

    if not data_lst:
        return status
    try:
        filter_args = filter_args if isinstance(filter_args, (list, tuple, set, dict)) else {'record_pk', 'op_time'}
        data_lst = check_models_len(models, data_lst, filter_args=filter_args)

        if on_duplicate_key:

            sql = models.__table__.insert(append_string=on_duplicate_key).values(data_lst)
            session.execute(sql)

        elif mode == 'ignore':

            session.execute(
                models.__table__.insert().prefix_with('IGNORE'),
                data_lst
            )
        elif mode == 'replace':
            sql = models.__table__.insert(sqlalchemy_replace_string='replace').values(data_lst)
            session.execute(sql)

        else:
            sql = models.__table__.insert().values(data_lst)
            session.execute(sql)
        if auto_commit:
            session.commit()

    except Exception as e:
        logger.error(e)
        if auto_commit:
            session.rollback()
        if not ignore_exception:
            raise e
        status = False

    return status


def sqlalchemy_update_generate_uniq_key(keys: set = None, data: dict = None):
    data = data or {}
    keys = keys or set()

    format_datas = [(k, v) for k, v in data.items() if k in keys]

    return tuple(format_datas)


def sqlalchemy_update_format_datas(models: Base,
                                   data_lst: list,
                                   update_key='record_pk'):
    if not data_lst:
        return {}

    keys = data_lst[0].keys()
    assert update_key in keys and getattr(models, update_key)

    keys = set(keys)
    keys.remove(update_key)
    assert len(keys) >= 1

    results = {}
    data_mapping = {}

    for data in data_lst:
        update_v = data[update_key]
        uniq_tuple_datas = sqlalchemy_update_generate_uniq_key(keys=keys, data=data)  # 返回一个字典当做key值
        results.setdefault(uniq_tuple_datas, [])
        results[uniq_tuple_datas].append(update_v)

    return results


def generate_models_update_time(models):
    """
    如果models  存在update_time 自动更新时间
    :param models:
    :return:
    """
    result = {}
    if hasattr(models, 'update_time'):
        result['update_time'] = datetime.now()
    elif hasattr(models, 'updated_at'):
        result['updated_at'] = datetime.now()

    return result


def sqlalchemy_generate_where_condition(models: Base,
                                        data_lst: list,
                                        add_where_info=None,
                                        update_key='record_pk',
                                        ):
    """
    生成 update where条件

    :param models: 表的 model 类，必填
    :param data_lst: 需要更新的数据列表，必填
    :param add_where_info: 添加额外的筛选条件，默认为空字典
    :param update_key: 指定更新主键，默认为 record_pk
    :return: 返回  sqlalchemy 的 and_ 对象
    """

    if add_where_info is None:
        add_where_info = dict()

    cond_key = update_key
    cond_values = [v[cond_key] for v in data_lst]

    model = getattr(models, cond_key)

    args = [model.in_(cond_values), ]
    for where_k, where_v in add_where_info.items():
        model = getattr(models, where_k)
        if isinstance(where_v, list):
            args.append(model.in_(where_v))

        else:
            args.append(model == where_v)

    return and_(*args)


def sqlalchemy_generate_set_condition(models: Base,
                                      data_lst: list,
                                      update_key='record_pk'):
    """
    生成 update set 字段，使用case批量更新

    :param models: 表的 model 类，必填
    :param data_lst: 需要更新的数据列表，必填
    :param update_key: 指定更新主键，默认为 record_pk

    例子：
    输入：data_lst
    [{"record_pk": 1, "a": 1, "b": 1},{"record_pk": 2, "a": 1,, "b": 1},{"record_pk": 3, "a": 2,, "b": 1}]

    返回：
    {"a" : case record_pk when 1 then 1 when 2 then 1 when 3 then 2,
    "b" : case record_pk when 1 then 1 when 2 then 1 when 3 then 1}
    """

    set_condition = dict()
    set_condition_dict = dict()
    for data in data_lst:
        update_value = data.pop(update_key)
        for k, v in data.items():
            set_condition_dict.setdefault(k, [])
            set_condition_dict[k].append((update_value, v))

    for k, v in set_condition_dict.items():
        set_cond = dict(v)
        set_condition[k] = case(
            set_cond,
            value=getattr(models, update_key))

    return set_condition


def check_update_datas(data_lst: list,
                       update_key='record_pk', ):
    """
    删除列表中没有主键的数据

    :param data_lst: 需要更新的数据列表，必填
    :param update_key: 指定更新主键，默认为 record_pk
    :return: 筛选之后的 data_lst
    """

    data_lst = [x for x in data_lst if x.get(update_key, None) is not None]

    return data_lst


def sqlalchemy_update_data_by_case(models: Base,
                                   data_lst: list,
                                   update_key='record_pk',
                                   auto_commit=False,
                                   add_where_info=None):
    """
    批量更新数据

    :param models: 表的 model 类，必填
    :param data_lst: 需要更新的数据列表，必填
    :param update_key: 指定更新主键，默认为 record_pk
    :param auto_commit: 是否自动提交事务，默认为 False
    :param add_where_info: 添加额外的筛选条件，默认为None
    :return: 执行状态True/False

    例子：
    输入： data_lst
    [{"record_pk": 1, "a": 1, "b": 4},{"record_pk": 2, "a": 2,, "b": 5},{"record_pk": 3, "a": 3,, "b": 6}]
    根据后面 record_pk 值进行批量更新

    生成sql语句：
    UPDATE table_name
    SET a = CASE record_pk
        WHEN 1 THEN 1
        WHEN 2 THEN 2
        WHEN 3 THEN 3
    END,
    b = CASE record_pk
        WHEN 1 THEN 4
        WHEN 2 THEN 5
        WHEN 3 THEN 6
    END
    WHERE record_pk IN record_pk_list
    """
    status = True

    if not data_lst:
        return status
    try:
        add_where_info = add_where_info or {}
        data_lst = check_models_len(models, data_lst)
        data_lst = check_update_datas(data_lst=data_lst, update_key=update_key)

        update_time_kwargs = generate_models_update_time(models)
        _pk = getattr(models, update_key)

        where_info = sqlalchemy_generate_where_condition(models=models,
                                                         data_lst=data_lst,
                                                         update_key=update_key,
                                                         add_where_info=add_where_info)

        update_data = sqlalchemy_generate_set_condition(models=models,
                                                        data_lst=data_lst,
                                                        update_key=update_key)
        update_data.update(update_time_kwargs)

        stmt = update(models).where(where_info). \
            values(**update_data)
        session.execute(stmt)

        if auto_commit:
            session.commit()

    except Exception as e:
        logger.exception(e)
        if auto_commit:
            session.rollback()
        status = False

    return status


def sqlalchemy_update_data(models: Base,
                           data_lst: list,
                           update_key='record_pk',
                           auto_commit=False,
                           add_where_info=None):
    """
    通用批量更新模块 更新key值 必须存在主键
    调用本方法必须用@db_session 修饰

    data_lst

    [{"record_pk": 1, "a": 1, "b": 1},{"record_pk": 2, "a": 1,, "b": 1},{"record_pk": 3, "a": 2,, "b": 1}]
    根据后面 a 值进行批量更新  如果字典内容都不一样 则单条插入效率会非常低
    不支持多个值当做限制条件
    """
    status = True

    if not data_lst:
        return status
    try:
        add_where_info = add_where_info or {}
        data_lst = check_models_len(models, data_lst)
        update_datas = sqlalchemy_update_format_datas(models=models,
                                                      data_lst=data_lst,
                                                      update_key=update_key)

        update_time_kwargs = generate_models_update_time(models)
        _pk = getattr(models, update_key)
        for uniq_tuple_key, update_key_lst in update_datas.items():
            update_data = dict(uniq_tuple_key)
            update_data.update(update_time_kwargs)

            if update_key_lst:
                update_key_lst = sorted(update_key_lst)
                add_where_info[update_key] = update_key_lst
                where_info = sqlalchemy_generate_where_info(add_where_info, models)
                stmt = update(models).where(where_info). \
                    values(**update_data)
                session.execute(stmt)
        if auto_commit:
            session.commit()

    except Exception as e:
        logger.exception(e)
        if auto_commit:
            session.rollback()
        status = False

    return status


def sqlalchemy_generate_where_info(add_where_info, models):
    add_where_info = add_where_info or {}
    args = []
    for where_k, where_v in add_where_info.items():
        model = getattr(models, where_k)
        if isinstance(where_v, list):

            args.append(model.in_(where_v))
        else:

            args.append(model == where_v)
    return and_(*args)


def sqlalchemy_bulk_update_mappings(models: Base, data_lst: list, auto_commit=False):
    """
    通用批量更新模块 更新key值 必须存在主键
    调用本方法必须用@db_session 修饰
    """
    status = True

    if not data_lst:
        return status
    try:
        data_lst = check_models_len(models, data_lst)

        session.bulk_update_mappings(models, data_lst)
        if auto_commit:
            session.commit()

    except Exception as e:
        logger.error(e)
        if auto_commit:
            session.rollback()
        status = False

    return status


def models_kwargs_format(model,
                         kwargs: dict,
                         filter_args: set = None):
    filter_args = filter_args or {}

    kwg = {k: v for k, v in kwargs.items() if k not in filter_args and hasattr(model, k)}
    return kwg


def format_datetime_to_str(data):
    if isinstance(data, datetime):
        data = str(data)
    return data


def check_models_len(model, data_lst, label_filter=False, filter_args: set = None):
    """
    pg 不支持截断 根据models 定义的长度对传入的文本类型的数据进行去标签  并且超长截断
    :param model:
    :param data_lst:
    :param label_filter: 标签
    :return:
    """

    if not isinstance(data_lst, list):
        return data_lst
    if not model:
        return data_lst
    if not data_lst or not isinstance(data_lst[0], dict):
        return data_lst

    output_lst = []
    for each in data_lst:
        tmp_dict = {}
        for k, v in each.items():
            try:
                org = getattr(model, k).property.columns[0].type
                if org.python_type is type(''):
                    # models 中定义数据库类型为字符串进行超长检测
                    length = org.length

                    if isinstance(v, (dict, list)):
                        # models 定义成字符串 传入list  json 自动转换成str
                        v = json.dumps(v, ensure_ascii=False)
                    if length and isinstance(v, str) and len(v) > length:
                        v = v[:length]  # 对字符串进行截断

            except Exception as e:
                pass

            tmp_dict[k] = v

        output_lst.append(models_kwargs_format(model, tmp_dict, filter_args=filter_args))

    return output_lst


def merge_db_results(d1: list, d2: list, key: str, format_mapping: dict = None):
    """
    根据key  合并两个list 以第一个列表为主
    :param d1: [{'uniq': '1', 'c': '1'}]
    :param d2: [{'uniq': '1', 'c1': '1'}]
    :param key: uniq
    :param format_mapping: 需要格式化字段  {"brand_info": str, "brand_info": json.dumps}
    :return: [{'uniq': '1', 'c': '1', 'c1': '1'}]

    """

    # 一定保证 key 存在 d1  d2
    mapping = {d[key]: d for d in d2}
    format_mapping = format_mapping or {}
    output = []
    not_exisit_data = {}

    if mapping:
        # 生成未知key
        not_exisit_keys = d2[0].keys()
        not_exisit_data = {k: None for k in not_exisit_keys}

    for cell in d1:

        data = mapping.get(cell[key]) or not_exisit_data
        cell.update(data)
        for k, formater in format_mapping.items():
            if k in cell:
                cell[k] = formater(cell[k])
        output.append(cell)
    return output


def query_model_datas_from_outerjoin(model, join_model, join_type=None, filter_op=None, fields=None,
                                     join_fields=None,
                                     join_op=None, limit: int = 20,
                                     offset: int = 0, order_by=None, order_desc=None):
    """
    联表查询
    model 主表model
    join_model 关联表model
    join_type 连接类型
    filter_op 筛选条件
    fields 主表显示字段
    join_fields 关联表显示字段
    join_op 关联key值 例(model.uid == join_model.uid,)
    """

    fields = fields or ()
    join_fields = join_fields or ()
    # 连接条件
    join_op = join_op or ()

    if not model or not join_model:
        raise

    query = session.query(*fields, *join_fields)

    if join_type == 'left':
        # 左 isouter=True
        query = query.join(join_model, *join_op, isouter=True)
    else:
        # 内连接
        query = query.join(join_model, *join_op, )

    if filter_op:
        query = query.filter(*filter_op)

    if order_by and order_desc:
        query = query.order_by(desc(*order_by))
    elif order_by:
        query = query.order_by(*order_by)

    query = query.offset(offset).limit(limit)
    query = query.all()
    results = sqlalchemy_result_format(query)

    return results


