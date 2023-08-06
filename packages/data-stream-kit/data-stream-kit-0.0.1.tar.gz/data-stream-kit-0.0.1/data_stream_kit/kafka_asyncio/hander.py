# -*- coding:utf-8 -*-

# @Time   : 2023/6/27 10:28
# @Author : huangkewei

import os
import gc
import time
import psutil
import logging
import asyncio
import confluent_kafka
from confluent_kafka import KafkaException

from threading import Thread

gc.set_threshold(50, 5, 5)

logger = logging.getLogger(__name__)


def delivery_report(err, msg):
    """
    生产消息之后的回调函数
    """
    if err is not None:
        # TODO 投递异常消息处理  高可用场景下需要做兜底处理
        logger.error('Message delivery failed: {}'.format(err))
    else:
        logger.debug('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


class Empty(Exception):
    def __init__(self, *args, **kwargs):
        pass


class AIOProducer:
    def __init__(self,
                 bootstrap_servers=None,
                 topic=None,
                 loop=None, ):
        self._topic = topic
        configs = self.get_default_configs()
        configs['bootstrap.servers'] = bootstrap_servers
        print(configs)
        self._loop = loop or asyncio.get_event_loop()
        self._producer = confluent_kafka.Producer(configs)
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop)
        self._poll_thread.start()

        self._producer_interval = 0.0

    def get_default_configs(self):
        producer_configs = {
            'bootstrap.servers': None,
        }
        return producer_configs

    def _poll_loop(self):
        while not self._cancelled:
            self._producer.poll(0.1)

    def close(self):
        self._cancelled = True
        self._poll_thread.join()

    def produce(self, topic, value, callback=delivery_report,
                *args, **kwargs):
        """
        A produce method in which delivery notifications are made available
        via both the returned future and on_delivery callback (if specified).
        """
        result = self._loop.create_future()

        def ack(err, msg):
            if err:
                self._loop.call_soon_threadsafe(
                    result.set_exception, KafkaException(err))
            else:
                self._loop.call_soon_threadsafe(
                    result.set_result, msg)
            if callback:
                self._loop.call_soon_threadsafe(
                    callback, err, msg)

        self._producer.produce(topic, value, on_delivery=ack,
                               *args, **kwargs)
        return result

    async def produce_loop(self, topic, value=None, *args, **kwargs):
        """
        循环插入 遇到BufferError 等待指定时间间隔重试 0.1 0.2 0.4 0.8 s 递增 最长等待 5S
        """
        while True:
            try:
                await self.produce(topic, value=value, *args, **kwargs)
                self._producer_interval = 0.0
                break
            except BufferError as e:
                logger.error(e)
                interval = self._producer_interval or 0.05
                interval = interval * 2
                self._producer_interval = interval if interval <= 5 else 5.0
                await asyncio.sleep(self._producer_interval)
                continue

    async def publish(self, topic=None, value=None, batch=None, auto_flush=False, *args, **kwargs):

        if 'callback' not in kwargs:
            kwargs['callback'] = delivery_report

        values = value if batch else [value, ]  # 批量投递
        topic = topic or self._topic
        assert topic

        for value in values:
            await self.produce_loop(topic, value=value, *args, **kwargs)

        if auto_flush:
            # 批量插入推荐使用
            self._producer.flush()


class AIOConsumer:
    def __init__(self, bootstrap_servers, group_id, topic, loop=None,
                 **kwargs):

        self._topic = topic
        configs = self.get_default_configs()

        for k_old, v in kwargs.items():
            k = k_old.replace('_', '.')
            if k not in configs:
                logger.warning(f'{k_old}参数不在默认配置中。')
            configs[k] = v

        configs['bootstrap.servers'] = bootstrap_servers
        configs['group.id'] = group_id

        self._loop = loop or asyncio.get_event_loop()
        self._consumer = confluent_kafka.Consumer(configs)
        self._consumer.subscribe(topics=[self._topic])
        self._callback_auto_commit = True

    def get_default_configs(self):
        producer_configs = {
            'bootstrap.servers': None,
            'group.id': None,
            'group.instance.id': None,
            'auto.offset.reset': 'earliest',
            'max.poll.interval.ms': 5 * 60 * 1000,
            'session.timeout.ms': 1 * 60 * 1000,
            'enable.auto.offset.store': False,
            'fetch.message.max.bytes': 1 * 1024 * 1024,
            'fetch.max.bytes': 100 * 1024 * 1024,
            'queued.max.messages.kbytes': 10 * 1024,
        }
        return producer_configs

    def get_latest_offset(self, msgs) -> dict:
        # 获取最新偏移量
        mapping = {}
        msgs = msgs if isinstance(msgs, list) else [msgs, ]

        for msg in msgs:
            partition = msg.partition()
            topic = msg.topic()
            offset = msg.offset()
            mapping.setdefault((topic, partition), msg)
            if offset > mapping[(topic, partition)].offset():
                mapping[(topic, partition)] = msg

        return mapping

    def auto_commit(self, msg_lst):
        if self._callback_auto_commit:
            # 回调结束后自动提交
            for m in self.get_latest_offset(msg_lst).values():
                self._consumer.commit(m, asynchronous=True)

    def callback(self, msg_lst):
        # todo 子类继承，回调处理消息
        for msg in msg_lst:
            print(int(time.time()), msg.value().decode())

    async def poll(self, timeout=1):
        """
        An awaitable consume method.
        """
        while True:
            msg = await self._loop.run_in_executor(None, self._consumer.poll, timeout)

            # if msg is None:
            #     continue
            yield msg

    async def consume(self,
                      num_messages=None,
                      callback_auto_commit=True,
                      timeout=1,
                      wait=False):
        num_messages = num_messages or 100
        self._callback_auto_commit = callback_auto_commit

        gen_msg = self.poll(timeout=timeout)
        msg_lst = []
        start_time = time.time()
        empty_time = time.time()
        async for msg in gen_msg:
            try:
                if msg is None:
                    raise Empty

                if msg and msg.error() is not None:
                    raise KafkaException(msg.error())

                get_time = time.time() - start_time

                msg_lst.append(msg)
                empty_time = time.time()

                if len(msg_lst) >= num_messages or \
                        (not wait and get_time > timeout):
                    self.callback(msg_lst)
                    self.auto_commit(msg_lst)
                    msg_lst = []
                    start_time = time.time()
            except Empty:
                msg_time = time.time() - empty_time
                if msg_time >= 60:
                    memory_usage = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
                    logger.info('当前进程的内存使用：%.4f MB' % memory_usage)
                    logger.info('%s 连续1分钟未获取到消息', self.__class__)
                    empty_time = time.time()
                continue
            except KafkaException as e:
                logger.error(e)
                await asyncio.sleep(3)
                continue
            except Exception as e:
                raise e


