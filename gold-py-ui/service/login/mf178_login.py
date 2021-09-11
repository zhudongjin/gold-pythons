"""
话费宝自动操作服务
"""
import datetime
import requests
from requests.cookies import RequestsCookieJar
# 爬虫网页解析
from lxml import html
from bs4 import BeautifulSoup

from utils.logger_factory import LoggerFactory
from utils.path import Path
from service.login.baidu_ocr import BaiduOcr

# 全局日志单例
LOGGER = LoggerFactory.get_logger()

urls = {
    # 图片验证码地址
    "VERIFY_IMAGE_URL": "http://www.mf178.cn/mobile/index/captcha?time=123",
    # 密码登录地址
    "LOGIN_URL": "http://www.mf178.cn/mobile/index/login",
    # 获取实名地址
    "GET_CN_NAME_URL": "http://www.mf178.cn/mobile/user/index",
    # 获取可提现金额地址
    "GET_DRAWOUT_URL": "http://www.mf178.cn/mobile/flow/withdraw?type=3",
    # 移动端提交提现操作地址
    "MOBILE_SUBMIT_DRAWOUT_URL": "http://www.mf178.cn/mobile/flow/do_withdraw",
    # PC提交提现操作地址
    "PC_SUBMIT_DRAWOUT_URL": "http://www.mf178.cn/customer/flow/withdraw",
    # 查询订单列表
    'RECHARGE_ORDER_LIST_URL': 'http://www.mf178.cn/customer/user/orders?status=0&ship=-1&ispayed=0&channel=0&channel_account=0&mobile=&sdate={}&edate='
}


