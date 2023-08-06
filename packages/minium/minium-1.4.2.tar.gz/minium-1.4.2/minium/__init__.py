#!/usr/bin/env python3
# Created by xiazeng on 2019-06-24
from .miniprogram.base_driver.version import build_version
from .miniprogram import get_minium_driver
from .miniprogram.wx_minium import WXMinium
from .miniprogram.qq_minium import QQMinium
from .miniprogram.base_driver.page import Page
from .miniprogram.base_driver.app import App
from .miniprogram.base_driver.element import BaseElement
from .miniprogram.base_driver.callback import Callback
from .framework.minitest import MiniTest
from .framework.assertbase import *
from .framework.miniddt import *
from .utils.utils import retry, catch
from .framework.miniresult import MiniResult
from .framework.exception import *
from .framework.libs.unittest import *
from .native import *


def Minium(conf=None, *args, **kwargs):
    return get_minium_driver(conf, *args, **kwargs)


__version__ = build_version().get("version", "1.2.0")
project_dir = os.path.dirname(os.path.abspath(__file__))
