### data-stream-kit

数据流处理工具包

主要功能：

1. **data_stream_kit.sqla_decorator**: sqlalchemy的高度封装，使用线程数据，实现修饰器的方式调用session。
2. **data_stream_kit.sqla_asyncio**: 简单封装了异步sqlalchemy的session。
3. **data_stream_kit.kafka_lib**: 封装了kafka的生产者KafkaProducer和消费者KafkaConsumer。
4. **data_stream_kit.kafka_asyncio**: 异步的kafka生产者AIOProducer和消费者AIOConsumer。



打包流程：

1. 生成wheel文件和源代码压缩包：`python setup.py sdist bdist_wheel`。
2. 上传生成的文件：`twine upload dist/*`。之后输入账号密码。
