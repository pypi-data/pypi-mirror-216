#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: lockerzhang
@LastEditors: lockerzhang
@Description: 小程序层面的操作(包含 web 和 Native)
@Date: 2019-03-11 14:41:43
@LastEditTime: 2019-06-05 16:30:44
"""
from __future__ import annotations
import typing
import types
from enum import Enum
from typing import Any
import functools

from minium.utils.utils import AsyncCondition
from .page import Page
from .minium_object import MiniumObject, RetryableApi
from ...framework.exception import *
from ...utils.injectjs import JsMode
from ...utils.platforms import *
from ...utils.emitter import ee
from ...utils.eventloop import event_loop
from ...utils.utils import get_result, WaitTimeoutError, retry, catch, urlencode
from .callback import AsyncCallback, Callback
import os
import json
import threading
import base64
import io
import time
import datetime
import copy


cur_path = os.path.dirname(os.path.realpath(__file__))  # source_path是存放资源文件的路径
conf_path = os.path.join(os.path.dirname(cur_path), "conf/iOS_conf")


class MockNetworkType(Enum):
    ALWAYS = 0
    ONCE = 1


class MockCloudCallType(Enum):
    ALWAYS = 0
    ONCE = 1


class RouteCommand:
    def __init__(
        self, open_type, path, route_done_lock=None, default_route_result=None
    ) -> None:
        """页面跳转指令

        :param str open_type: 跳转操作: navigateTo/redirectTo/reLaunch/switchTab
        :param str path: 路径: /pages/index/index?a=b&c=1
        :param AsyncCondition route_done_lock: onAppRouteDone回调释放的异步锁, defaults to None(不需要等待route done)
        :param bool default_route_result: _description_, defaults to None
        """
        self.open_type = open_type
        self.path = path
        self._open_id = None  # 调用异步接口返回的请求id

        self._async_msg_lock: AsyncCondition = route_done_lock
        self._open_callback = AsyncCallback(event_loop)
        self._route_changed = None
        self._error: Exception = None

    @property
    def open_id(self):
        return self._open_id

    @open_id.setter
    def open_id(self, value):
        if value == self._open_id:
            return
        self._open_id = value
        ee.once(self._open_id, self.open_callback)

    def on_connect_state_change(self, value: bool, error: Exception):
        if not value:  # break
            self._error = error

    async def _wait_msg_lock(self, timeout=None):
        await self._async_msg_lock.acquire()
        ret = await self._async_msg_lock.wait(timeout=timeout)
        self._async_msg_lock.release()
        return ret

    async def _wait_route_changed_async(self, timeout=None) -> bool:
        if not timeout:
            timeout = 5

        ret = await self._wait_msg_lock(timeout)
        return ret

    def __enter__(self):
        ee.on("connect_state_change", self.on_connect_state_change)
        return self

    def __exit__(self, *args):
        ee.remove_listener("connect_state_change", self.on_connect_state_change)

    def listen_route_change(self, timeout):
        if not self._async_msg_lock:
            return
        self._route_changed = event_loop.run_coroutine(
            self._wait_route_changed_async(timeout + 5)
        )
        return self._route_changed

    def open_callback(self, *args):
        return self._open_callback.callback(*args)

    def cancel_open_callback(self):
        if self._open_id:
            ee.remove_listener(self._open_id, self.open_callback)
        return self._open_callback.cancel()

    def get_open_result(self, timeout):
        """获取打开页面操作结果"""
        try:
            if self._open_callback.wait_called(timeout):
                return self._open_callback.get_result()
            raise MiniTimeoutError(
                f"[{self._open_id}][{self.open_type}] receive from remote timeout"
            )
        except MiniClientOfflineError as co:
            raise MiniTimeoutCauseByClientOffline(str(co)) from co
        except MiniConnectionClosedError as cc:
            raise MiniTimeoutCauseByConnectionBreakError(str(cc)) from cc

    def get_route_result(self, timeout):
        if not self._async_msg_lock:
            # 不需要等待则认为已经route done
            return True
        if self._error:
            raise self._error
        try:
            if get_result(self._route_changed, timeout):
                return True
            return False
        except WaitTimeoutError as wt:
            if self._error:
                if isinstance(self._error, MiniClientOfflineError):
                    raise MiniTimeoutCauseByClientOffline(str(self._error)) from wt
                if isinstance(self._error, MiniConnectionClosedError):
                    raise MiniTimeoutCauseByConnectionBreakError(
                        str(self._error)
                    ) from wt
                raise self._error from wt
            if self.open_type == "switchTab":
                # switchTab方法可能没有on app route done
                return False
            raise wt
        except MiniClientOfflineError as co:
            raise MiniTimeoutCauseByClientOffline(str(co)) from co
        except MiniConnectionClosedError as cc:
            raise MiniTimeoutCauseByConnectionBreakError(str(cc)) from cc


class App(MiniumObject, metaclass=RetryableApi):
    __RETRY_API__ = [
        "enable_log",
        "screen_shot",
        "expose_function",
        "get_all_pages_path",
        "get_current_page",
        # "get_page_stack",  # _page_stack方法重试
        "wait_util",
        "hook_wx_method",
        "release_hook_wx_method",
        "hook_current_page_method",
        "restore_wx_method",
        "restore_request",
        "mock_request",
        # "mock_request_once",  #如果重试, 会影响once的逻辑
        "restore_call_function",
        "mock_call_function",
        # "mock_call_function_once",  #如果重试, 会影响once的逻辑
        "restore_call_container",
        "mock_call_container",
        # "mock_call_container_once",  #如果重试, 会影响once的逻辑
        "edit_editor_text",
        "reflesh_mocked_images",
        "mock_choose_images",  # 重试可能遇上前面已经mock的情况, 但已经兼容
        "mock_choose_image_with_name",
        # protect(common method)
        "_mock_wx_method",  # 各类mock方法都使用到
        "_page_stack",
        # private
        "__get_pages_config",
    ]

    class CurrentPage(object):
        """代理current_page
        """
        def __init__(self, app: App) -> None:
            self.app = app

        def __del__(self):
            self.app = None

        @property
        def _current_page(self):
            return self.app._current_page or self.app.get_current_page()

        def _catch_page_destroyed_error(self, func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except PageDestroyed:
                    attr = getattr(self.app._current_page, func.__name__)
                    return attr(*args, **kwargs)
            return wrapper

        def __getattr__(self, __name: str) -> Any:
            attr = getattr(self._current_page, __name)
            if callable(attr):  # 可能是api接口
                return self._catch_page_destroyed_error(attr)
            return attr
        
        def __eq__(self, page):
            return self._current_page == page
        
        def __ne__(self, page) -> bool:
            return not (self._current_page == page)
        
        def __repr__(self):
            _current_page = self._current_page
            return "Page(id={0}, path={1}, query={2})".format(
                _current_page.page_id, _current_page.path, _current_page.query
            )

    def __init__(self, connection, relaunch=False, native=None, platform="ide", **kwargs):
        """
        创建一个 APP 实例
        :param connection:
        """
        super().__init__()
        self.connection = connection
        self.native = native
        self.platform = platform
        self.js_mode: JsMode = (
            JsMode.JUST_ES5 if platform in [OS_ANDROID, OS_IOS] else JsMode.ALL
        )  # 真机调试2.0环境下只支持es5语法
        self._msg_lock = threading.Condition()
        self._async_msg_lock = AsyncCondition(loop=event_loop)
        self._is_log_enable = False
        self._main_page_path = None
        self.route_return_page = None
        self._route_return_page_update_time = None  # 监听到页面变化后由于是异步通信, 有可能出现两个相近信息重复顺序调乱
        self._appid = None
        self._current_page = None  # 只有调用 get_current_page 和 监听到 _on_route_changed 回调时更新
        self.current_page = App.CurrentPage(self)
        self._mocked_images = None
        self._mocked_images_dir = None
        self._mocked_images_data = {}
        # init methods
        self._route_change_listener()
        self._request_stack_listener()
        # self.__is_injected = self._evaluate_js(
        #     "checkInject"
        # )  # 是否已经注入过了, 注入过的环境不需要重复注入, 防止出现多次回调等预期之外的情况
        env = self._evaluate_js("checkEnv")
        self.__is_injected = env.get("injected")  # 是否已经注入过了, 注入过的环境不需要重复注入, 防止出现多次回调等预期之外的情况
        self._is_third_app = env.get("isThirdApp")  # 是否是第三方开发框架构建的小程序, 影响mock & hook功能
        self.pages = []
        self.tabbar_pages = {}
        self.__get_pages_config()
        if not self.__is_injected and self.js_mode is JsMode.JUST_ES5:  # 注入一些垫片
            self._evaluate_js("helpers")
        if relaunch:
            self.relaunch(self.main_page_path.path, self.main_page_path.query)

    def release(self):
        """释放循环引用
        _current_page -> app -> _current_page
        """
        current_page = self._current_page
        if current_page:
            self._current_page = None
            current_page.app = None
        self.current_page.app = None
        self.current_page = None

    @property
    def app_id(self):
        if not self._appid:
            self._appid = self._get_account_info_sync().result.result.miniProgram.appId
        return self._appid

    # @property
    # def current_page(self):
    #     return self._current_page or self.get_current_page()

    @property
    def is_injected(self):
        """
        是否已经注入过, 如果没有, 则设置并进行注入操作
        """
        if self.__is_injected:
            return True
        self.__is_injected = True
        return False

    @property
    def main_page_path(self):
        if self._main_page_path is None:
            options = self._get_launch_options_sync().result.result
            if options.path == "":
                raise MiniLaunchError("get launch options failed")
            self._main_page_path = Page(None, options.path, options.query, None)
        return self._main_page_path

    def _evaluate_js(
        self,
        filename,
        args=None,
        sync=True,
        default=None,
        code_format_info=None,
        **kwargs,
    ):
        """
        重写, 默认使用self.js_mode参数
        """
        return super(App, self)._evaluate_js(
            filename, args, sync, default, code_format_info, self.js_mode, **kwargs
        )

    def enable_log(self):
        """
        打开日志
        每次调用, 都会新增一个回调, 最好记录一下已经调用过
        """
        if not self._is_log_enable:
            self.connection.send("App.enableLog")
            self._is_log_enable = True

    @catch(MiniClientOfflineError)
    def exit(self):
        """
        退出小程序
        :return: None
        """
        setattr(self.connection, "_is_close_app_by_cmd", True)
        self.connection.send_async("App.exit", ignore_response=True)

    def get_account_info_sync(self):
        """
        获取账号信息
        :return:
        """
        return self._get_account_info_sync()

    def screen_shot(self, save_path=None, format="raw", use_native=False):
        """
        截图, 仅能截取 webview 部分, 原生控件不能截取到
        :param save_path:
        :param format: raw or pillow
        :param use_native: use native interface
        :return:
        """
        if self.platform != "ide":
            # 小程序不是运行在开发者工具中, 不支持`App.captureScreenshot`
            if self.native:
                # 使用native接口实现截图
                _save_path = save_path or "%s.png" % datetime.datetime.now().strftime(
                    "%H%M%S%f"
                )
                self.native.screen_shot(_save_path)
                if not os.path.isfile(_save_path):
                    self.logger.error("%s.screen_shot fail" % self.native.__class__)
                    return None
                with open(_save_path, "rb") as fd:
                    raw_value = fd.read()
                if not save_path:
                    os.remove(_save_path)
            else:
                self.logger.error("native instance not exists, please check")
        else:
            try:
                b64_data = (
                    self.connection.send("App.captureScreenshot")
                    .get("result")
                    .get("data")
                )
            except MiniAppError as e:
                self.logger.error(e)
                return None
            else:
                raw_value = base64.b64decode(b64_data)
                png_header = b"\x89PNG\r\n\x1a\n"
                if not raw_value.startswith(png_header) and save_path:
                    self.logger.error("screenshot png format error")

                if save_path:
                    with open(save_path, "wb") as f:
                        f.write(raw_value)

        if format == "raw":
            return raw_value
        elif format == "pillow":
            from PIL import Image

            buff = io.BytesIO(raw_value)
            return Image.open(buff)
        else:
            self.logger.warning(f"unknown format:{format} for screenshot")
            return raw_value

    def expose_function(self, name, binding_function):
        """
        在 AppService 全局暴露方法, 供小程序侧调用测试脚本中的方法。
        :param name:
        :param binding_function:
        :return:
        """
        self._expose_function(name, binding_function)

    def add_observer(self, event, callback):
        """
        监听小程序的事件
        :param event: 需要监听的事件
        :param callback: 收到事件后的回调函数
        :return:
        """
        if not callable(callback):
            raise Exception("the callback is not a function")

        self.connection.register(event, callback)

    def remove_observer(self, event, callback=None):
        """
        移除小程序事件监听
        :param event: 监听的事件
        :param callback: 指定的监听函数, 不传则移除该事件所有监听函数
        :return:
        """
        self.connection.remove(event, callback)

    def on_exception_thrown(self, func):
        """
        JS 错误回调
        :param func: 回调函数
        :return:
        """
        self.connection.register("App.exceptionThrown", func)

    def call_wx_method(self, method, args=None, plugin_appid="auto"):
        """
        调用 wx 的方法
        :param method:
        :param args:
        :param plugin_appid: 调用插件[${appid}]中的方法, auto时自动获取当前页面是否插件页
        :return:
        """
        if plugin_appid == "auto":
            plugin_appid = (self._current_page or self.get_current_page()).plugin_appid
        return self._call_wx_method(method=method, args=args, plugin_appid=plugin_appid)

    def call_wx_method_async(
        self, method, args=None, plugin_appid="auto", ignore_response=False
    ):
        """
        调用 wx 的方法, 返回异步message id
        :param method:
        :param args:
        :param plugin_appid: 调用插件[${appid}]中的方法, auto时自动获取当前页面是否插件页
        :return: str(message_id)
        """
        if plugin_appid == "auto":
            plugin_appid = (self._current_page or self.get_current_page()).plugin_appid
        return self._call_wx_method(
            method=method,
            args=args,
            plugin_appid=plugin_appid,
            sync=False,
            ignore_response=ignore_response,
        )

    def get_all_pages_path(self):
        """
        获取所有已配置的页面路径
        :return:
        """
        return self._evaluate_js("getAllPagesPath")

    def __get_pages_config(self):
        """
        获取所有page相关信息
        """
        try:
            ret = self.evaluate(
                """function(){return {"pages": __wxConfig.pages, "tabBar": __wxConfig.tabBar && __wxConfig.tabBar.list} }""",
                sync=True,
            ).result.result
            self.pages = ret.get("pages", [])
            tabbar_list = ret.get("tabBar", None)
            if tabbar_list:
                idx = 0
                for tabbar in tabbar_list:
                    page_path = tabbar["pagePath"].rstrip(".html")
                    if not page_path.startswith("/"):
                        page_path = "/" + page_path
                    self.tabbar_pages[page_path] = tabbar
                    self.tabbar_pages[page_path].update(
                        {"index": idx, "pagePath": page_path.lstrip("/")}
                    )
                    idx += 1
        except MiniAppError:
            return {}
        return ret

    def get_current_page(self) -> Page:
        """
        获取当前顶层页面
        :return: Page 对象
        """

        def get_current_page(cnt=0):
            ret = self.connection.send("App.getCurrentPage")
            if hasattr(ret, "error"):
                raise Exception("Get current page fail, cause: %s" % ret.error)
            if not ret.result and cnt < 3:
                # 返回信息有问题, 没拿到pageId等属性
                return get_current_page(cnt + 1)
            return ret

        ret = get_current_page()
        page = Page(ret.result.pageId, ret.result.path, ret.result.query, self)
        # 记录当前页面
        self._current_page = page
        return page

    def evaluate(self, app_function: str, args=None, sync=False, desc=None):
        """
        向 app Service 层注入代码并执行
        :param app_function:
        :param args:
        :param sync:
        :param desc: 报错描述
        :return:
        """
        return self._evaluate(
            app_function=app_function, args=args, sync=sync, desc=desc
        )

    def get_page_stack(self) -> typing.List[Page]:
        """
        获取当前小程序所有的页面
        :return: Page List
        """
        return self._page_stack()

    # navigate_to不进行重试:
    # 1. 小程序断线没有重试必要, 必须等待小程序重连。
    # 2. ws链接断连在send的时候就已经检查并等待重连。
    # 3. 如果是单纯没有回包, 不能确定指令是否已经生效, 如指令生效并重试, 会增加页面堆栈
    def navigate_to(self, url, params=None, is_wait_url_change=True):
        """
        以导航的方式跳转到指定页面, 但是不能跳到 tabbar 页面。支持相对路径和绝对路径, 小程序中页面栈最多十层
        支持相对路径和绝对路径
        /page/tabBar/API/index: 绝对路径,最前面为/
        tabBar/API/index: 相对路径, 会被拼接在当前页面的路径后面
        :param url:"/page/tabBar/API/index"
        :param params: 页面参数
        :param is_wait_url_change: 是否等待页面变换完成
        :return:Page 对象
        """
        if params:
            url += (
                ("?" + urlencode(params))
                if url.find("?") < 0
                else ("&" + urlencode(params))
            )
        self.logger.info("NavigateTo: %s" % url)
        page = self._change_route_async("navigateTo", url, is_wait_url_change)
        if page != url.split("?")[0]:
            self.logger.warning("NavigateTo(%s) but(%s)" % (url, page.path))
        return page

    # redirect_to因为不产生新的页面堆栈, ws断连引起的回报丢失可以尝试重试
    @retry(2, (MiniTimeoutCauseByConnectionBreakError))
    def redirect_to(self, url, params=None, is_wait_url_change=True):
        """
        关闭当前页面, 重定向到应用内的某个页面。但是不允许跳转到 tabbar 页面
        :param url:"/page/tabBar/API/index"
        :param params: 页面参数
        :param is_wait_url_change: 是否等待页面变换完成
        :return:Page 对象
        """
        if params:
            url += (
                ("?" + urlencode(params))
                if url.find("?") < 0
                else ("&" + urlencode(params))
            )
        self.logger.info("RedirectTo: %s" % url)
        page = self._change_route_async("redirectTo", url, is_wait_url_change)
        if page != url.split("?")[0]:
            self.logger.warning("RedirectTo(%s) but(%s)" % (url, page.path))
        return page

    # relaunch因为不产生新的页面堆栈, ws断连引起的回报丢失可以尝试重试
    @retry(2, (MiniTimeoutCauseByConnectionBreakError))
    def relaunch(self, url, params=None, is_wait_url_change=True):
        """
        关闭所有页面, 打开到应用内的某个页面
        :param url: "/page/tabBar/API/index"
        :return:Page 对象
        """
        if params:
            url += (
                ("?" + urlencode(params))
                if url.find("?") < 0
                else ("&" + urlencode(params))
            )
        self.logger.info("ReLaunch: %s" % url)
        page = self._change_route_async("reLaunch", url, is_wait_url_change)
        if page != url.split("?")[0]:
            self.logger.warning("ReLaunch(%s) but(%s)" % (url, page.path))
        return page

    def navigate_back(self, delta=1):
        """
        关闭当前页面, 返回上一页面或多级页面。
        :param delta: 返回的层数, 如果超出 page stack 最大层数返回首页
        :return:Page 对象
        """
        # self._wait_until_page_is_stable()
        page = self.current_page
        page_stack = self._page_stack()
        if page.page_id == page_stack[0].page_id:
            self.logger.warning("Current page is root, can't navigate back")
            return page
        self.logger.info("NavigateBack from:%s" % page.path)
        self._call_wx_method("navigateBack", [{"delta": delta}])
        if self._route_changed():
            return self.route_return_page
        else:
            self.logger.warning("route has not change, may be navigate back fail")

    # switch_tab因为不产生新的页面堆栈, ws断连引起的回报丢失可以尝试重试
    @retry(2, (MiniTimeoutCauseByConnectionBreakError))
    def switch_tab(
        self, url, is_wait_url_change=True, is_click=False, wait_route_done_time=15
    ):
        """
        跳转到 tabBar 页面, 并关闭其他所有非 tabBar 页面
        :param url: "/page/tabBar/API/index"
        :param is_click: 点击触发帮用户触发一下onTabItemTap
        :return:Page 对象
        """
        page = self._change_route_async(
            "switchTab", url, is_wait_url_change, wait_route_done_time
        )
        if is_click and page.path in self.tabbar_pages:  # is tabbar and is click
            try:
                page.call_method(
                    "onTabItemTap",
                    {
                        "index": self.tabbar_pages[page.path]["index"],
                        "pagePath": self.tabbar_pages[page.path]["pagePath"],
                        "text": self.tabbar_pages[page.path]["text"],
                    },
                )
            except MiniAppError:
                # 尝试触发 onTabItemTap 即可
                pass
        if page != url.split("?")[0]:
            self.logger.warning("Switch tab(%s) but(%s)" % (url, page.path))
        return page

    def stop_audits(self, path: str = None):
        """
        停止体验测评
        :path: 存放评测结果html的路径, 默认不存
        :return: dict, 测评结果
        """
        ret = self._stop_audits()
        if path:
            html_result = ret["result"]["report"]
            with open(path, "w", encoding="utf-8") as h_f:
                h_f.write(html_result)
        return json.loads(ret["result"]["data"])

    def get_perf_time(self, entry_types: list = None):
        default_entry_types = ["render", "script", "navigation", "loadPackage"]
        if not entry_types:
            entry_types = default_entry_types
        for item_type in entry_types:
            if item_type not in default_entry_types:
                raise Exception("the entryType is not available")
        self._evaluate_js(
            "startGetPerformance",
            [
                entry_types,
            ],
        )

    def stop_get_perf_time(self):
        time.sleep(2)  # 收集数据的时间推后一点点, 怕收集不完全
        return self._evaluate_js("stopGetPerformance")

    def go_home(self, main_page_path=None):
        """
        跳转到首页
        :param main_page_path: 路径
        :return: Page 对象
        """
        if not main_page_path:
            main_page_path = self.main_page_path
        elif not isinstance(main_page_path, Page):
            main_page_path = Page(None, main_page_path, None, None)

        if main_page_path.path in self.tabbar_pages:
            if (
                self.current_page.path == main_page_path.path
            ):  # switch will not route done
                is_wait_url_change = False
            else:
                is_wait_url_change = True
            # switch_tab有可能没有route done回调, 最多等5s
            page = self.switch_tab(
                main_page_path.path,
                is_wait_url_change=is_wait_url_change,
                wait_route_done_time=5,
            )
        else:
            page = self.relaunch(main_page_path.path, main_page_path.query)
        return page

    def get_async_response(self, msg_id: str, timeout=None) -> None or dict:
        """
        description: 获取异步调用的结果
        param {*} self
        param {str} msg_id 消息ID
        param {int} timeout 超时时间
        return {*}
        """
        if timeout is None:
            return self._get_async_response(msg_id)
        ret = None

        def get():
            nonlocal ret
            ret = self._get_async_response(msg_id)
            return ret is not None

        self._wait(get, timeout)
        return ret

    def wait_for_page(self, page_path=None, max_timeout=10):
        if not self._current_page or self._current_page != page_path:
            # 没有记录到当前页面/当前页面不是目标页面, 等待页面跳转成功的回调
            self._route_changed(max_timeout)
            ret = (self.current_page == page_path)
            # issue#144 如果等不到预期的页面, 考虑是否因为页面栈满了(自动化流程中, 用户可以直接调用navigate to, 很有可能会满的)
            if not ret:
                self.logger.debug(f"{self.current_page} != {page_path}")
                if len(self._page_stack()) == 10:
                    self.logger.warning(
                        """
