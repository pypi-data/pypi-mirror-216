"""
!/usr/bin/env python
# -*- coding: utf-8 -*-
@Time    : 2023/6/29 17:27
@Author  : 派大星
@Site    :
@File    : group.py
@Software: PyCharm
@desc:
"""
from .base_api import BaseApi


class GroupMixIn(BaseApi):
    """用户组相关接口"""

    def get_mygroup(self):
        """获取我的分组"""
        res = self.get('/api/group/get_mygroup')
        return res

    def group_list(self):
        """获取项目分组列表"""
        res = self.get('/api/group/list')
        return res

    def get_group(self, _id=11):
        """获取项目分组"""
        res = self.get(f'/api/group/get?id={_id}')
        return res

    def add_group(self, group_name, group_desc='', owner_uids=[]):
        """添加项目分组"""
        res = self.post('/api/group/add',
                        json={"group_name": group_name, "group_desc": group_desc, "owner_uids": owner_uids})
        return res

    def add_group_member(self, group_id, member_uids=[], role='dev', ):
        """添加项目分组成员"""
        res = self.post('/api/group/add_member', json={"id": group_id, "member_uids": member_uids, "role": role})
        return res

    def change_member_role(self, group_id, member_uid, role='dev'):
        """修改项目分组成员角色"""
        res = self.post('/api/group/change_member_role', json={"id": group_id, "member_uid": member_uid, "role": role})
        return res

    def get_member_list(self, group_id):
        """获取项目成员列表"""
        res = self.get(f'/api/group/get_member_list?id={group_id}')
        return res

    def del_group_member(self, group_id, member_uid):
        """删除项目成员"""
        res = self.post('/api/group/del_member', json={"id": group_id, "member_uid": member_uid})
        return res

    def del_group(self, group_id):
        """删除项目分组"""
        res = self.post('/api/group/del', json={"id": group_id})
        return res

    def update_group(self, group_name, group_desc, group_id, enable=False, name=''):
        """更新项目分组"""
        if name:
            json_data = {"group_name": group_name, "group_desc": group_desc,
                         "custom_field1": {"enable": enable}, "id": group_id}

        else:
            json_data = {"group_name": group_name, "group_desc": group_desc,
                         "custom_field1": {"enable": enable, "name": name}, "id": group_id}
        res = self.post('/api/group/up', json=json_data)
        return res
