#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from sonarqube.utils.rest_client import RestClient
from sonarqube.utils.config import API_USERS_SEARCH_ENDPOINT, API_USERS_GROUPS_ENDPOINT
from sonarqube.utils.common import GET


class SonarCloudUsers(RestClient):
    """
    SonarCloud users Operations
    """

    MAX_SEARCH_NUM = 200

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        super(SonarCloudUsers, self).__init__(**kwargs)

    def get(self, login):
        result = self.search_users(q=login)
        users = result.get("users", [])

        for user in users:
            if user["login"] == login:
                return user

    @GET(API_USERS_SEARCH_ENDPOINT)
    def search_users(self, q=None, p=None, ps=None):
        """
        Get a list of active users.

        :param q: Filter on login, name and email
        :param p: page number.
        :param ps: Page size. Must be greater than 0 and less or equal than 500
        :return:
        """

    @GET(API_USERS_GROUPS_ENDPOINT)
    def search_groups_user_belongs_to(
        self, login, organization, q=None, selected="selected", p=None, ps=None
    ):
        """
        Lists the groups a user belongs to.

        :param login:
        :param organization: organization key.
        :param q: Limit search to group names that contain the supplied string.
        :param selected: Depending on the value, show only selected items (selected=selected), deselected items
          (selected=deselected), or all items with their selection status (selected=all).Possible values are for:
            * all
            * deselected
            * selected
          default value is selected.
        :param p: page number.
        :param ps: Page size. Must be greater than 0 and less or equal than 500
        :return:
        """
