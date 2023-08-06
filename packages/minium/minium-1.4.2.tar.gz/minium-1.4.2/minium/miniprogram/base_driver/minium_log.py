#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
Author:         lockerzhang
Filename:       minium_log.py
Create time:    2019-08-29 11:12
Description:

"""

from functools import wraps
import datetime
import types
import json
import requests
import queue
import threading
import logging
import os
import time
import traceback
from .version import build_version
from ...framework.exception import MiniError

logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger("minium").getChild("datareport")

REPORT_DOMAIN = "minitest.weixin.qq.com"
REPORT_PATH = "xbeacon/user_report"
app_id = None
version = build_version().get("version")
revision = build_version().get("revision")
__DEV = os.environ.get("MINIUM_DEV", None)
class ReportData(dict):
    cmd = ""

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, ReportData):
            return self.dumps() == __value.dumps()
        return super().__eq__(__value)

    def dumps(self):
        return json.dumps(self)

class ExceptionData(ReportData):
    def __init__(self, err: Exception, **kwargs):
        kwargs["from"] = "minium"
        self.TimeStamp = getattr(err, "timestamp", None) or time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.error = err.__class__.__name__
        self.err_msg = getattr(err, "msg", None) or str(err)
        self.Uin = 0
        self.version = version
        self.revision = revision
        self.ext = ""
        self.app_id = app_id
        self.msg_id = getattr(err, "msg_id", "")
        self.__dict__.update(kwargs)
        super().__init__(self.__dict__)
        self.cmd = "cloud_exception_log"


class ConsumeData(ReportData):
    def __init__(self, __map: dict, **kwargs):
        self.version = version
        self.revision = revision
        self.app_id = app_id
        self.time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        __map.update(kwargs)
        self.__dict__.update(__map)
        super().__init__(self.__dict__)
        self.cmd = "api_log"

def process_report():
    global existFlag
    while not existFlag:
        lock.acquire()
        lock.wait(10)
        lock.release()
        while not report_queue.empty():
            data = report_queue.get()
            # logger.debug("Thread processing report data %s" % data)
            report(data=data)


def report_fail(failed=True):
    global fail, existFlag
    if failed:
        fail += 1
        if fail >= 10:
            existFlag = 1
    else:
        fail = 0


def report_exception(data: ExceptionData):
    if not data.app_id:
        return
    report_queue.put(data)
    lock.acquire()
    lock.notify()
    lock.release()


def report(data: ReportData):
    """
    report minium_new
    """
    if existFlag:
        return
    # print(f"https://{REPORT_DOMAIN}/{REPORT_PATH}/{data.cmd}")
    # print(data)
    if __DEV:
        logger.debug(f"https://{REPORT_DOMAIN}/{REPORT_PATH}/{data.cmd}")
        logger.debug(data.dumps())
    try:
        ret = requests.post(
            url=f"https://{REPORT_DOMAIN}/{REPORT_PATH}/{data.cmd}",
            data=data.dumps(),
            timeout=10,
        )
        if __DEV:
            logger.debug(ret.text)
        report_fail(ret.status_code != 200)
    except Exception as e:
        # logger.debug("data report fail with https")
        try:
            ret = requests.post(
                url=f"http://{REPORT_DOMAIN}/{REPORT_PATH}/{data.cmd}",
                data=data.dumps(),
                timeout=10,
            )
            if __DEV:
                logger.debug(ret.text)
            report_fail(ret.status_code != 200)
        except Exception as e:
            # logger.error("data report fail with http, give up")
            if __DEV:
                logger.exception(e)


# logger.debug(ret.text)


existFlag = 0
fail = 0

lock = threading.Condition()
report_queue = queue.Queue()
thread = threading.Thread(target=process_report)
thread.setDaemon(True)
thread.start()

usage = []

REPORT_THRESHOLD = 10000  # 上报阈值

def minium_log(func):
    """
    函数统计装饰器
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        global usage, app_id

        start = datetime.datetime.now()
        self = args[0]
        func_name = f"{self.__class__.__name__}.{func.__name__}"
        try:
            result = func(*args, **kwargs)
        except MiniError as me:
            report_exception(ExceptionData(me, func=func_name))
            raise
        end = datetime.datetime.now()
        consuming = int((end - start).total_seconds() * 1000)
        if app_id is None and hasattr(self, "app_id"):
            app_id = self.app_id
        if consuming < REPORT_THRESHOLD:
            return result
        new_args = list(args[1:])
        
        consum_data = ConsumeData({
            "func": func_name,
            "args": str(new_args),
            "kwargs": kwargs,
            "consuming": consuming
        })

        if app_id is None:
            usage.append(consum_data)
        else:
            report_queue.put(consum_data)
            for f in usage:
                f["app_id"] = app_id
                report_queue.put(f)
            usage.clear()
            lock.acquire()
            lock.notify()
            lock.release()
        return result

    return wrapper


class MonitorMetaClass(type):
    """
    类监控元类
    """

    def __new__(mcs, cls_name, bases, attr_dict):
        for k, v in attr_dict.items():
            if (
                isinstance(v, types.FunctionType)
                and not k.startswith("_")
                and not k.startswith("send")
                and not k.startswith("register")
                and not k.startswith("notify")
                and not k.startswith("remove")
            ):
                attr_dict[k] = minium_log(v)
        return type.__new__(mcs, cls_name, bases, attr_dict)

