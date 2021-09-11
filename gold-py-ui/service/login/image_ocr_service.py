#!/usr/bin/env python
# coding:utf-8
# 适用于python 3.x 版本 ，2.x版本将 print 后面的括号去掉就可以了

import requests
import os

"""
图形验证码识别功能
"""


class KSClient(object):

    def __init__(self):
        self.username = ''

        self.Token = ''
        # 服务公共Header
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }
        # 服务主机
        self.host = 'http://api.95man.com:8888/'

    # 获取taken
    def GetTaken(self, username, passord):
        brtn = False
        r = requests.get(
            self.host + '/api/Http/UserTaken?user=' + username + '&pwd=' + passord + '&isref=0',
            headers=self.headers)
        arrstr = r.text.split('|')
        if (arrstr[0] == '1'):
            self.username = username
            self.Token = arrstr[1]
            brtn = True
        return brtn

    # 识别图片
    def PostPic(self, filepath, codetype):
        """
        imbyte: 图片字节
        imgtype: 类型 1为通用类型 更多精准类型请参考 http://fast.net885.com/auth/main.html
        """
        strRtn = ''
        imbyte = open(filepath, 'rb').read()
        filename = os.path.basename(filepath)

        files = {'imgfile': (filename, imbyte)}
        r = requests.post(
            self.host + '/api/Http/Recog?Taken=' + self.Token + '&imgtype=' + str(codetype) + '&len=0',
            files=files, headers=self.headers)
        arrstr = r.text.split('|')
        # 返回格式：识别ID|识别结果|用户余额
        if (int(arrstr[0]) > 0):
            strRtn = arrstr[1]

        return strRtn

    # 识别报错
    def ReportError(self, imageid):
        """
        imageid:报错题目的图片ID
        """
        r = requests.get(self.host + '/api/Http/ReportErr?Taken=' + self.Token + '&ImgID=' + str(imageid),
                         headers=self.headers)
        arrstr = r.text.split('|')
        if (arrstr[0] == '1'):
            print('报错成功！')
        else:
            print('报错失败，错误信息：' + arrstr[1])


if __name__ == '__main__':
    Ks95man = KSClient()
    if Ks95man.GetTaken('Osheep', 'ouyang123'):
        # 获取成功,taken获取一次就可以了，taken 生成后如果不用参数"isref=1"刷新，就一直不会变。如果写死在您的软件中，就要慎用"isref=1"，否则您之前写死的软件都要改taken。
        # 开始识别
        # 获取文件二进制流
        image_path = 'verify.png';
        print('识别结果：' + Ks95man.PostPic(image_path, 1))
        # 识别报错
        Ks95man.ReportError(88)
