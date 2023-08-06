# -*- coding:utf-8 -*-

# @Time   : 2023/6/26 13:33
# @Author : huangkewei

import json
from sqlalchemy import update, and_, case, insert, text


async def aiosession_execute(aiosession, sql, auto_commit=False):
    async with aiosession.begin() as tr:
        try:
            res = await aiosession.execute(sql)
            if auto_commit:
                await tr.commit()
            return res
        except Exception:
            await tr.rollback()
            raise


def models_kwargs_format(model,
                         kwargs: dict,
                         filter_args: set = None):
    filter_args = filter_args or {}

    kwg = {k: v for k, v in kwargs.items() if k not in filter_args and hasattr(model, k)}
    return kwg


def check_models_len(model, data_lst, filter_args: set = None):
    """
    pg 不支持截断 根据models 定义的长度对传入的文本类型的数据进行去标签  并且超长截断
    :param model:
    :param data_lst:
    :param filter_args: 筛选的字段
    :return:
    """

    if not model:
        return data_lst

    if not data_lst or \
            not isinstance(data_lst, list) or \
            not isinstance(data_lst[0], dict):
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

            except Exception:
                pass

            tmp_dict[k] = v

        output_lst.append(models_kwargs_format(model, tmp_dict, filter_args=filter_args))

    return output_lst


def check_update_datas(data_lst: list,
                       update_key='record_pk', ):
    """
    删除列表中没有主键的数据

    :param data_lst: 需要更新的数据列表，必填
    :param update_key: 指定更新主键，默认为 record_pk
    :return: 筛选之后的 data_lst
    """

    data_lst = [x for x in data_lst if x.get(update_key) is not None]

    return data_lst


def sqlalchemy_generate_where_condition(models,
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


def sqlalchemy_generate_set_condition(models,
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


def generate_sql_update_data_by_case(models,
                                     data_lst: list,
                                     update_key='record_pk',
                                     add_where_info=None):
    if not data_lst:
        return

    add_where_info = add_where_info or {}
    data_lst = check_models_len(models, data_lst)
    data_lst = check_update_datas(data_lst=data_lst, update_key=update_key)

    where_info = sqlalchemy_generate_where_condition(models=models,
                                                     data_lst=data_lst,
                                                     update_key=update_key,
                                                     add_where_info=add_where_info)

    update_data = sqlalchemy_generate_set_condition(models=models,
                                                    data_lst=data_lst,
                                                    update_key=update_key)
    update_sql = (
        update(models).
        where(where_info).
        values(**update_data)
    )

    return update_sql


async def aio_update_data_by_case(aiosession,
                                  models,
                                  data_lst: list,
                                  update_key='record_pk',
                                  auto_commit=False,
                                  add_where_info=None):
    if not data_lst:
        return True

    update_sql = generate_sql_update_data_by_case(
        models=models,
        data_lst=data_lst,
        update_key=update_key,
        add_where_info=add_where_info
    )
    try:
        await aiosession_execute(aiosession, update_sql, auto_commit)
        status = True
        return status
    except Exception as e:
        status = False

        raise e


def parse_field(field_exec):
    k, v = field_exec.split('=')

    k = k.replace('`', '').strip()
    v = text(v.strip())

    return k, v


def parse_on_duplicate_key(on_duplicate_key: str):
    field_lst = (
        on_duplicate_key.
        lower().
        replace('on duplicate key update', '').
        split(',')
    )
    field_lst = list(map(parse_field, field_lst))
    field_map = dict(zip(
        [d[0] for d in field_lst],
        [d[1] for d in field_lst]
    ))

    return field_map


def generate_sql_insert_data(models,
                             data_lst,
                             mode='ignore',
                             on_duplicate_key=''):
    if on_duplicate_key:
        insert_sql = insert(models, append_string=on_duplicate_key).values(data_lst)
        # duplicate_key = parse_on_duplicate_key(on_duplicate_key)
        # insert_sql = (  # from sqlalchemy.dialects.mysql import insert
        #     insert(models).
        #     values(data_lst).
        #     on_duplicate_key_update(**duplicate_key)
        # )

        return insert_sql

    if mode == 'ignore':
        insert_sql = (
            insert(models).
            values(data_lst).
            prefix_with('IGNORE')
        )
        return insert_sql

    elif mode == 'replace':
        insert_sql = insert(models, sqlalchemy_replace_string='replace').values(data_lst)
        return insert_sql

    else:
        insert_sql = insert(models).values(data_lst)
        return insert_sql


async def aio_insert_data(aiosession,
                          models,
                          data_lst: list,
                          mode='ignore',
                          on_duplicate_key='',
                          auto_commit=False,
                          filter_args: set = None):
    if not data_lst:
        return True

    filter_args = (
        filter_args
        if isinstance(filter_args, (list, tuple, set, dict))
        else {}
    )
    data_lst = check_models_len(models, data_lst, filter_args=filter_args)
    insert_sql = generate_sql_insert_data(models=models,
                                          data_lst=data_lst,
                                          mode=mode,
                                          on_duplicate_key=on_duplicate_key)

    try:
        await aiosession_execute(aiosession, insert_sql, auto_commit)
        return True
    except Exception as e:
        raise e


def generate_sql_test():
    # 生成sql测试
    from pipeline_data.sqla_decorator.models import LogLock

    datas = [
        {'script_name': 'test1', 'thread_id': 1},
        {'script_name': 'test2', 'thread_id': 2},
        {'script_name': 'test3', 'thread_id': 3},
    ]
    on_duplicate_key = '''
    ON DUPLICATE KEY UPDATE 
        `script_name` = values(script_name),
        thread_id = 1
    '''
    # o = parse_on_duplicate_key(on_duplicate_key)
    # print(o)
    # sql = generate_sql_insert_data(models=LogLock,
    #                                data_lst=datas,
    #                                mode='replace',
    #                                on_duplicate_key=on_duplicate_key)

    sql = generate_sql_update_data_by_case(
        models=LogLock,
        data_lst=datas,
        update_key='script_name'
    )
    print(sql)


if __name__ == '__main__':
    generate_sql_test()
