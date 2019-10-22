# @Time : 2019/10/22 11:26
# @Author : GKL
# FileName : spider.py
# Software : PyCharm

import re
import time

import gevent
from gevent import monkey; monkey.patch_all()
import requests


class Spider(object):
    """
    通过协程获取斗图啦表情包
    """
    def __init__(self):
        # self.url = 'http://www.doutula.com/article/list/?page=1'
        self.page = 1

    @classmethod
    def get_url(cls, url):
        """
        获取图片地址
        :param url:
        :return:
        """
        resp = requests.get(url).text
        url_list = re.findall(r'data-original="(.*?)"', resp)
        name_list = re.findall(r'alt="(.*?)"', resp)
        return url_list, name_list

    @classmethod
    def download(cls, url_list, name_list):
        """
        图片下载并保存到本地
        :param url_list:
        :param name_list:
        :return:
        """
        for url, name in zip(url_list, name_list):

            # 获取图片后缀名
            suffix = url.split('.')[-1]

            # 拼接图片保存到本地的名字
            name = '{}.{}'.format(name, suffix) if name else ' .{}'.format(suffix)
            print(name)

            # 获取图片二进制数据
            response = requests.get(url).content

            # 异常捕获, 舍去命名不规范的图片
            try:
                with open('./img/{}'.format(name), 'wb') as f:
                    f.write(response)
            except OSError as e:
                print(e)


    def run(self, url):
        """
        该方法用于调用
        :param url:
        :return:
        """
        print(url)
        url_list, name_list = self.get_url(url)
        self.download(url_list, name_list)
        self.page += 1
        next_url = 'http://www.doutula.com/article/list/?page={}'.format(self.page)

        # 设置延时, 防止访问过快封ip
        time.sleep(5)
        self.run(next_url)


if __name__ == '__main__':
    s = Spider()
    # s.run('http://www.doutula.com/article/list/?page=1')
    # 协程调用方式
    gevent.joinall([gevent.spawn(s.run, 'http://www.doutula.com/article/list/?page={}'.format(i)) for i in range(5)])
