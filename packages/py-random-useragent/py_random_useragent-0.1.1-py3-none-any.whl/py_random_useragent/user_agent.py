# -*- coding: utf-8 -*-
# @Author: Suvorinov Oleg <olegsuvorinov@me.com>
# @Date:   2023-02-28 10:01:30
# @Last Modified by:   Oleg Suvorinov
# @Last Modified time: 2023-06-30 09:33:56

import os
import random

import requests
from lxml import html


class UserAgent(object):
    """docstring for UserAgent"""

    def __init__(self):
        super(UserAgent, self).__init__()

        self._u_agents = []

    def __most_common_user_agents(self):
        """Забираем содержмое страницы с наиболее популярными
        браузерами"""

        url = ("https://webcache.googleusercontent.com/"
               "search?q=cache:FxxmQW9XrRcJ:https://techblog.willshouse.com/"
               "2012/01/03/most-common-user-agents/+&cd=4&hl=en&ct=clnk&gl=us")
        xpath = '//*[@id="post-2229"]/div[2]/textarea[1]'

        try:
            r = requests.get(url)
            xml = html.fromstring(r.content)
            elem = xml.xpath(xpath)[0]
        except Exception:
            pass
        else:
            cur_dir, _ = os.path.split(__file__)
            ua_file = os.path.join(cur_dir, 'useragents.txt')
            with open(ua_file, 'w') as f:
                f.write(elem.text_content())

    def update_ua(self):
        """Обновляем список наиболее популярных
        браузеров"""

        self.__most_common_user_agents()

    def get_ua(self) -> str:
        """Рандомно забираем User Agents из файла
        useragents.txt
        """

        _u_a = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0' # noqa
        if self._u_agents:
            return random.choice(self._u_agents)

        try:
            cur_dir, _ = os.path.split(__file__)
            ua_file = os.path.join(cur_dir, 'useragents.txt')
            with open(ua_file) as f:
                for line in f:
                    self._u_agents.append(line.strip())
        except Exception:
            return _u_a
        else:
            return random.choice(self._u_agents)
