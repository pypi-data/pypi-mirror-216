#!/usr/bin/env python3
# Created by xiazeng on 2019-06-11
from .basenative import BaseNative, logger
from ...utils.utils import Version
from ...framework.exception import MiniLaunchError

class IdeNative(BaseNative):
    _mini = None  # ide的native操作也以来minium的实例，可能引起循环引用，需要谨慎处理

    def __init__(self, json_conf, mini=None):
        self.use_native = False
        self.mini = mini
        super().__init__(json_conf)

    def __del__(self):
        self.mini = None

    def release(self):
        self.release_auto_authorize()
        self.mini = None

    @property
    def mini(self):
        return self._mini

    @mini.setter
    def mini(self, value):
        if self._mini == value:
            return
        self._mini = value
        if value is not None and getattr(self._mini, "connection"):
            self.__get_dev_tool_info()

    def start_wechat(self):
        pass

    def stop_wechat(self):
        ...

    def connect_weapp(self, path):
        ...

    def __get_dev_tool_info(self):
        try:
            result = self._mini.connection.send("Tool.getInfo", max_timeout=3).result
        except Exception:
            # not support Tool.getInfo
            return
        if Version(result.SDKVersion) < Version("2.7.3"):
            raise MiniLaunchError("基础库版本[%s]过低，请确认基础库版本>=2.7.3" % self.sdk_version)
        if str(result.version).endswith("2") and Version(result.version) >= "1.06.2211072":  # nightly
            self.use_native = True
        elif str(result.version).endswith("1") and Version(result.version) >= "1.06.2212011":  # RC
            self.use_native = True
        elif Version(result.version) >= "1.06.2301160":  # Stable
            self.use_native = True

    def send(self, method, data=None):
        if self.use_native and self.mini:
            ret = self.mini.connection.send("Tool.native", {
                "method": method,
                "data": data
            })
            if "error" in ret.result:
                logger.warning(f"handle {method} error: {ret.result.error.get('message', '')}")
            return ret

    def go_home(self):
        """
        跳转到小程序首页
        """
        if self.use_native:
            return self.send("goHome")

    def navigate_back(self):
        """
        左上角返回上一页
        """
        if self.use_native:
            return self.send("navigateLeft")

    def switch_tab(self, url):
        """
        点击tabBar
        """
        if self.use_native:
            return self.send("switchTab", {
                "url": url,  # tabbar 路径, 不带参数
            })

    def close_payment_dialog(self):
        """
        关闭支付弹窗
        """
        if self.use_native:
            return self.send("closePaymentDialog")

    def screen_shot(self, filename, return_format="raw"):
        if self.mini:
            self.mini.app.platform = "ide"  # 防止无限回调
            self.mini.app.screen_shot(filename, return_format)
            return filename
        return ""

    def pick_media_file(
        self,
        cap_type="camera",
        media_type="photo",
        original=False,
        duration=5.0,
        names=None,
    ):
        raise NotImplementedError("ide not implemented")

    def allow_authorize(self, answer=True, title=None):
        return self._allow_authorize(answer)

    def _allow_authorize(self, answer):
        """
        mock实现, 所有接口引发的原生弹窗授权理论上都可以使用
        """
        if self.use_native:
            return self.send("authorizeAllow" if answer else "authorizeCancel")
        if self.mini:
            return self.mini.app._evaluate_js(
                "ideHandleAuthModal",
                [
                    "允许" if answer else "拒绝",
                ],
            )
        return False

    def allow_login(self, answer=True):
        self._allow_authorize(answer)

    def allow_get_user_info(self, answer=True):
        self._allow_authorize(answer)

    def allow_get_location(self, answer=True):
        self._allow_authorize(answer)

    def allow_get_we_run_data(self, answer=True):
        self._allow_authorize(answer)

    def allow_record(self, answer=True):
        self._allow_authorize(answer)

    def allow_write_photos_album(self, answer=True):
        self._allow_authorize(answer)

    def allow_camera(self, answer=True):
        self._allow_authorize(answer)

    def allow_get_user_phone(self, answer=True):
        self._allow_authorize(answer)

    def allow_send_subscribe_message(self, answer=True):
        """
        允许发送订阅消息
        """
        if self.use_native:
            return self.handle_modal("允许" if answer else "取消")
        if self.mini:
            return self.mini.app._evaluate_js(
                "ideHandleAuthModal",
                [
                    "允许" if answer else "取消",
                ],
            )
        return False

    def handle_modal(self, btn_text="确定", title: str = None, force_title=False):
        """
        mock实现, 所有接口引发的原生弹窗理论上都可以使用
        ps: 需要兼容一下授权弹窗

        新工具版本支持native操作, 区分confirm/cancel, btn_text参数支持bool类型指定confirm/cancel
        """
        if self.use_native:
            cancel = not btn_text if isinstance(btn_text, bool) else btn_text in ("取消", "拒绝")
            if cancel:
                return self.send("cancelModal")
            else:
                return self.send("confirmModal")
        if self.mini:
            return self.mini.app._evaluate_js(
                "ideHandleModal",
                [
                    btn_text,
                ],
            )

    def handle_action_sheet(self, item):
        if self.mini:
            return self.mini.app._evaluate_js(
                "ideHandleModal",
                [
                    item,
                ],
            )
        # self.handle_modal(item)

    def forward_miniprogram(
        self, name: str, text: str = None, create_new_chat: bool = True
    ):
        raise NotImplementedError("ide not implemented")

    def forward_miniprogram_inside(
        self, name: str, text: str = None, create_new_chat: bool = True
    ):
        # if self.use_native:
        #     return self.send("shareConfirm")  # 不支持confirm
        raise NotImplementedError("ide not implemented")

    def forward_miniprogram_cancel(self):
        if self.use_native:
            return self.send("shareCancel")

    def input_text(self, text):
        if self.mini:
            self.mini.app.get_current_page().get_element("input").input(text)

    def input_clear(self):
        if self.mini:
            self.mini.app.get_current_page().get_element("input").input("")

    def textarea_text(self, text, index=0):
        if self.mini:
            els = self.mini.app.get_current_page().get_elements("textarea")
            els[index].input(text)

    def textarea_clear(self, index=0):
        if self.mini:
            els = self.mini.app.get_current_page().get_elements("textarea")
            els[index].input("")

    def send_custom_message(self, message=None):
        ...

    def phone_call(self):
        ...

    def map_select_location(self, name=None):
        if self.mini:
            return self.mini.app._evaluate_js(
                "ideHandleMap",
                [
                    name,
                ],
            )

    def map_back_to_mp(self):
        if self.mini:
            return self.mini.app._evaluate_js(
                "ideHandleMap",
                [
                    "取消",
                ],
            )

    def deactivate(self, duration):
        ...

    def get_authorize_settings(self):
        ...

    def back_from_authorize_setting(self):
        ...

    def authorize_page_checkbox_enable(self, name, enable):
        ...
