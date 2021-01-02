#coding: utf8
from datetime import datetime
from dn_helper import DNHelper
from http_helper import HttpHelper
import requests
import json
import time
import codecs
start = 320776
history_reader = open("history_data.txt", "r")
history_writer = codecs.open("history_data.txt", "a", 'utf8')
history_datas = filter(lambda x: x, map(lambda x:x.strip('\n').split('\t'), history_reader.readlines()))
history_titles = [x[0] for x in history_datas]
history_links = [x[1] for x in history_datas]
dn_helper = DNHelper()
http_helper = HttpHelper()
notice_template = u"新公告：%s\n 链接：%s"


debug = False
first_run = True
if not debug and not first_run:
    group_ids = [655514756, 584050850]
else:
    group_ids = [
        655514756
    ]

def calc_hammer_distance(s1, s2):
    dp = [[0x3f3f3f3f for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]
    dp[0][0] = 0
    for i in range(len(s1) + 1):
        for j in range(len(s2) + 1):
            if i < len(s1):
                dp[i + 1][j] = min(dp[i + 1][j], dp[i][j] + 1)
            if j < len(s2):
                dp[i][j + 1] = min(dp[i][j + 1], dp[i][j] + 1)
            if i < len(s1) and j < len(s2) and s1[i] == s2[j]:
                dp[i + 1][j + 1] = min(dp[i + 1][j + 1], dp[i][j])
    return dp[len(s1)][len(s2)]

def check_title_link_dedup(data):
    if data['link'] in history_links:
        return True
    for title in history_titles:
        try:
            utf8_title = title.decode('utf8')
        except:
            utf8_title = title
        if calc_hammer_distance(data['title'], utf8_title) < 2:
            return True
    return False

def get_group_ids():
    if not debug and not first_run:
        group_ids = [655514756, 584050850]
    else:
        group_ids = [
            655514756
        ]
    return group_ids

def process():
    global history_titles, history_links, start, first_run
    while True:
        for i in range(start, start + 200):
            data = dn_helper.get_news_content(i)
            if not data or not data.get('title') or check_title_link_dedup(data):
                continue
            start = i
            history_writer.write(u'%s\t%s\n' % (data['title'], data['link']))
            history_titles.append(data['title'])
            history_links.append(data['link'])
            print i, data['title'], data['link']
            http_helper.send_group_msgs(get_group_ids(), notice_template % (data['title'], data['link']))
            time.sleep(0.2)
        print datetime.now(), 'process done'
        first_run = False
        time.sleep(40)

def test():
    print calc_hammer_distance(
        u'【专栏】大神进阶之路 | 巧用技能龙玉连招  让御灵输出爆炸',
        u'【专栏】大神进阶之路 | 巧用技能龙玉 让御灵输出爆炸'
    )

if __name__ == '__main__':
    # test()
    process()
    pass