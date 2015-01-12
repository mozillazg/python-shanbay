#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import datetime
import logging
import re
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Team(object):
    """小组管理

    :param shanbay: :class:`~shanbay.Shanbay` 实例对象
    :param team_url: 小组首页 URL

    ::

     >>> from shanbay import Shanbay, Team
     >>> s = Shanbay('username', 'password')
     >>> s.login()
     >>> t = Team(s, 'http://www.shanbay.com/team/1234/')
    """

    def __init__(self, shanbay, team_url):
        self.shanbay = shanbay
        self._request = shanbay._request
        self.request = shanbay.request
        self.team_url = team_url
        self.team_id = self.get_url_id(team_url)
        self.dismiss_url = 'http://www.shanbay.com/team/manage/'

    def get_url_id(self, url):
        return re.findall(r'/(\d+)/?$', url)[0]

    def info(self):
        """小组信息

        :return: 小组信息
        :rtype: dict

        返回值示例 ::

          {
              'title': u'title',  # 标题
              'leader': u'leader',  # 组长
              'date_created': datetime.datetime(2013, 10, 6, 0, 0),  # 创建日期
              'rank': 1000,  # 排名
              'number': 10,  # 当前成员数
              'max_number': 20,  # 最大成员数
              'rate': 1.112,  # 打卡率
              'points': 23  # 总成长值
          }
        """
        html = self.request(self.team_url).text
        soup = BeautifulSoup(html)
        team_header = soup.find_all(class_='team-header')[0]

        # 标题
        title = team_header.find_all(class_='title')[0].text.strip()
        # 组长
        leader = team_header.find_all(class_='leader'
                                      )[0].find_all('a')[0].text.strip()
        # 创建时间
        date_str = team_header.find_all(class_='date')[0].text.strip()
        date_created = datetime.datetime.strptime(date_str, '%Y/%m/%d')
        # 排名
        team_stat = soup.find_all(class_='team-stat')[0]
        _str = team_stat.find_all(class_='rank')[0].text.strip()
        rank = int(re.findall(r'\d+$', _str)[0])
        # 成员数
        _str = team_stat.find_all(class_='size')[0].text.strip()
        number, max_number = map(int, re.findall(r'(\d+)/(\d+)$', _str)[0])
        # 打卡率
        _str = team_stat.find_all(class_='rate')[0].text.strip()
        rate = float(re.findall(r'(\d+\.?(?:\d+)?)%$', _str)[0])
        # 总成长值
        _str = team_stat.find_all(class_='points')[0].text.strip()
        points = int(re.findall(r'\d+$', _str)[0])

        return {
            'title': title,
            'leader': leader,
            'date_created': date_created,
            'rank': rank,
            'number': number,
            'max_number': max_number,
            'rate': rate,
            'points': points
        }

    def update_limit(self, days, kind=2, condition='>='):
        """更新成员加入条件

        :rtype: bool
        """
        url = 'http://www.shanbay.com/team/setqualification/%s' % self.team_id
        data = {
            'kind': kind,
            'condition': condition,
            'value': days,
            'team': self.team_id,
            'csrfmiddlewaretoken': self._request.cookies.get('csrftoken')
        }
        r = self.request(url, 'post', data=data)
        return r.url == 'http://www.shanbay.com/referral/invite/?kind=team'

    def members(self):
        """获取小组所有成员的信息列表"""
        all_members = []
        for page in range(1, self.max_page() + 1):
            all_members.extend(self.single_page_members(page))
        return all_members

    def max_page(self):
        """获取小组成员管理页面的最大页数"""
        html = self.request(self.dismiss_url).text
        soup = BeautifulSoup(html)
        # 分页所在 div
        try:
            pagination = soup.find_all(class_='pagination')[0]
        except IndexError as e:
            logger.exception(e)
            return 1
        pages = pagination.find_all('li')
        return int(pages[-2].text) if pages else 1

    def single_page_members(self, page_number=1):
        """获取单个页面内的小组成员信息

        :param page_number: 页码
        :return: 包含小组成员信息的列表

        返回值示例: ::

            [{
                'id': 123,                  # member_id
                'username': 'jim',          # username
                'nickname': 'Jim',          # 昵称
                'role': u'小组长',          # 身份
                'points': 1234,             # 贡献成长值
                'days': 100,                # 组龄
                'rate': 99.9,               # 打卡率
                'checked_yesterday': True,  # 昨天是否打卡
                'checked': False,           # 今天是否打卡
            }, {
                # ...
            }]


        """
        url = '%s?page=%s' % (self.dismiss_url, page_number)
        html = self.request(url).text
        soup = BeautifulSoup(html)
        members_html = soup.find(id='members')
        if not members_html:
            return []

        def get_tag_string(html, class_, tag='td', n=0):
            """获取单个 tag 的文本数据"""
            return html.find_all(tag, class_=class_)[n].get_text().strip()

        members = []
        # 获取成员信息
        for member_html in members_html.find_all('tr', class_='member'):
            _id = member_html.attrs['data-id']
            try:
                user_url = member_html.find_all('td', class_='user'
                                                )[0].find('a').attrs['href']
                username = self.get_username('http://www.shanbay.com'
                                             + user_url)
            except Exception as e:
                logger.exception(e)
                username = ''
            try:
                nickname = get_tag_string(member_html, 'nickname', 'a')
            except Exception as e:
                logger.exception(e)
                nickname = username
            try:
                role = member_html.find_all('td', class_='user'
                                            )[0].find_all('span', class_='label'
                                                          )[0].get_text().strip()
            except IndexError:
                role = ''
            except Exception as e:
                logger.exception(e)
                role = ''

            member = {
                'id': int(_id),
                'username': username,
                # 昵称
                'nickname': nickname,
                # 身份
                'role': role,
                # 贡献成长值
                'points': int(get_tag_string(member_html, 'points')),
                # 组龄
                'days': int(get_tag_string(member_html, 'days')),
                # 打卡率
                'rate': float(get_tag_string(member_html, 'rate'
                                             ).split('%')[0]),
                # 昨天是否打卡
                'checked_yesterday': get_tag_string(member_html, 'checked'
                                                    ) != '未打卡',
                # 今天是否打卡
                'checked': get_tag_string(member_html, 'checked',
                                          n=1) != '未打卡',
            }
            members.append(member)
        return members

    def get_username(self, url):
        html = self.request(url).text
        soup = BeautifulSoup(html)
        t = soup.find_all(class_='page-header')[0].find_all('h2')[0].text.strip()
        return t.strip(u'的日记').strip()

    def dismiss(self, member_ids):
        """踢人. 注意别把自己给踢了.

        :param member_ids: 组员 ids
        :return: bool
        """
        url = 'http://www.shanbay.com/api/v1/team/member/'
        data = {
            'action': 'dispel',
        }
        if isinstance(member_ids, (list, tuple)):
            data['ids'] = ','.join(map(str, member_ids))
        else:
            data['ids'] = member_ids
        r = self.request(url, 'put', data=data)
        try:
            return r.json()['msg'] == "SUCCESS"
        except Exception as e:
            logger.exception(e)
            return False

    def forum_id(self):
        """小组发帖要用的 forum_id"""
        html = self.request(self.team_url).text
        soup = BeautifulSoup(html)
        return soup.find(id='forum_id').attrs['value']

    def new_topic(self, title, content):
        """小组发贴

        :return: 帖子 id 或 ``None``
        """
        data = {
            'title': title,
            'body': content,
            'csrfmiddlewaretoken': self._request.cookies.get('csrftoken')
        }
        url = 'http://www.shanbay.com/api/v1/forum/%s/thread/' % self.forum_id()
        r = self.request(url, 'post', data=data)
        j = r.json()
        if j['status_code'] == 0:
            return j['data']['thread']['id']

    def reply_topic(self, topic_id, content):
        """小组回帖

        :return: 帖子 id 或 ``None``
        """
        data = {
            'body': content,
            'csrfmiddlewaretoken': self._request.cookies.get('csrftoken')
        }
        url = 'http://www.shanbay.com/api/v1/forum/thread/%s/post/' % topic_id
        r = self.request(url, 'post', data=data)
        j = r.json()
        if j['status_code'] == 0:
            return j['data']['thread']['id']
