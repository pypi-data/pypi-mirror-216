"""Main module."""
from pprint import pprint

from .user import UserMixIn
from .group import GroupMixIn
from .project import ProjectMixIn


class Yapi(UserMixIn, GroupMixIn, ProjectMixIn):
    """封装yapi接口"""

    def __init__(self, username, password):
        """登录"""
        super().__init__()
        _cookie = self.login(username, password)


if __name__ == '__main__':
    yapi = Yapi('nocoding@126.com', 'ymfe.org')

    cc = yapi.get_project_member_list(119)
    pprint(cc.json())

    # bb = yapi.logout()
    # print(bb.text)
