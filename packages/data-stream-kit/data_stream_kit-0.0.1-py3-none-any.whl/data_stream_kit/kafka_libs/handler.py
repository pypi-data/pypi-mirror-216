# -*- coding: utf-8 -*-

"""
# Created on 2021/11/4 2:12 下午
---------
Summary:

---------
# @Author  : zhuyaowen
# @Email  : zhuyaowen@chinasofti.com

"""
import atexit
import logging
import time
import warnings
import psutil
import os
import gc

from queue import Empty
from typing import List, Union
from confluent_kafka import Consumer, Producer, Message, KafkaError, KafkaException
from .util import get_func_default_argspec
from .mapping import KAFKA_ALLOW_KWARGS

gc.set_threshold(50, 5, 5)
logger = logging.getLogger(__name__)


class KafkaHandlerBase:
    ignore_kwargs = set()

    def __init__(self, config: dict = None,
                 **kwargs
                 ):
        """

        :param config: kafka 参数vendor/librdkafka_configuration.md
                        https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
        :param kwargs: python 写法参数  bootstrap_servers   config 中写法 bootstrap.servers
        """

        self._class_type = getattr(self, '_class_type', None) or 'base'
        self._config = self.parser_config(config=config, **kwargs)
        self._kfk_cls = Producer if self._class_type == 'producer' else Consumer
        self._handler = None
        self._handler_attr = None
        self.instance()

        self._atexit_register()  # 退出时回调

    def _init(self):
        raise NotImplementedError

    def _reset_attr(self):

        for k in self._handler_attr:
            setattr(self, k, getattr(self._handler, k))

    def _atexit_register(self):
        atexit.register(self.destroy)

    @property
    def _self_default_kwages(self):
        """
        获取方法默认参数
        :return:
        """
        if hasattr(self, '_default_kwargs'):
            return getattr(self, '_default_kwargs', {})

        default_kwargs = get_func_default_argspec(self.__init__)

        if 'config' in default_kwargs:
            default_kwargs.pop('config')

        setattr(self, '_default_kwargs', default_kwargs)
        return default_kwargs

    def _pprint_config(self, config: dict):
        """
        打印所有连接参数  包括默认值
        :param config:
        :return:
        """

        logger.info('kafka connect config')
        for k, v in config.items():
            text = '{}: {}'.format(k, v)
            logger.info(text)

    def instance(self):
        """
        实例初始化 调用
        :return:
        """
        self._handler = self._kfk_cls(**self._config)
        self._handler_attr = self.generate_cls_attr(self._handler)
        self._reset_attr()

    def generate_cls_attr(self, cls):
        """
        生成 kafka Consumer Producer 可调用方法
        :param cls:
        :return:
        """
        cls_attr_set = set()
        for k in dir(cls):

            if k.startswith('__'):
                continue

            cls_attr_set.add(k)

        return cls_attr_set

    def parser_config(self, config: dict = None,
                      **kwargs):
        """
        解析配置 支持python 写法  也可以通过config 直接传入kafka 原生写法
        :param config:
        :param kwargs:
        :return:
        """

        config = config or {}

        # 根据当前默认参数 以及config 参入数据 合并生成

        # 优先级
        # input_kwargs(人工输入参数 )  》 config  》 default_kwargs(默认参数参数 )
        input_kwargs = {}
        default_kwargs = {}

        for k, v in kwargs.items():
            config_key = k.replace('_', '.')
            default_value = self._self_default_kwages.get(k)
            if k in self.ignore_kwargs:
                continue
            if k not in KAFKA_ALLOW_KWARGS:
                continue
            if v == default_value:
                # TODO 参入参数是dict 会有问题   一般也不允许
                # 传入参数跟默认值一致  优先级最低
                default_kwargs[config_key] = v

            elif v is None and k in self._self_default_kwages:
                # 人工未传入参数 且 默认参数 为 None
                # 直接忽略该参数
                continue

            else:
                input_kwargs[config_key] = v

        for k, v in self._self_default_kwages.items():
            # 存在默认值
            if k in kwargs or k in self.ignore_kwargs or v is None:
                continue

            config_key = k.replace('_', '.')
            default_kwargs[config_key] = v

        # 优先级高的 覆盖优先级低的
        default_kwargs.update(config)
        default_kwargs.update(input_kwargs)

        self._pprint_config(default_kwargs)

        return default_kwargs

    def destroy(self):
        """
        类销毁后调用
        :return:
        """
        # Producer 销毁前调用 flush  将数据投递到 broker
        # Consumer 销毁前调用 close  将连接释放   broker 会立即进入rebalance(重平衡) 下一个消费者立马可以接受消息
        # 否则需要等待  max.poll.interval.ms 设置的超时时间（默认45秒） 下个消费者才能接收到消息

        try:
            func = self.flush if self._class_type == 'producer' else self.close
            func()
        except Exception as e:
            logger.exception(e)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.destroy()

    def __del__(self):
        # KeyboardInterrupt  等强制退出时 关闭连接
        self.destroy()
        logger.debug('kafka {class_type} handler destroy'.format(class_type=self._class_type))


