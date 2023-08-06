# -*- coding:utf-8 -*-

# @Time      :2022/10/21 14:26
# @Author    :huangkewei

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

package_name = 'data-stream-kit'
package_version = '0.0.1'
install_requires = [
    'sqlalchemy[asyncio]~=1.4.0',
    'pottery~=3.0.0',
    'regex~=2022.7.0',
    'cchardet~=2.1.0',
    'werkzeug~=2.3.0',
    'pymysql~=1.0.0',
    'aiomysql~=0.1.0',
    'confluent-kafka~=2.0.0',
    'psutil~=5.8.0',
]

setuptools.setup(
    name=package_name,
    version=package_version,
    author='huangkewei',
    description='数据处理工具',
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=install_requires
)
