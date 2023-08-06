# -*- coding: utf-8 -*-

"""
# Created on 2021/11/9 8:46 下午
---------
Summary:

---------
# @Author  : zhuyaowen
# @Email  : zhuyaowen@chinasofti.com

"""
import inspect


def get_func_default_argspec(func) -> dict:
    """
    获取指定方法的默认参数
    :param func:
    :return:
    """
    argspec_info = inspect.getfullargspec(func)
    # spec_args = argspec_info.args  # args list
    # spec_varargs = argspec_info.varargs
    # spec_varkw = argspec_info.varkw
    args = argspec_info.args
    defaults = list(argspec_info.defaults or [])
    args = args[len(args) - len(defaults):]

    return dict(zip(args, defaults))


# 测试
def default_demo1(d, a=None, b=1, c='a', *arg, **kwargs):
    return 1


def default_demo2(d, *arg, **kwargs):
    return 1


def default_demo3(*arg, **kwargs):
    return 1


def default_demo4(a=None, b=1, c='a', *arg, **kwargs):
    return 1


def main():
    r = get_func_default_argspec(default_demo1)
    print(r)
    r = get_func_default_argspec(default_demo2)
    print(r)
    r = get_func_default_argspec(default_demo3)
    print(r)
    r = get_func_default_argspec(default_demo4)
    print(r)


if __name__ == '__main__':
    main()