class KafkaConsumer(KafkaHandlerBase, Consumer):
    """
    confluent_kafka.Consumer
        Consumer(config)
        使用指定的配置dict创建Consumer实例。

        Consumer.assign(partitions)
        由指定TopicPartition列表设置Consumer的分区分配策略，启动消费。如果对关闭的Consumer调用本函数会抛出RuntimeError。

        Consumer.assignment()
        返回当前分区分配策略，返回list(TopicPartition)

        Consumer.close()
        关闭和终止Consumer实例，关闭Consumer实例会执行以下操作：停止消费；提交位移（如果enable.auto.commit设置为False会抛出异常）、离开Consumer Group。

        Consumer.commit([message=None][,offsets=None][,asynchronous=True])
        提交一条消息或位移列表，message和offsets是互斥参数，如果没有指定参数，会使用当前分区分配策略的offsets。

        message：提交消息的位移加1

        offsets：要提交的TopicPartition列表

        asynchronous：是否异步提交。异步提交会立即返回None。如果设置为False，会阻塞直到提交成功或失败，如果提交成功，会返回提交的offsets。注意：提交成功，需要对返回的TopicPartition列表的每个TopicPartition的err字段进行检查，TopicPartition可能会提交失败。

        Consumer.committed(partitions[,timeout=None])
        获取已提交的分区的offsets。

        partitions：TopicPartition列表

        timeout：请求超时，单位秒。
        返回TopicPartition列表或错误集

        Consumer.consume([num_messages=1][,timeout=-1])
        消费消息，调用回调函数，返回消息列表，如果超时，返回空。
        应用程序必须检查返回Message的error方法，正常Message的error返回None。

        num_messages：返回的最大消息数量，默认为1

        timeout：阻塞等待消息、事件、回调函数的最大时间

        Connsumer.get_watermark_offsets(partition[,timeout=None][,cached=False])
        获取分区的低水位和高水位

        partition：TopicPartition对象

        Timeout：请求超时，

        Cached：是否替换正在查询的Broker使用的缓存信息。
        成功返回低水位和高水位的元组，超时返回None。

        Consumer.list_topics([topic=None][,timeout=-1])
        请求集群的元数据信息。

        topic：字符串类，如果指定，只请求本Topic的信息，否则返回集群的所有Topic。

        timeout：超时前的最大响应时间，-1表示永不超时。
        返回ClusterMetadata类型

        Consumer.offsets_for_times(partitions[,timeout=None])
        对指定的分区列表根据时间戳查询offsets。
        返回每个分区的offsets大于等于指定分区列表的时间戳的位移。

        partitions：TopicPartition列表

        timeout：请求超时时间。

        Consumer.pause(partitions)
        暂停指定分区列表的分区的消费

        Consumer.poll([timeout=None])
        消费消息，调用回调函数，返回事件。
        应用程序必须检查返回的Message对象的error()方法，如果是正常消息，返回None。
        返回Message对象回None。

        Consumer.position(partitions)
        获取指定分区列表分区的位移

        partitions：分区列表
        返回带位移的TopicPartition列表，当前位移是最新消费消息的位移加1。

        Consumer.resume(partitions)
        恢复指定分区列表的分区的消费

        partitions：要恢复的TopicPartitio列表

        Consumer.seek(partition)
        定位分区的消费位移到offset。offset可以是绝对值，也可以是逻辑位移OFFSET_BEGINNING。本函数只用于活跃消费分区更新消费位移，要设置分区的起始位移可以使用assign函数。

        Consumer.store_offsets([message=None][,offsets=None])
        存储一条消息的位移或位移列表。

        message和offsets是互斥参数。
        被存储的位移会根据auto.commit.interval.m参数值被提交，使用本函数时enable.auto.offset.store参数必须被设置为False。

        message：存储message的位移加1。

        offsets：要存储位移的TopicPartition列表

        Consumer.subscribe(topics[,on_assign=None][,on_revoke=None])
        设置要订阅的Topic列表，会替代此前订阅的Topic。
        订阅的Topic名称支持正则表达式，使用”^”作为Topic名称前缀。

        topics：Topic名称列表

        on_assign：完成分区再分配的回调函数

        on_revoke：再平衡操作的

        on_assign(consumer, partitions)

        on_revoke(consumer, partitions)
            1.on_assign(consumer, partitions)
            2.on_revoke(consumer, partitions)

        Consumer.unassign()
        删除当前分区分配策略和停止消费

        Consumer.unsubscribe()
        删除当前订阅Topic


    """

    def __init__(self, bootstrap_servers=None,
                 group_id=None,
                 topic=None,
                 group_instance_id=None,
                 auto_offset_reset='earliest',
                 max_poll_interval_ms=5 * 60 * 1000,
                 session_timeout_ms=1 * 60 * 1000,
                 auto_commit_enable=False,
                 enable_auto_offset_store=False,
                 fetch_message_max_bytes=1 * 1024 * 1024,
                 fetch_max_bytes=100 * 1024 * 1024,
                 # socket_receive_buffer_bytes=10 * 1024 * 1024,
                 queued_max_messages_kbytes=10 * 1024,
                 config: dict = None,
                 callback_auto_commit=False,
                 callback=None,
                 **kwargs
                 ):
        """

        :param bootstrap_servers: kafka 连接串 必填

        :param group_id: 分组名称 必填

        :param group_instance_id: 启用静态组成员身份。静态组成员可以在配置的 session.timeout.ms 内离开和重新加入组，而不会提示组重新平衡。这应该与更大的 session.timeout.ms 结合使用，以避免由暂时不可用（例如进程重新启动）引起的组重新平衡。需要代理版本 >= 2.3.0

        :param auto_offset_reset:  当前默认 earliest
                                    earliest 当各分区下有已提交的offset时，从提交的offset开始消费；无提交的offset时，从头开始消费
                                    latest 当各分区下有已提交的offset时，从提交的offset开始消费；无提交的offset时，消费新产生的该分区下的数据
                                    none topic各分区都存在已提交的offset时，从offset后开始消费；只要有一个分区不存在已提交的offset，则抛出异常

        :param max_poll_interval_ms:  默认 5 * 60 * 1000  5分钟
                                    高级消费者的消费消息调用之间的最大允许时间
                                    （例如，rd_kafka_consumer_poll()）。
                                    如果超过此时间间隔，则认为消费者失败，组将重新平衡，以便将分区重新分配给另一个消费者组成员。
                                    警告：此时可能无法进行偏移提交。
                                    注意：建议为长时间处理的应用程序设置 enable.auto.offset.store=false ，
                                    然后在消息处理后显式存储偏移量（使用 offsets_store()），
                                    以确保在处理有偏移量之前不会自动提交偏移量完成的。
                                    该间隔每秒检查两次。有关更多信息，请参阅 KIP-62。

        :param session_timeout_ms:  默认 1 * 60 * 1000  1分钟
                                    客户端组会话和故障检测超时。消费者定期发送心跳 (heartbeat.interval.ms) 以向代理表明其活跃度。
                                    如果代理在会话超时内没有收到组成员的红心，代理将从组中删除消费者并触发重新平衡。
                                    允许范围使用代理配置属性
                                    group.min.session.timeout.ms 和 group.max.session.timeout.ms 进行配置。
                                    另请参阅 max.poll.interval.ms。
        :param auto_commit_enable: 默认 false   关闭手动位移提交
                                    在后台自动和定期提交偏移量。注意：将此设置为 false 不会阻止消费者获取先前提交的起始偏移量。
                                    为了避免这种行为，在调用assign() 时为每个分区设置特定的起始偏移量。

        :param enable_auto_offset_store: 默认 true   自动存储提供给应用程序的最后一条消息的偏移量。
                                                    偏移存储是每个分区（自动）提交的下一个偏移的
        :param fetch_message_max_bytes:  获取最大消息大小  默认 1 * 1024 * 1024 = 1M
                                        从代理获取消息时，每个主题+分区需要请求的初始最大字节数。如果客户端遇到大于该值的消息，它将逐渐尝试增加该值，直到获取整个消息。
        :param fetch_max_bytes:  获取最大消息大小  默认 100 * 1024 * 1024 = 100M
                                        从代理获取消息时，每个主题+分区需要请求的初始最大字节数。如果客户端遇到大于该值的消息，它将逐渐尝试增加该值，直到获取整个消息。
        :param socket_receive_buffer_bytes:  网络请求Socket接受Buffer大小
        :param queued_max_messages_kbytes:   预加载 大小
        :param config:

        :param kwargs:
        """
        self.ignore_kwargs.add('topic')
        self.ignore_kwargs.add('callback_auto_commit')
        self.ignore_kwargs.add('callback')

        self._class_type = 'consumer'
        self._topic = topic
        self._callback_auto_commit = callback_auto_commit  # 回调函数结束后自动提交默认 false
        self._callbacks = []
        kwargs['bootstrap_servers'] = bootstrap_servers
        kwargs['group_id'] = group_id
        kwargs['group_instance_id'] = group_instance_id
        kwargs['auto_offset_reset'] = auto_offset_reset
        kwargs['max_poll_interval_ms'] = max_poll_interval_ms
        kwargs['session_timeout_ms'] = session_timeout_ms
        kwargs['auto_commit_enable'] = auto_commit_enable
        kwargs['enable_auto_offset_store'] = enable_auto_offset_store
        kwargs['fetch_message_max_bytes'] = fetch_message_max_bytes
        kwargs['fetch_max_bytes'] = fetch_max_bytes
        # kwargs['socket_receive_buffer_bytes'] = socket_receive_buffer_bytes
        kwargs['queued_max_messages_kbytes'] = queued_max_messages_kbytes
        super().__init__(
            config=config,
            **kwargs)

        if callback:
            self.register_callback(callback)

    def check_auto_commit_enable(self):
        if self._config['auto.commit.enable']:
            # 打开了自动提交 抛warning
            warnings.warn('auto.commit.enable=True 当前打开了自动提交位移存在丢数据风险 请关闭！')
        else:
            logger.info('auto.commit.enable=False 当前开启手动提交  '
                        '请手动调用 consumer.commit(msg) 或设置 callback_auto_commit=True')

    def get_msg_partitions(self, msgs: Union[Message, List[Message]]):
        partitions = set()
        msgs = msgs if isinstance(msgs, list) else [msgs, ]

        for msg in msgs:
            partition = msg.partition()
            partitions.add(partition)

        return list(partitions)

    def get_latest_offset(self, msgs: Union[Message, List[Message]]) -> dict:
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

    def consumer_callback_start(self, msgs: Union[Message, List[Message]]):
        return msgs

    def consumer_callback_end(self, msgs: Union[Message, List[Message]]):
        return msgs

    def consumer_msgs_filter(self, msgs: Union[Message, List[Message]]):
        return msgs

    def message_callback(self, consumer, msgs: Union[Message, List[Message]]):
        """外部重构"""
        raise NotImplemented

    def consumer_callback(self, msgs: Union[Message, List[Message]]):
        """

        :param msg: Message or [Message]
        :return:
        """

        try:
            # TODO filter, 过滤DDL发送到特定topic
            msgs = self.consumer_msgs_filter(msgs)

            for callback in self._callbacks:
                self.consumer_callback_start(msgs)

                r = callback(self, msgs)  # TODO 处理结果 RPC等

                self.consumer_callback_end(msgs)

            if self._callback_auto_commit:
                # 回调结束后自动提交
                # partitions = self.get_msg_partitions(msgs)
                # self.committed(partitions)
                for m in self.get_latest_offset(msgs).values():
                    self.commit(m, asynchronous=False)
        except (KafkaError, KafkaException) as e:
            # 断连接 抛出异常重连
            # TODO 异常处理
            logger.error(e)
            raise e

    def register_callback(self, callback):
        """Register a new callback to be called when a message is received.

        Note:
            The signature of the callback needs to accept two arguments:
            `(body, message)`, which is the decoded message body
            and the :class:`~confluent_kafka.Message` instance.
        """
        if callback and callback not in self._callbacks:
            self._callbacks.append(callback)

    def start_subscribe(self):
        if self._topic:
            topics = [self._topic, ] if isinstance(self._topic, str) else self._topic
            self.subscribe(topics=topics)

    def start(self, callback=None,
              batch=True,
              batch_size=None,
              num_messages=None,
              callback_auto_commit=None,
              timeout=1,
              wait=False):
        """
        阻塞获取消息  如果成功获取到消息 调用注册的回调函数
        :param callback: 回调函数
        :param batch: 是否批量获取
        :param batch_size: 批量获取大小
        :param num_messages: 批量获取大小  batch_size 别名
        :param callback_auto_commit: 回调之后自动提交
        :param timeout: 超时
        :param wait: 是否等待  当wait=True
                        如果topic 中数据不足batch_size
                        则会等待 指定timeout 时间返回

        """
        # 主动拉取服务器数据 直到返回数据为空
        logger.info("Kafka Consuming start.")
        if callback:
            self.register_callback(callback)
        if not self._callbacks:
            self.register_callback(self.message_callback)  # 内部回调 可重新继承
        assert self._callbacks, '未设置回调函数'
        self.check_auto_commit_enable()

        batch_size = batch_size or num_messages or 100
        logger.info('batch_size: %s', batch_size)
        if callback_auto_commit is not None:
            self._callback_auto_commit = callback_auto_commit

        self.start_subscribe()  # 开始订阅主题
        empty_num = 0  # 超过10次获取不到消息 自动重启
        err_print_timed = time.time()
        empty_timed = time.time()
        while True:
            try:
                if batch:
                    messages = self.get_batch(block=True, timeout=timeout, batch_size=batch_size, wait=wait)
                else:
                    messages = self.get(timeout=timeout)

                empty_num = 0
                empty_timed = time.time()

                self.consumer_callback(messages)  # 调用回调函数
                del messages
            except Empty:
                empty_num += 1
                now = time.time()
                time.sleep(0.1)
                if now - empty_timed >= 60 * 1:
                    empty_num = 0
                    logger.info('当前进程的内存使用：%.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
                    logger.info('%s 连续1分钟未获取到消息', self.__class__)
                    empty_timed = time.time()
                continue

            except KafkaError as e:

                if e.code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                    # 主题不存在 等待1分钟
                    time.sleep(1)
                    if time.time() - err_print_timed > 60:
                        err_print_timed = time.time()
                        logger.info("主题不存在 等待1分钟")
                        logger.error(e)  # 降低报错频率
                        continue

                logger.error(e)
                time.sleep(3)
                continue
            except Exception as e:
                # logger.exception(e)
                raise e

            time.sleep(0)

    def get(self, block=True, timeout=None) -> Message:
        """
        底层调用 poll  获取单条消息
        :param block: 是否阻塞 非阻塞如果获取不到消息直接返回
        :param timeout: 获取消息超时时间 如果 block=False timeout 不生效

        :return:  <message>
        """
        remaining = timeout

        if not block:
            # 非阻塞  timeout= 0
            remaining = 0
        message = self.poll(timeout=remaining)
        if message and message.error() is not None:
            raise message.error()
        return message

    def get_batch(self, block=True, timeout=None, batch_size=None, wait=False, num_messages=100) -> List[Message]:
        """
        批量获取消息
        :param block: 是否阻塞 非阻塞如果获取不到消息直接返回   如果批量获取100条消息 但是topic中只有50条 会一值等待直到超时
        :param timeout: 获取消息超时时间 如果 block=False timeout 不生效
        :param batch_size: 每次获取消息条数
        :param wait: 是否等待 block 阻塞模式   当batch_size=100  但是topic中只有50条消息时
                     wait=False   会直接返回50条 wait=True 会等待直到超时才返回50条
        :param num_messages: 每次获取消息条数 兼容kafka 默认参数
        :return: list [<message>, <message>]
        """

        batch_size = num = batch_size or num_messages
        timeout: float = -1 if timeout is None else timeout
        remaining = timeout
        time_start = time.time()

        if not block:
            # 非阻塞  timeout= 0
            remaining = 0.000001
        if not wait:
            # 非等待模式 先将超时时间设置为0 如果返回指定数量数据则直接返回
            # 如果返回 None 则先判断是否为阻塞模式 如果阻塞模式则将batch_size 调整为1 等待
            # 一旦获取到数据则立即进行二次数据获取 合并后立即返回
            remaining = 0.000001

        results = []
        is_first = True
        # 第一次启动很有可能由于连接问题 获取不到消息  导致只拿到一条消息就返回
        # 解决办法 判断是否是第一次消费 第一次消费则获取多次
        while True:
            messages = self.consume(num_messages=num, timeout=remaining)
            if messages:

                # 异常检测
                err = messages[0].error()
                if err is not None:
                    # KafkaError ValueError
                    raise err

                # 结果处理
                results.extend(messages)
                len_msg = len(results)
                if len_msg >= batch_size or not block:
                    # 非等待模式 如果返回数量跟理想一致 直接返回

                    # 或 非阻塞模式
                    break
                if not wait and not is_first:
                    #  返回数量不够 且 不等待
                    # 非第一次启动
                    break

                # 返回数量不足 且为阻塞模式 且需要返回指定数量数据
                # 重新调整条数及超时时间
                is_first = False
                remaining = timeout if timeout == -1 else timeout - (time.time() - time_start)
                if timeout >= 0 and remaining <= 0:
                    # 超时 返回
                    break

                # 消息数不够继续获取消息
                remaining = 0.01  # 获取剩下消息 超时 0.01 s
                num = batch_size - len(results)
                if num <= 0:
                    break
                # 重新获取消息
                continue

            # messages is None
            # 未获取到消息

            if not block:
                # 非阻塞模式 直接返回
                break

            # 阻塞模式
            # 消息数量一定不够 需要等待消息足够才返回

            remaining = timeout if timeout == -1 else timeout - (time.time() - time_start)
            if timeout >= 0 and remaining <= 0:
                break

            if wait:

                num = batch_size - len(results)
                if num <= 0:
                    break
            else:
                # not wait 非等待状态
                # 先将batch_size 调整为1  尝试获取消息 (否则可能会因为消息数 不够卡住)
                num = 1

        if not results:
            raise Empty
        logger.debug('批量获取消息成功  当前获取到：%s条', len(results))
        return results


class KafkaProducer(KafkaHandlerBase, Producer):
    # 全局实例化一次即可

    """

    confluent_kafka.Producer 是异步Kafka生产者。
        Producer.Producer(config)
            使用config字典创建Producer实例。

        config：配置字典对象，至少应该设置bootstrap.servers属性

        Producer.len()
            返回要传递到Broker的消息数量

        Producer.flush([timeout])
            等待Producer队列中要传递的所有消息。

        timeout：阻塞的最大时间，要求librdkafka版本大于0.9.4。
            返回Producer消息队列中仍然存在的消息的数量。

        Producer.list_topics([topic=None][, timeout=-1])
            请求集群的元数据。

        topic：如果指定Topic，只返回Topic的相应元数据，否则返回所有Topic的元数据。

        timeout：超时前的最大响应时间，-1表示永不超时。
            返回ClusterMetadata类型。

        Producer.poll([timeout])

        Poll生产者事件，调用相应回调函数。

        timeout：阻塞等待事件的最大时间。
            返回处理事件的数量。

        Producer.produce(topic[, value][, key][, partition][, on_delivery][, timestamp][, headers])
            生产消息到指定Topic，异步操作。


        topic：要生产消息到的指定Topic。

        value：str或bytes类型，消息数据。

        key：str或bytes类型，消息Key。

        partition：要生产消息到指定分区，否则使用内置分区分配策略。

        on_delivery：投递报告回调函数

        timestamp：消息事件戳，要求librdkafka v0.9.4以上版本，api.version.request=true, Kafka 0.10.0.0以上版本。

        headers：消息头，字典类型，消息头的key必须是字符串，value必须是二进制数据，unicode或None。要求librdkafka v0.11.4以上版本和Kafka 0.11.0.0以上版本。

    """

    def __init__(self, bootstrap_servers=None,
                 topic=None,
                 compression_type='lz4',
                 message_max_bytes=1024 * 1024 * 100,
                 message_send_max_retries=2147483647,
                 queue_buffering_max_messages = 100000,
                 # socket_send_buffer_bytes=10 * 1024 * 1024,
                 enable_idempotence=False,
                 retry_backoff_ms=100,
                 linger_ms=5,
                 max_in_flight=5,
                 acks=-1,
                 config: dict = None,
                 **kwargs
                 ):
        """

        :param bootstrap_servers: kafka 连接串
        :param topic: 主题名 可以不写
        :param compression_type: 数据压缩类型 支持 none, gzip, snappy, lz4, zstd   当前默认lz4
        :param message_max_bytes: 单条消息大下 需要同时设置 kafka broker 才能生效 当前默认100M
        :param message_send_max_retries: 消息发送重试次数  重试可能会导致消息乱序  如果发送消息有顺序要求
                                            enable.idempotence 必须设置为True
        :param queue_buffering_max_messages: 本地缓存最大缓存消息数
        :param enable_idempotence: 是否开启幂等性功能
                                当设置为 true 时，生产者将确保消息只按原始生产顺序成功生产一次。
                                启用幂等性时会自动调整以下配置属性（如果用户未修改）
                                max.in.flight.requests.per.connection=5（必须小于等于5）
                                retries=INT32_MAX（必须是大于 0)，acks=all，queuing.strategy=fifo。
                                如果用户提供的配置不兼容，生产者实例化将失败

        :param retry_backoff_ms: 用来设定两次重试之间的时间间隔，默认值100。

        :param linger_ms: 消息逗留时间 在构建消息批次 (MessageSets)
                                以传输到代理之前等待生产者队列中的消息累积的延迟（以毫秒为单位）。
                                生产者客户端会在ProducerBatch被填满或者等待时间超过linger.ms时发送出去。
                                增大这个参数的值会增加消息的延迟，但同时会提高吞吐量
        :param socket_send_buffer_bytes: 消息发送缓存大小默认 10M
        :param max_in_flight: max.in.flight.requests.per.connection 的别名：
                                发送多少条消息后,接收服务端确认,
                                比如设置为1,就是每发一条就要确认一条,设置为5就是,发送5条消息等待一次确认 ,
                                如果大于1,比如5,这种情况下是会有一个顺序问题的,就是这5条消息其中的一条发送失败了,
                                如果进行重试,那么重发的消息其实是在下个批次的,这就会造成消息顺序的错乱,
                                所以如果需要保证消息的顺序,建议设置此参数为1 Default: 5.

                                每个代理连接的最大动态请求数。
                                这是适用于所有代理通信的通用属性，但它主要与生成请求相关。
                                特别要注意的是，其他机制将每个代理的未完成消费者提取请求的数量限制为一个。
                                发送多少条消息后,接收服务端确认,比如设置为1,就是每发一条就要确认一条,设置为5就是,发送5条消息等待一次确认 ,如果大于1,比如5,这种情况下是会有一个顺序问题的,就是这5条消息其中的一条发送失败了,如果进行重试,那么重发的消息其实是在下个批次的,这就会造成消息顺序的错乱,所以如果需要保证消息的顺序,建议设置此参数为1 Default: 5.

        :param acks: request.required.acks 的别名
                                用来指定必须要多少个副本收到这条消息，之后生产者才会认为这条消息成功写入。
                                acks是生产者客户端中一个非常重要的参数，它涉及消息的可靠性和吞吐量之间的权衡。
                                acks参数有三种类型的值：字符串类型， 整型。
                                1：只要分区的leader副本写入成功，生产者就会收到来自服务端的成功响应。
                                    如果再被其它follower副本拉取前leader副本崩溃，那么此时消息还是会丢失。
                                0：生产者发送消息之后不需要等待任何服务端的响应。
                                    如果在消息发送到写入kafka的过程中出现了某些异常，导致kafka并没有收到这条消息，
                                    那么生产者也无从得知，消息会丢失。
                                -1或者all：生产者发送消息之后，需要等待ISR中所有副本成功写入消息之后才能收到来自服务端的成功响应。

        :param config:
        :param kwargs:
        """

        self._class_type = 'producer'
        self._producer_interval = 0.0  # 插入时间间隔
        self._topic = topic
        self.ignore_kwargs.add('topic')

        kwargs['compression_type'] = compression_type
        kwargs['message_max_bytes'] = message_max_bytes
        kwargs['message_send_max_retries'] = message_send_max_retries
        kwargs['queue_buffering_max_messages'] = queue_buffering_max_messages
        # kwargs['socket_send_buffer_bytes'] = socket_send_buffer_bytes
        kwargs['enable_idempotence'] = enable_idempotence
        kwargs['retry_backoff_ms'] = retry_backoff_ms
        kwargs['linger_ms'] = linger_ms
        kwargs['max_in_flight'] = max_in_flight
        kwargs['acks'] = acks

        super().__init__(bootstrap_servers=bootstrap_servers,
                         config=config,
                         **kwargs)

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            # TODO 投递异常消息处理  高可用场景下需要做兜底处理
            logger.error('Message delivery failed: {}'.format(err))
        else:

            logger.debug('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def produce_loop(self, topic, value=None, *args, **kwargs):
        """
        循环插入 遇到BufferError 等待指定时间间隔重试 0.1 0.2 0.4 0.8 s 递增 最长等待 5S
        """
        while True:
            try:
                self.produce(topic, value=value, *args, **kwargs)
                self._producer_interval = 0.0
                break
            except BufferError as e:
                logger.error(e)
                interval = self._producer_interval or 0.05
                interval = interval * 2
                self._producer_interval = interval if interval <= 5 else 5.0
                self.poll(0)
                time.sleep(self._producer_interval)
                continue

    def publish(self, topic=None, value=None, batch=None, auto_poll=True, auto_flush=False, *args, **kwargs):

        """

        底层调用 produce  增加批量插入功能  batch=True  且 value 类型为 list 会尝试分开插入

        .. py:function:: produce(topic, [value], [key], [partition], [on_delivery], [timestamp], [headers])

          Produce message to topic.
          This is an asynchronous operation, an application may use the ``callback`` (alias ``on_delivery``) argument to pass a function (or lambda) that will be called from :py:func:`poll()` when the message has been successfully delivered or permanently fails delivery.

          Currently message headers are not supported on the message returned to the callback. The ``msg.headers()`` will return None even if the original message had headers set.

          :param str topic: Topic to produce message to
          :param str|bytes value: Message payload   消息体
          :param bool batch: batch Message  开启批量插入 传入的数据 value 格式必须为 List[<message>, ]
          :param bool auto_poll: 提交消息前先调用轮训事件  会调用callback 函数  官方样例写法 默认打开
          :param bool auto_flush: 每次提交完成后 自动刷盘  数据高可用场景下开启
          :param str|bytes key: Message key
          :param int partition: Partition to produce to, else uses the configured built-in partitioner.
          :param func on_delivery(err,msg): Delivery report callback to call (from :py:func:`poll()` or :py:func:`flush()`) on successful or failed delivery
          :param int timestamp: Message timestamp (CreateTime) in milliseconds since epoch UTC (requires librdkafka >= v0.9.4, api.version.request=true, and broker >= 0.10.0.0). Default value is current time.

          :param headers dict|list: Message headers to set on the message. The header key must be a string while the value must be binary, unicode or None. Accepts a list of (key,value) or a dict. (Requires librdkafka >= v0.11.4 and broker version >= 0.11.0.0)
          :rtype: None
          :raises BufferError: if the internal producer message queue is full (``queue.buffering.max.messages`` exceeded)
          :raises KafkaException: for other errors, see exception code
          :raises NotImplementedError: if timestamp is specified without underlying library support.
        """

        if 'callback' not in kwargs:
            kwargs['callback'] = self.delivery_report

        values = value if batch else [value, ]  # 批量投递
        topic = topic or self._topic
        assert topic

        if auto_poll:
            self.poll(0)
        for value in values:
            self.produce_loop(topic, value=value, *args, **kwargs)

        if auto_flush:
            # 批量插入推荐使用
            self.flush()
