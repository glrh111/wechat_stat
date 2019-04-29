#! /usr/bin/env python
# coding: utf-8

"""
wxpy doc: https://wxpy.readthedocs.io/zh/latest/messages.html
"""

import csv
import os
import pytz
from datetime import datetime
import time
import unittest
import traceback
import pprint
import string

from wxpy import Bot, Message as WeMessage, Group, User, embed


class Datetimer(object):
    """deal with date time"""

    tz = pytz.timezone("Asia/Shanghai")
    FORMAT = "%Y%m%D"

    @classmethod
    def wechattime_to_timestamp(cls, wechat_str: str, FORMAT: str="%Y%m%D") -> int:
        """return timestamp_in_ms"""
        dt = datetime.strptime(wechat_str, FORMAT)
        local_dt = cls.tz.localize(dt)
        return int(time.mktime(local_dt.timetuple()) * 1000)

    @classmethod
    def timestamp_to_beijingtime(cls, timestamp_in_ms: int, FORMAT: str="%Y%m%D") -> str:
        local_dt = datetime.fromtimestamp(timestamp_in_ms/1000, cls.tz)
        return local_dt.strftime(FORMAT)


class Message(object):

    def __init__(self, t: str, group_id: str, group_name: str, from_id: str, from_nickname: str, content_type: str, content: str):
        self.t = t  # '2019-04-29 10:56:57.200536' [:10 is date by day]
        self.group_id = group_id
        self.group_name = group_name
        self.from_id = from_id
        self.from_nickname = from_nickname
        self.content_type = content_type
        self.content = content


class Collector(object):

    def __init__(self, msg: WeMessage):
        self.we_msg = msg

    @classmethod
    def do(cls, we_msg: WeMessage) -> Message:
        group: Group = we_msg.sender  #
        from_user: User = we_msg.member  # display_name
        print("group: ", group.nick_name, "from_user: ", from_user.nick_name)
        return Message(
            t= Datetimer.timestamp_to_beijingtime(1000 * we_msg.raw.get('CreateTime', 0), FORMAT="%Y-%m-%d %H:%M:%S"),
            group_id=group.puid,
            group_name=group.nick_name,
            from_id=from_user.puid,
            from_nickname=from_user.nick_name,
            content_type=we_msg.type,
            content=we_msg.text,
        )


class Stater(object):

    csv_header = ["time(Asia/Shanghai)", "group_id", "group_name", "from_id", "from_nickname", "content_type", "content"]

    def __init__(self, csv_filename: str, msg: Message):
        self.csv_filename = csv_filename
        self.msg = msg

    def stat(self):
        csv_lines = [
            [self.msg.t, self.msg.group_id, self.msg.group_name, self.msg.from_id, self.msg.from_nickname, self.msg.content_type, (self.msg.content or "").strip()]
        ]
        # choose from new file
        if not os.path.exists(self.csv_filename):
            csv_lines.insert(0, self.csv_header)
        with open(self.csv_filename, "a+", encoding='utf-8', newline='') as f:
            csv_writer = csv.writer(f, delimiter=",", quotechar='"')
            csv_writer.writerows(csv_lines)

    @classmethod
    def do(cls, msg: Message):
        dirname = "wechat_stat_data"
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        # filename format(per file every day): ./wechat_stat_data/wechat_stat_2017-04-29.csv
        print(msg.t, msg.t[:11])
        csv_filename = "./{}/wechat_stat_{}.csv".format(dirname, msg.t[:11])
        cls(csv_filename, msg).stat()


class TestDatetimer(unittest.TestCase):

    def setUp(self):
        # (timestamp, dts)
        # datetime(year=2019, month=4, day=29, hour=9, minute=49, second=33, tzinfo=tz)
        self.FORMAT = "%Y-%m-%d %H:%M:%S"
        self.dt_list = [
            (1556502573000, "2019-04-29 09:49:33"),
        ]

    def test_wechattime_to_timestamp(self):
        for ts, dts in self.dt_list:
            self.assertEqual(
                ts,
                Datetimer.wechattime_to_timestamp(dts, self.FORMAT)
            )

    def test_timestamp_to_beijingtime(self):
        for ts, dts in self.dt_list:
            self.assertEqual(
                dts,
                Datetimer.timestamp_to_beijingtime(ts, self.FORMAT)
            )

    def tearDown(self):
        del self.dt_list
        del self.FORMAT


def main():
    bot: Bot = Bot(cache_path=True)
    bot.enable_puid()

    @bot.register(Group)
    def deal_with_group_msg(we_msg: WeMessage):
        # Message.text 文本内容
        # Message.sender 群 Group 对象
        # Message.member 实际发送人 User 对象
        # Message.receive_time 本地接收时间(应该取 create_time 服务端发送时间)  '2019-04-29 10:56:57.200536'  [10]
        print(we_msg, "\ntext ", we_msg.text, "\nsender ", we_msg.sender, "\nmember", we_msg.member, "\nreceive",
              we_msg.receive_time)

        try:
            msg: Message = Collector.do(we_msg)
            pprint.pprint(msg)
            Stater.do(msg)
        except Exception:
            traceback.print_exc()

    embed()


if __name__ == '__main__':
    main()
