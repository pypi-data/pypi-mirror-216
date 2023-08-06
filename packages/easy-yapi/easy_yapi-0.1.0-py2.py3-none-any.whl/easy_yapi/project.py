"""
!/usr/bin/env python
# -*- coding: utf-8 -*-
@Time    : 2023/6/29 17:27
@Author  : 派大星
@Site    :
@File    : project.py
@Software: PyCharm
@desc:
"""
import copy
from .base_api import BaseApi


class ProjectMixIn(BaseApi):
    """项目相关接口"""

    def check_project_name(self, project_name, group_id):
        """判断分组名称是否重复"""
        res = self.get(f'/api/project/check_project_name?name={project_name}&group_id={group_id}')
        return res

    def add_project(self, name, group_id='11', color='blue', icon='unlock'):
        """添加项目分组"""
        json_data = {"name": name, "group_id": group_id, "icon": icon, "color": color,
                     "project_type": "private"}

        res = self.post('/api/project/add', json=json_data)
        return res

    def copy_project(self, new_project_name, old_project_data):
        """复制项目"""
        old_project_name = old_project_data.get('name', '')
        old_project_data.update({'preName': old_project_name})
        json_data = copy.deepcopy(old_project_data)
        json_data['name'] = new_project_name
        res = self.post('/api/project/copy', json=json_data)
        return res

    def get_project_list(self, group_id='11', page=1, limit=10):
        """获取项目列表"""
        res = self.get(f'/api/project/list?group_id={group_id}&page={page}&limit={limit}')
        return res

    def get_project_id(self, _id):
        """获取项目"""
        res = self.get(f'/api/project/get?id={_id}')
        return res

    def add_project_member(self, _id, member_uids=None, role='dev'):
        """添加项目成员"""
        if member_uids is None:
            member_uids = []
        res = self.post('/api/project/add_member', json={"id": _id, "member_uids": member_uids, "role": role})
        return res

    def del_project_member(self, _id, member_uid):
        """删除项目成员"""
        res = self.post('/api/project/del_member', json={"id": _id, "member_uid": member_uid})
        return res

    def get_project_member_list(self, _id):
        """获取项目成员列表"""
        res = self.get(f'/api/project/get_member_list?id={_id}')
        return res

    def del_project(self, _id):
        """删除项目"""
        res = self.post('/api/project/del', json={"id": _id})
        return res

    def change_member_role(self, _id, member_uid, role='dev'):
        """修改项目成员角色"""
        res = self.post('/api/project/change_member_role', json={"id": _id, "member_uid": member_uid, "role": role})
        return res

    def change_member_email_notice(self, _id, member_uid, is_email_notice=False):
        """修改项目成员邮件通知"""
        res = self.post('/api/project/change_member_email_notice',
                        json={"id": _id, "member_uid": member_uid, "is_email_notice": is_email_notice})
        return res

    def upset_project(self, _id, color='blue', icon='unlock'):
        """项目头像设置"""
        json_data = {"id": _id, "icon": icon, "color": color}
        res = self.post('/api/project/upset', json=json_data)
        return res

    def update_project(self, project_data):
        """编辑项目"""
        res = self.post('/api/project/upset', json=project_data)
        return res

    def up_project_env(self, project_id, env_data):
        """编辑项目环境配置"""
        res = self.post('/api/project/up_env', json={"id": project_id, "env": env_data})
        return res

    def get_project_env(self, project_id):
        """编辑项目环境配置"""
        res = self.get(f'/api/project/get_env?project_id={project_id}')
        return res

    def up_project_tag(self, project_id, up_tag):
        """编辑项目环境配置"""
        res = self.post('/api/project/up_tag', json={"id": project_id, "tag": up_tag})
        return res

    def get_project_token(self, project_id):
        """获取项目token配置"""
        res = self.get(f'/api/project/token?project_id={project_id}')
        return res

    def update_project_token(self, project_id):
        """更新项目token"""
        res = self.get(f'/api/project/update_token?project_id={project_id}')
        return res

    def search_project(self, q):
        """模糊搜索项目名称或者分组名称或接口名称"""
        res = self.get(f'/api/project/search?q={q}')
        return res