wait for page fail, probably because the page stack is exceeded 10
more infomation see: https://developers.weixin.qq.com/miniprogram/dev/api/route/wx.navigateTo.html#功能描述
"""
                    )
            return ret
        return True

    def wait_util(self, cnt, max_timeout=10):
        """
        {max_timeout}秒内, 剩余没有完成的请求数 <= {cnt}个
        符合上述条件则返回 True, 否则 False
        """
        return self._evaluate_js("waitUtil", [cnt, max_timeout], default=False)

    def _get_launch_options_sync(self):
        return self._call_wx_method("getLaunchOptionsSync")

    def _change_route(self, open_type, path, is_wait_url_change=True) -> Page:
        """
        跳转页面
        call wx method -> call result / on app route done -> on app route done / call result
        "call result" and "on app route done" should wait together
        """
        self.call_wx_method(open_type, [{"url": path}])
        if is_wait_url_change and self._route_changed():
            return self.route_return_page
        else:
            return self.current_page  # todo: 状态有BUG, 超时也认为可用的

    def _change_route_async(
        self, open_type, path, is_wait_url_change=True, wait_route_done_time=15
    ):
        """
        跳转页面
        call wx method -> call result / on app route done -> on app route done / call result
        "call result" and "on app route done" should wait together
        """
        wait_timeout = self.connection.timeout
        with RouteCommand(
            open_type,
            path,
            route_done_lock=self._async_msg_lock if is_wait_url_change else None,
        ) as cmd:
            cmd.listen_route_change(wait_timeout)

            cmd.open_id = self.call_wx_method_async(open_type, [{"url": path}])
            # 理论上RouteCommand中通过ee监听了不会再在这里获取到结果, 以防线程切换过程导致时序问题，这里做一个兜底
            response = self.connection.get_aysnc_msg_return(cmd.open_id)
            if response is None:
                cmd.get_open_result(wait_timeout)
            else:
                cmd.cancel_open_callback()

            if cmd.get_route_result(wait_route_done_time):
                return self.current_page
            else:
                return self.get_current_page()  # 没有等到route done, 直接获取当前页面

    def _on_route_changed(self, message):
        if not message.name == "onAppRouteDone":
            return
        args = message.args
        options = args[0]
        update_time = args[1] if len(args) > 1 else int(time.time() * 1000)
        if (
            self._route_return_page_update_time
            and self._route_return_page_update_time > update_time
        ):
            # 旧信息, 丢弃
            return
        self.route_return_page = Page(
            options.webviewId, options.path, options.query, self
        )
        # 记录当前页面
        self._current_page = self.route_return_page
        self._notify_msg_lock()
        self.logger.info("Route changed, %s" % message)

    def _route_changed(self, timeout=None):
        if not timeout:
            timeout = 5

        self._msg_lock.acquire()
        ret = self._msg_lock.wait(timeout)
        self._msg_lock.release()
        return ret

    def _notify_msg_lock(self):
        async def _notify():
            await self._async_msg_lock.acquire()
            self._async_msg_lock.notify_all()
            self._async_msg_lock.release()

        event_loop.run_coroutine(_notify())
        self._msg_lock.acquire()
        self._msg_lock.notify_all()
        self._msg_lock.release()

    async def _wait_msg_lock(self, timeout=None):
        await self._async_msg_lock.acquire()
        ret = await self._async_msg_lock.wait(timeout=timeout)
        self._async_msg_lock.release()
        return ret

    async def _wait_route_changed_async(self, timeout=None):
        if not timeout:
            timeout = 5

        ret = await self._wait_msg_lock(timeout)
        return ret

    def _route_change_listener(self):
        self._unregister("onAppRouteDone")
        self._expose_function("onAppRouteDone", self._on_route_changed)
        self._evaluate(
            """function () {
    if (!global.__minium_onAppRouteDone) {
        wx.onAppRouteDone(function (options) {
            onAppRouteDone(options, Date.now())
        })
        global.__minium_onAppRouteDone = true
    }
}""",
            sync=True,
        )

    def _request_stack_listener(self):
        return self._evaluate_js("requestStack")

    def _get_account_info_sync(self):
        return self._call_wx_method("getAccountInfoSync")

    def _page_stack(self):
        ret = self.connection.send("App.getPageStack")
        page_stack = []
        for page in ret.result.pageStack:
            page_stack.append(Page(page.pageId, page.path, page.query, self))
        return page_stack

    # ws断连可重试
    @retry(2, (MiniConnectionClosedError))
    def _stop_audits(self):
        ret = self.connection.send("Tool.stopAudits")
        return ret

    def hook_wx_method(
        self,
        method: str,
        before: Callback or types.FunctionType = None,
        after: Callback or types.FunctionType = None,
        callback: Callback or types.FunctionType = None,
    ):
        """
        hook wx 方法
        :param method: 需要 hook 的方法
        :param before: 在需要 hook 的方法之前调用
        :param after: 在需要 hook 的方法之后调用
        :param callback: 在需要 hook 的方法回调之后调用
        :return:
        """
        stages: typing.List[types.FunctionType] = []  # 完成的步骤
        if isinstance(before, Callback):
            before = before.callback
        if isinstance(after, Callback):
            after = after.callback
        if isinstance(callback, Callback):
            callback = callback.callback

        if before and not callable(before):
            self.logger.error(f"wx.{method} hook before method is non-callable")
            return

        if after and not callable(after):
            self.logger.error(f"{method} hook after method is non-callable")
            return

        if callback and not callable(callback):
            self.logger.error(f"{method} hook callback method is non-callable")
            return
        try:

            def super_before(msg):
                self.logger.debug(f"{method} before hook result: {msg['args']}")
                if before:
                    before(msg["args"])

            if before:
                stages.append(super_before)
                self._expose_function(
                    method + "_" + super_before.__name__, super_before
                )

            def super_after(msg):
                self.logger.debug(f"wx.{method} after hook result: {msg['args']}")
                if after:
                    after(msg["args"])

            if after:
                stages.append(super_after)
                self._expose_function(method + "_" + super_after.__name__, super_after)

            def super_callback(msg):
                self.logger.debug(f"wx.{method} callback hook result: {msg['args']}")
                if callback:
                    callback(msg["args"])

            if callback and not method.endswith("Sync"):  # Sync方法没有callback，通过after回调
                stages.append(super_callback)
                self._expose_function(
                    method + "_" + super_callback.__name__, super_callback
                )
            return self._evaluate_js(
                "hookWxMethod",
                code_format_info=dict(
                    method=method,
                    origin=method + "_MiniumOrigin",
                    before=method + "_" + super_before.__name__,
                    after=method + "_" + super_after.__name__,
                    callback=method + "_" + super_callback.__name__,
                ),
            )
        except MiniError:
            for stage in stages:
                self.remove_observer(method + "_" + stage.__name__, stage)
            raise

    def release_hook_wx_method(self, method):
        """
        释放 hook wx 方法
        :param method: 需要释放 hook 的方法
        :return:
        """
        self._evaluate_js(
            "releaseHookWxMethod",
            code_format_info=dict(
                origin=method + "_MiniumOrigin",
                method=method,
                before=method + "_super_before",
                after=method + "_super_after",
                callback=method + "_super_callback",
            ),
        )
        # 移除监听函数
        self.connection.remove(method + "_super_before")
        self.connection.remove(method + "_super_after")
        self.connection.remove(method + "_super_callback")

    def hook_current_page_method(self, method, callback):
        """
        hook 当前页面的方法
        :param method:  方法名
        :param callback:    回调函数
        """

        if isinstance(callback, Callback):
            callback = callback.callback

        def super_callback(msg):
            self.logger.debug(f"Page.{method} call hook result: {msg['args']}")
            if callback:
                callback(msg["args"])

        if callback and not callable(callback):
            self.logger.error(f"Page.{method} hook callback method is non-callable")
            return
        try:
            if callback:
                self._expose_function(
                    "page_hook_" + method + "_" + super_callback.__name__,
                    super_callback,
                )
            self._evaluate_js(
                "hookCurrentPageMethod",
                code_format_info={
                    "method": method,
                    "callback": "page_hook_" + method + "_" + super_callback.__name__,
                },
            )
        except MiniError:
            if callback:
                self.remove_observer(
                    "page_hook_" + method + "_" + super_callback.__name__,
                    super_callback,
                )
            raise

    def release_hook_current_page_method(self, method):
        # 移除监听函数
        self.connection.remove("page_hook_" + method + "_super_callback")

    ###
    # 各类 mock
    ###

    def mock_wx_method(
        self,
        method,
        functionDeclaration: str = None,
        result=None,
        args=None,
        success=True,
        plugin_appid="auto",
    ):
        """
        mock wx method and return result
        :param self:
        :param method:
        :param functionDeclaration:
        :param result:
        :param args:
        :param success:
        :return:
        """
        if plugin_appid == "auto":
            plugin_appid = (self._current_page or self.get_current_page()).plugin_appid
        self._mock_wx_method(
            method=method,
            functionDeclaration=functionDeclaration,
            result=result,
            args=args,
            success=success,
            plugin_appid=plugin_appid,
        )

    def restore_wx_method(self, method, plugin_appid="auto"):
        """
        恢复被 mock 的方法
        :param method: mock的方法
        :param plugin_appid: 插件appid
        :return:
        """
        params = {"method": method}
        if plugin_appid == "auto":
            plugin_appid = (self._current_page or self.get_current_page()).plugin_appid
        if plugin_appid:
            params["pluginId"] = plugin_appid
        self.connection.send("App.mockWxMethod", params)

    def _mock_network(
        self,
        interface: str,
        rule: str or dict,
        success=None,
        fail=None,
        mock_type=MockNetworkType.ALWAYS,
    ):
        if success and fail:
            raise RuntimeError("Can't call back both SUCCESS and FAIL")
        if not (success or fail):
            raise RuntimeError("Must call back either SUCCESS or FAIL")
        if isinstance(rule, (str, bytes)):
            # 默认匹配url
            _rule = {"url": rule}
        else:
            _rule = rule
        if success:
            _rule["success"] = success
        elif fail:
            if isinstance(fail, (str, bytes)):
                fail = {"errMsg": "%s:fail %s" % (interface, fail)}
            _rule["fail"] = fail
        if mock_type == MockNetworkType.ONCE:
            # 保护字段, 保证不冲突
            _rule["_miniMockType"] = MockNetworkType.ONCE.value
        has_mock = self._evaluate_js(
            "addNetworkMockRule", [_rule], code_format_info={"interface": interface}
        )
        if not has_mock:
            retry(self.__class__.__RETRY_CNT__, self.__class__.__RETRY_EXCEPTION__)(
                self._evaluate_js
            )("mockNetwork", code_format_info={"interface": interface})

    def _restore_network(self, interface: str):
        """
        恢复被mock的网络接口
        """
        return self._evaluate_js(
            "cleanNetworkMockRule", code_format_info={"interface": interface}
        )

    def _mock_cloud_call(
        self,
        interface: str,
        rule: dict,
        success=None,
        fail=None,
        mock_type=MockCloudCallType.ALWAYS,
    ):
        if success and fail:
            raise RuntimeError("Can't call back both SUCCESS and FAIL")
        if not (success or fail):
            raise RuntimeError("Must call back either SUCCESS or FAIL")
        if not isinstance(rule, dict):
            raise RuntimeError(
                'Cloud call mock rule must be a dict like {"name": "testCloudFunction"}'
            )
        _rule = copy.deepcopy(rule)
        if success:
            _rule["success"] = success
        elif fail:
            if isinstance(fail, (str, bytes)):
                fail = {"errMsg": "%s:fail %s" % (interface, fail)}
            _rule["fail"] = fail
        if mock_type == MockCloudCallType.ONCE:
            # 保护字段, 保证不冲突
            _rule["_miniMockType"] = MockCloudCallType.ONCE.value
        has_mock = self._evaluate_js("addCloudCallMockRule", [_rule, interface])
        if not has_mock:
            retry(self.__class__.__RETRY_CNT__, self.__class__.__RETRY_EXCEPTION__)(
                self._evaluate_js
            )("mockCloudCall")

    def _restore_cloud_call(self, interface: str):
        """
        恢复被mock的云调用接口
        """
        return self._evaluate_js(
            "cleanCloudCallMockRule",
            [
                interface,
            ],
        )

    def mock_request(self, rule: str or dict, success=None, fail=None):
        """
        mock wx.request, 根据正则mock规则返回mock结果
        """
        return self._mock_network("request", rule, success, fail)

    def mock_request_once(self, rule: str or dict, success=None, fail=None):
        """
        mock wx.request, 根据正则mock规则返回mock结果, 一旦匹配上了, 即废除该rule
        """
        return self._mock_network("request", rule, success, fail, MockNetworkType.ONCE)

    def restore_request(self):
        return self._restore_network("request")

    def mock_call_function(self, rule: dict, success=None, fail=None):
        return self._mock_cloud_call("callFunction", rule, success, fail)

    def mock_call_function_once(self, rule: dict, success=None, fail=None):
        return self._mock_cloud_call(
            "callFunction", rule, success, fail, MockCloudCallType.ONCE
        )

    def mock_call_container(self, rule: dict, success=None, fail=None):
        return self._mock_cloud_call("callContainer", rule, success, fail)

    def mock_call_container_once(self, rule: dict, success=None, fail=None):
        return self._mock_cloud_call(
            "callContainer", rule, success, fail, MockCloudCallType.ONCE
        )

    def restore_call_function(self):
        return self._restore_cloud_call("callFunction")

    def restore_call_container(self):
        return self._restore_cloud_call("callContainer")

    def mock_show_modal(self, answer=True):
        """
        mock 弹窗
        :param answer: 默认点击确定
        :return: None
        """
        self._mock_wx_method(
            "showModal",
            result={
                "cancel": answer,
                "confirm": False if answer else True,
                "errMsg": "showModal:ok",
            },
        )

    def mock_get_location(
        self,
        acc=65,
        horizontal_acc=65,
        vertical_acc=65,
        speed=-1,
        altitude=0,
        latitude=23.12908,
        longitude=113.26436,
    ):
        """
        mock 位置获取
        :param acc: 位置的精确度
        :param horizontal_acc: 水平精度, 单位 m
        :param vertical_acc: 垂直精度, 单位 m(Android 无法获取, 返回 0)
        :param speed: 速度, 单位 m/s
        :param altitude: 高度, 单位 m
        :param latitude: 纬度, 范围为 -90~90, 负数表示南纬
        :param longitude: 经度, 范围为 -180~180, 负数表示西经
        :return:
        """
        self._mock_wx_method(
            "getLocation",
            result={
                "accuracy": acc,
                "altitude": altitude,
                "errMsg": "getLocation:ok",
                "horizontalAccuracy": horizontal_acc,
                "verticalAccuracy": vertical_acc,
                "latitude": latitude,
                "longitude": longitude,
                "speed": speed,
            },
        )

    def mock_show_action_sheet(self, tap_index=0):
        """
        mock 显示操作菜单
        :param tap_index: 用户点击的按钮序号, 从上到下的顺序, 从0开始
        :return:
        """
        self._mock_wx_method(
            "showActionSheet",
            result={"errMsg": "showActionSheet:ok", "tapIndex": tap_index},
        )

    def edit_editor_text(self, editorid, text):
        ret = self._evaluate_js(
            "editEditorText",
            code_format_info={
                "editorid": editorid,
                "text": text,
            },
        )
        self.logger.info(ret)
        return ret

    def reflesh_mocked_images(self, mock_images_dir=None, mock_images=None):
        """
        1. 暴露全局方法用于mock chooseImage
        2. 获取已经有的文件列表
        """
        self._mocked_images_dir = mock_images_dir or None
        self._mocked_images_data = mock_images or {}
        if self._mocked_images is None:
            self._mocked_images = {}  # 需要先调用一次reflesh再进行mock
        ret = self._evaluate_js(
            "mockChooseImage",
        )  # [{name, size}]
        if not ret:
            return
        for item in ret:
            self._mocked_images[item["name"]] = item["size"]

    def mock_choose_image(self, name: str, image_b64data: str):
        """
        mock chooseImage, chooseMedia, takePhoto等选择图片相关接口
        :param name: 文件名
        :param image_b64data: base64格式的图片数据
        :return bool: True for success, False for fail
        """
        return self.mock_choose_images([{"name": name, "b64data": image_b64data}])

    def mock_choose_images(self, items):
        """
        mock chooseImage, chooseMedia, takePhoto等选择图片相关接口
        :param items: [{name, b64data} ... ]
            :name: 文件名
            :b64data: base64格式的图片数据
        :return bool: True for success, False for fail
        """
        if self._mocked_images is None:
            self.reflesh_mocked_images()
        ret = self._evaluate_js(
            "evalMockChooseImage",
            [
                {"imageName": item["name"], "size": self._mocked_images[item["name"]]}
                if item["name"] in self._mocked_images
                else {"imageName": item["name"], "imageData": item["b64data"]}
                for item in items
            ],
        )
        for result in ret:
            self._mocked_images[result["name"]] = result["size"]
        return True

    def mock_choose_image_with_name(self, file_name):
        """
        通过文件名mock上传图片, 被mock的图片需要放在`${mock_images_dir}`或配置在`${mock_images}`键值对中
        :return bool: True for success, False for fail
        """
        if not self._mocked_images_dir and not self._mocked_images_data:
            raise MiniConfigError(
                "can't not use `mock_choose_image`, please config `mock_images_dir` or `mock_images` first"
            )
        if self._mocked_images is None:
            self.reflesh_mocked_images()
        if file_name in self._mocked_images:
            self._evaluate_js(
                "evalMockChooseImage",
                [{"imageName": file_name, "size": self._mocked_images[file_name]}],
            )
            return True
        if file_name in self._mocked_images_data:  # 命中data
            file_content = self._mocked_images_data[file_name]
        else:
            file_path = os.path.join(self._mocked_images_dir, file_name)
            if os.path.isfile(file_path):
                with open(file_path, "rb") as fd:
                    c = fd.read()
                    file_content = base64.b64encode(c).decode("utf8")
            else:
                file_content = ""
        if not file_content:
            return False
        ret = self._evaluate_js(
            "evalMockChooseImage", [{"imageName": file_name, "imageData": file_content}]
        )
        for result in ret:
            self._mocked_images[result["name"]] = result["size"]
        return True
