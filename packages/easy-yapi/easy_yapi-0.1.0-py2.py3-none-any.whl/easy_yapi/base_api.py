"""
!/usr/bin/env python
# -*- coding: utf-8 -*-
@Time    : 2023/6/29 17:25
@Author  : 派大星
@Site    :
@File    : base_api.py
@Software: PyCharm
@desc:
"""
import requests
import copy
import logging

logging.basicConfig(level=logging.INFO)


class BaseApi:
    # Create a session
    DEFAULT_OPTIONS = {
        "base_url": "http://82.156.152.141:3000",
        "headers": {
            "Content-Type": "application/json;charset=UTF-8"
        }
    }
    _options = copy.deepcopy(DEFAULT_OPTIONS)

    def __init__(self, base_url=_options["base_url"]):
        self._base_url = base_url
        self._session = requests.Session()
        self._session.headers.update(self._options["headers"])

    def get(self, url, **kwargs):
        """封装get请求"""
        if not url.startswith('http'):
            url = self._base_url + url
        logging.info(f"请求url:{url} 请求参数:{kwargs}")
        res = self._session.get(url, **kwargs)
        res.raise_for_status()
        return res

    def post(self, url, **kwargs):
        """封装post请求"""
        if not url.startswith('http'):
            url = self._base_url + url
        logging.info(f"请求url:{url} 请求参数:{kwargs}")
        return self._session.post(url, **kwargs)
