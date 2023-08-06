import logging
import math
from typing import Type, Any
from concurrent.futures import TimeoutError as PubsubTimeoutError
from asyncio.exceptions import TimeoutError as AsyncTimeoutError

import base64
from datetime import datetime
import asyncio
import queue
from functools import partial
import google.auth
from google.cloud import pubsub
from xia_fields import ByteField, IntField, TimestampField
from xia_engine import Document
from xia_logger import HttpLogger, DataLog


class PubsubLogger(HttpLogger):
    engine_param = "pubsub_logging"
    engine_connector = pubsub.PublisherClient
    streaming_client: pubsub.SubscriberClient = None
    streaming_pull_future = None

    @classmethod
    def get_subscriber(cls):
        if cls.streaming_client is None:
            cls.streaming_client = pubsub.SubscriberClient()
        elif cls.streaming_pull_future is not None and not cls.streaming_pull_future.running():
            cls.streaming_client = pubsub.SubscriberClient()  # Client closed so we create a new Client
        return cls.streaming_client

    @classmethod
    def _get_streaming_params(cls, **kwargs) -> dict:
        params = {
            "project_id": kwargs.get("project_id", google.auth.default()[1]),
            "topic_id": kwargs["topic_id"],
            "ack_timestamp": kwargs.get("ack_timestamp", None),
            "timeout": kwargs.get("timeout", None)
        }
        return params

    @classmethod
    def custom_callback_sync(cls, message, ack_timestamp: float, callback):
        """The callback function will receive the document object one by one

        Args:
            message: pubsub message
            ack_timestamp: All data with insert time before this timestamp will be ack. None = ack nothing
            callback: callback function (synchronous mode)
        """
        db_content = dict(message.attributes)
        db_content["data_content"] = message.data
        data_log = DataLog.from_db(_engine=cls, **db_content)
        if ack_timestamp and data_log.insert_timestamp < ack_timestamp:
            message.ack()  # Old data, ignore and ack them
            return
        try:
            for parsed_doc in PubsubLogger.parse_log(data_log):
                callback(parsed_doc[1], parsed_doc[0].operation_type, parsed_doc[0].create_seq)
            message.ack()  # All data sent, could ack the message
        except TypeError as e:
            logging.error(str(e))

    @classmethod
    def custom_callback_async(cls, message, ack_timestamp: float, callback):
        """The callback function will receive the document object one by one

        Args:
            message: pubsub message
            ack_timestamp: All data with insert time before this timestamp will be ack. None = ack nothing
            callback: callback function (synchronous mode)
        """
        db_content = dict(message.attributes)
        db_content["data_content"] = message.data
        data_log = DataLog.from_db(_engine=cls, **db_content)
        if ack_timestamp and data_log.insert_timestamp < ack_timestamp:
            message.ack()  # Old data, ignore and ack them
            return
        try:
            for parsed_doc in PubsubLogger.parse_log(data_log):
                callback(parsed_doc[1], parsed_doc[0].operation_type, parsed_doc[0].create_seq)
            message.ack()  # All data sent, could ack the message
        except TypeError as e:
            logging.error(str(e))

    @classmethod
    def streaming(cls, callback: Any, **kwargs):
        """Streaming data (callback is called in child thread)

        Args:
            callback: The synchronous call back function takes three parameters:
                * doc: Document
                * op: Operation Type
                * seq: Create Sequence
            **kwargs: could contain the following information:
                * project_id: Pubsub project id, default value is defined by credential json
                * topic_id: Pubsub topic id
                * ack_timestamp: All data with insert time before this timestamp will be ack. None = ack nothing
                * timeout: Pulling for how much time. None = forever
        """
        if asyncio.iscoroutinefunction(callback):
            raise TypeError("Callback of streaming shouldn't be async, using streaming_async instead")

        subscriber = cls.get_subscriber()
        params = cls._get_streaming_params(**kwargs)
        subscription_path = subscriber.subscription_path(params["project_id"], params["topic_id"])
        custom_callback = partial(cls.custom_callback_sync, ack_timestamp=params["ack_timestamp"], callback=callback)
        cls.streaming_pull_future = subscriber.subscribe(subscription_path, callback=custom_callback)
        with subscriber:
            try:
                cls.streaming_pull_future.result(timeout=params["timeout"])
            except PubsubTimeoutError:
                cls.streaming_pull_future.cancel()
                cls.streaming_pull_future.result()

    @classmethod
    async def streaming_async(cls, callback, **kwargs):
        """Streaming data (callback is called in child thread)

        Args:
            callback: The asynchronous call back function takes three parameters:
                * doc: Document
                * op: Operation Type
                * seq: Create Sequence
            **kwargs: could contain the following information:
                * project_id: Pubsub project id, default value is defined by credential json
                * topic_id: Pubsub topic id
                * ack_timestamp: All data with insert time before this timestamp will be ack. None = ack nothing
                * timeout: Pulling for how much time. None = forever
        """
        if not asyncio.iscoroutinefunction(callback):
            raise TypeError("Callback of streaming_async must be an async function")

        subscriber = cls.get_subscriber()
        params = cls._get_streaming_params(**kwargs)
        subscription_path = subscriber.subscription_path(params["project_id"], params["topic_id"])

        message_queue = queue.Queue()

        def async_callback(message, ack_timestamp: float):
            db_content = dict(message.attributes)
            db_content["data_content"] = message.data
            data_log = DataLog.from_db(_engine=cls, **db_content)
            if ack_timestamp and data_log.insert_timestamp < ack_timestamp:
                message.ack()  # Old data, ignore and ack them
                return
            try:
                for parsed_doc in PubsubLogger.parse_log(data_log):
                    message_queue.put(parsed_doc)
            except TypeError as e:
                logging.error(str(e))

        custom_callback = partial(async_callback, ack_timestamp=params["ack_timestamp"])
        cls.streaming_pull_future = subscriber.subscribe(subscription_path, callback=custom_callback)

        get_message_func = partial(message_queue.get, timeout=1)
        time_count = params["timeout"] if params["timeout"] else math.inf
        while True:
            try:
                time_count = time_count - 1
                header, document = await asyncio.get_event_loop().run_in_executor(None, get_message_func)
                asyncio.create_task(callback(document, header.operation_type, header.create_seq))
            except queue.Empty:
                if time_count < 0:
                    cls.streaming_pull_future.cancel()
                    cls.streaming_pull_future.result()
                    break
                else:
                    pass  # Waiting one more second

    @classmethod
    def create(cls, document_class: Type[Document], db_content: dict, doc_id: str = None):
        publisher: pubsub.PublisherClient = cls.get_connection()
        project_id = google.auth.default()[1]
        if "/" in db_content["logger_name"]:
            topic_path = db_content["logger_name"]
        else:
            topic_id = db_content["logger_name"]
            topic_path = publisher.topic_path(project_id, topic_id)
        data_content = db_content.pop("data_content", b"")
        future = publisher.publish(topic_path, data_content, **db_content)
        message_no = future.result(60)
        return message_no if not doc_id else doc_id

    @classmethod
    def db_content_from_message(cls, attributes: dict, data: bytes):
        db_content = dict(attributes).copy()
        db_content["data_content"] = data
        return db_content
