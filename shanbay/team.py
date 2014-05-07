#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import datetime
import re

from bs4 import BeautifulSoup


class Team(object):
    """小组管理"""

    def __init__(self, shanbay, team_url):
        self.shanbay = shanbay
        self._request = shanbay._request
        self.request = shanbay.request
        self.team_url = team_url
        self.team_id = re.findall(r'/(\d+)/?$', team_url)[0]

    def info(self):
        """小组信息

        :return: 小组信息
        :rtype: dict

        返回值示例::

          return {
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
        html = self.request(self.team_url, 'get').text
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
        rate = float(re.findall(r'(\d+\.?\d+)%$', _str)[0])
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
