# -*- coding: utf-8 -*-

"""
# Created on 2021/11/14 5:48 下午
---------
Summary:

---------
# @Author  : zhuyaowen
# @Email  : zhuyaowen@chinasofti.com

"""

import hashlib
import regex as re
import time
import os

try:
    import cchardet as chardet
except ImportError:
    import chardet
import logging
import uuid
import inspect
import math
import socket

logger = logging.getLogger(__name__)

RE_IGNORE_STACK_PATTERN = re.compile('pydev/pydevd|pydev/_pydev_imps', flags=re.I)
RE_SUB_CHAR_SCRIPT = re.compile(r'''<script[^>]*>[\s\S]*?</script[^>]*>''', flags=re.I)  # 去除script

md5string = lambda x: hashlib.md5(x.encode('utf-8')).hexdigest()


# 传入字符串返回MD5  默认flag=True  返回32位哈希  如果flag=False  则返回16位的MD5
def str_to_md5(text, flag=True):
    if not isinstance(text, str):
        # 传入字段不是字符串 直接返回
        return ''
    text = hashlib.md5(text.encode('utf-8')).hexdigest()
    if flag:
        return text
    else:
        return text[8:-8]


def get_filename_abs(path):
    file_name = os.path.split(os.path.realpath(path))[-1]
    return file_name


def get_mac_address():
    """
    获取本机的mac地址
    """
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


def generate_uuid():
    """
    生成随机 uuid
    :return: str
    """
    uuid4 = str(uuid.uuid4())
    now = str(time.time())
    task_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, uuid4 + now))
    task_id = task_id.replace('-', '')
    return task_id


def get_session_stack_hash():
    """

    获取当前堆栈文件名  以定位路径
    """
    stack_lst = inspect.stack()
    stack_lst.reverse()
    hash_data_lst = []
    for stack_info in stack_lst:
        func_name = stack_info.function
        filename = stack_info.filename
        if func_name in {'<module>'}:
            continue
        if RE_IGNORE_STACK_PATTERN.search(filename):
            continue
        last_file_name = get_filename_abs(filename)
        hash_data_lst.extend([func_name, last_file_name])

    hash_text = ''.join(hash_data_lst)
    stack_hash = str_to_md5(hash_text)[:16]

    return stack_hash


def list_data_cut(datas, step=10):
    # 将列表分割打包成指定大小

    d_len = len(datas)

    total = math.ceil(d_len / step)
    results = []
    for n in range(total):
        data = datas[n * step:(n + 1) * step]
        results.append(data)
    return results


# 过滤传入文本的html标签   &nbsp;|&quot;|&rdquo;|amp;|&gt;|&lt;  所有空格
def tag_filter(content, flag=0):
    """flag 0 为默认  1 专门跟火车头的全选一致"""
    if not isinstance(content, str):
        # 传入字段不是字符串 直接返回
        return ''
    if flag == 0:
        ret_text = re.sub(r'<[^>]*>|&nbsp;|&quot;|&rdquo;|amp;|&gt;|&lt;|\r|\n|\t', '', content)
    else:
        content = RE_SUB_CHAR_SCRIPT.sub('', content)  # 先去除脚本
        ret_text = re.sub(r'<[^>]*>|&nbsp;|\r|\n|\t', '', content).strip()
    return ret_text.strip()


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
        return ip


def get_hostname():
    hostname = socket.gethostname()
    return hostname