class MfLogin(object):
    """话费宝自动登录"""

    def __init__(self, userName, password):
        self.userName = userName
        self.password = password
        self.cookies = None
        self.session_key = "ci_session"
        self.session_id = None
        self.domain = "www.mf.cn"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/45.0.2454.101 Safari/537.36"}
        self.storage_image_path = Path.get_app_ab_path() + "/cache/verify/mf178_verify_{}.png".format(self.userName)
        # 用户相关信息
        self.is_login = False
        self.cn_name = None
        self.draw_out_amt = 0
        self.plats = ""

    def login(self):
        """话费宝自动登录"""
        # 1、下载图片验证码
        self.down_verify_image()
        # 2、识别并登录
        self.orc_and_login()
        return self.is_login

    def orc_and_login(self):
        """识别并登录"""
        # 2、识别图片验证码（百度OCR）
        time.sleep(1)  # QPS 间隔
        baidu_ocr = BaiduOcr()
        verify_code = baidu_ocr.ocr(self.storage_image_path)
        # 2、识别图片验证码（本地OCR）
        # local_ocr = OsheepOcr()
        # verify_code = local_ocr.ocr(self.storage_image_path)
        verify_code = verify_code.replace(" ", "")
        LOGGER.info("[验证码OCR] - 识别图片验证码出现异常，识别结果为[{}]".format(verify_code))
        # 验证码长度不等于4位，重新来
        if len(verify_code) != 4:
            # time.sleep(0.2)
            self.login()
            return

        # 3、执行自动登录操作
        self.do_login(verify_code.replace(" ", ""))

    def down_verify_image(self):
        """下载验证码图片，并记录其cookies"""
        response = None
        try:
            response = requests.get(urls["VERIFY_IMAGE_URL"], headers=self.headers, stream=True)
        except Exception as e:
            LOGGER.error("获取蜜蜂登录图形验证码失败 -> {}", e)
            # 重试
            self.down_verify_image()
        # 记录cookies
        self.cookies = response.cookies
        self.session_id = self.cookies.__getitem__(self.session_key)
        # 写入到本地文件
        with open(self.storage_image_path, 'wb') as fd:
            for chunk in response.iter_content(128):
                fd.write(chunk)

    def get_login_params(self, image_code):
        data = {
            "username": self.userName,
            "password": self.password,
            "vcode": image_code
        }
        return data

    def do_login(self, image_code):
        """进行登录"""
        data = self.get_login_params(image_code)
        # LOGGER.info("LoginData  = {}", data)
        response = None
        try:
            response = requests.post(urls["LOGIN_URL"], data=data, headers=self.headers, cookies=self.cookies,
                          stream=True)
        except Exception as e:
            LOGGER.error("获取蜜蜂登录图形验证码失败 -> {}", e)
            # 重试
            self.do_login(image_code)
        # 尝试获取实名进行判断是否登录成功
        # self.set_login_cookies(self.session_id)
        if response.status_code == 200:
            self.is_login = True
            LOGGER.info("[响应Refresh] - [{}]".format(response.headers['Refresh']))
            LOGGER.info("[登录成功] - [{}] - 响应状态码：{}".format(self.userName, response.status_code))
        else:
            self.is_login = False
            LOGGER.info("[响应headers] - [{}]".format(response.headers))
            LOGGER.info("[登录失败] - [{}] - 响应状态码：{}".format(self.userName, response.status_code))

    def set_login_cookies(self, session_id=None):
        """设置session_id，自动登录"""
        self.cookies = RequestsCookieJar()
        self.cookies.set(self.session_key, session_id, domain=self.domain)
        # 设置已登录
        self.session_id = session_id
        self.is_login = True
        # 尝试获取实名信息，确认是否已登录
        cn_name = self.get_cn_name()
        if cn_name is None or len(cn_name) == 0:
            self.is_login = False
            LOGGER.info("[登录失败] - [{}]".format(self.userName))
        else:
            LOGGER.info("[登录成功] - [{}]".format(self.userName))
            pass

    def get_soup(self, url):
        """获取解析器"""
        # 获取页面内容
        html_doc = requests.get(url, cookies=self.cookies).content.decode()
        soup = BeautifulSoup(html_doc, "html.parser")  # 声明BeautifulSoup对象
        return soup

    def get_cn_name(self):
        """获取实名信息，需在登录成功后操作"""
        if self.is_login is False:
            return "NOT_LOGIN"

        LOGGER.info("[获取实名信息] - [{}]".format(self.userName))
        page_html = requests.get(urls["GET_CN_NAME_URL"], cookies=self.cookies).content.decode()
        element = html.etree.HTML(page_html)
        # 使用XPATH获取数据节点
        try:
            self.cn_name = element.xpath('//td//text()')[5]
        except Exception as e:
            # LOGGER.info(e)
            self.cn_name = None
            pass
        return self.cn_name
        return None

    def get_recharge_order_count(self):
        """获取充值成功笔数"""
        if self.is_login is False:
            return "NOT_LOGIN"

        LOGGER.info("[获取今日成功单数] - [{}]".format(self.userName))
        # 获取页面内容
        soup = self.get_soup(urls["RECHARGE_ORDER_LIST_URL"].format(datetime.datetime.now().strftime("%Y-%m-%d")))
        strong_doc = soup.select('.page-header strong')[0].get_text()
        order_num = strong_doc.split(' ', 2)[1].split('：')[1]
        return order_num

    def get_drawout_amt(self):
        """获取可提现信息，需在登录成功后操作"""
        if self.is_login is False:
            return "NOT_LOGIN"

        LOGGER.info("[获取可提现余额] - [{}]".format(self.userName))
        # 获取页面内容
        page_html = requests.get(urls["GET_DRAWOUT_URL"], cookies=self.cookies).content.decode()
        element = html.etree.HTML(page_html)
        # 使用XPATH获取数据节点
        amt_elements = element.xpath('//*[@id="stat_payment"]//text()')
        self.draw_out_amt = 0
        if len(amt_elements) > 0:
            self.draw_out_amt = float(amt_elements[0].replace(' ', '')[2:])
            self.plats = element.xpath('//*[@name="plats[]"]//@value')[0]
        return self.draw_out_amt

    def do_withdraw(self, min_amt=0.01, pay_type=100):
        """进行触发提现"""
        # pay_amt = self.get_drawout_amt()
        pay_amt = 100
        # 未登录的情况
        if pay_amt == "NOT_LOGIN":
            return None

        if pay_amt >= min_amt:
            # 支付宝提现
            response = self.do_alipay_withdraw()
            # LOGGER.info("自动提现响应码：{}".format(response.status_code))
            if response.status_code == 200:
                LOGGER.info("[申请提现成功] - [{}]".format(self.userName))
                return pay_amt
            else:
                return None
        else:
            return None

    def do_alipay_withdraw(self):
        """支付宝提现"""
        params = dict()
        params["type"] = 3
        params["deposit"] = 0
        params["card_type_3"] = 3
        params["card_type_2"] = 2
        params["card_type_99"] = 99
        params["card_type"] = 3
        params["plats[]"] = self.plats
        response = requests.post(urls["MOBILE_SUBMIT_DRAWOUT_URL"],
                                 data=params,
                                 headers=self.headers,
                                 cookies=self.cookies,
                                 stream=True)
        return response

    def do_bankcard_withdraw(self, amount):
        """银行卡提现"""
        params = dict()
        params["type"] = 3
        params["deposit"] = 0
        params["amount"] = amount
        params["card_type"] = 2
        params["bank_flag_2"] = "6214836559289869"
        params["bank_flag_4"] = "6214836559289869"
        params["plats[]"] = self.plats
        response = requests.post(urls["PC_SUBMIT_DRAWOUT_URL"],
                                 data=params,
                                 headers=self.headers,
                                 cookies=self.cookies,
                                 stream=True)
        return response


import time

if __name__ == '__main__':
    # for i in range(100):
    # LOGGER.info("-------------- 第{}次操作 --------------".format(i))
    mf = MfLogin('18665961760', 'ouyang@123')
    # 执行登录流程
    # mf.login()
    session_id = "avneluulucffjj9av0bdcgoi4f913anv"
    mf.set_login_cookies(session_id)
    print("是否登录成功 => {}".format(mf.is_login))
    print("用户真实姓名 => {}".format(mf.get_cn_name()))
    print("获取今日订单数 => {}".format(mf.get_recharge_order_count()))
    print("可转出的金额 => {}".format(mf.get_drawout_amt()))
    # print("进行触发提现 => {}".format(mf.do_withdraw()))

    time.sleep(6)
