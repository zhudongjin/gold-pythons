"""
系统健康检查服务
"""
import requests
from utils.resp_data import *


def down_verify_image(verify_image_url, storage_image_path):
    """下载验证码图片，并返回其cookies"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"}
    response = requests.get(verify_image_url, headers=headers, stream=True)
    with open(storage_image_path, 'wb') as fd:
        for chunk in response.iter_content(128):
            fd.write(chunk)

    # 返回cookies，下个请求使用
    # return response.cookies


if __name__ == '__main__':
    down_verify_image('https://store.10044.cn/common/img2sms/getImgVerifyCode.do?time=123', 'verify.png')
