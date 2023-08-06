"""
!/usr/bin/env python
# -*- coding: utf-8 -*-
@Time    : 2023/6/29 17:28
@Author  : 派大星
@Site    :
@File    : user.py
@Software: PyCharm
@desc:
"""
from .base_api import BaseApi


class UserMixIn(BaseApi):
    """用户相关接口"""
    def login(self, email, password):
        """登录"""
        res = self.post('/api/user/login', json={"email": email, "password": password})
        res.raise_for_status()
        _cookie = res.headers.get('Set-Cookie', '')
        self._session.cookies.update({"Cookie": _cookie})
        # self._session.headers.update({"Cookie": _cookie})

    def logout(self):
        """退出登录"""
        res = self.get('/api/user/logout')
        res.raise_for_status()
        return res

    def user_change_password(self, _id, new_password, old_password=''):
        """修改密码"""
        res = self.post('/api/user/change_password', json={"old_password": old_password, "password": new_password,
                                                           "uid": _id})
        res.raise_for_status()
        return res

    def user_reg(self, email, password, username):
        """注册"""
        res = self.post('/api/user/reg', json={"email": email, "password": password, "username": username})
        res.raise_for_status()
        return res

    def get_user(self, _id):
        """获取用户信息"""
        res = self.get(f'/api/user/find?id={_id}')
        res.raise_for_status()
        return res

    def get_user_list(self, page=1, limit=20):
        """获取用户列表"""
        res = self.get(f'/api/user/list?page={page}&limit={limit}')
        res.raise_for_status()
        return res

    def del_user(self, _id):
        """删除用户"""
        res = self.post('/api/user/del', json={"id": _id})
        res.raise_for_status()
        return res

    def get_user_status(self):
        """获取用户状态"""
        res = self.get('/api/user/status')
        res.raise_for_status()
        return res

    def search_user(self, q):
        """搜索用户"""
        res = self.get(f'/api/user/search?q={q}')
        res.raise_for_status()
        return res

    def update_user(self, _id, username):
        """更新用户"""
        res = self.post('/api/user/update', json={"uid": _id, "username": username})
        res.raise_for_status()
        return res
