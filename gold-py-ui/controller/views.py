import time
from threading import Thread
from flask import request, Response, jsonify
from utils.logger_factory import LoggerFactory
from service.storage.mf178_storage import MfCache
from service.login.mf178_login import MfLogin
from utils.resp_data import RespData
from . import mf


class MfStore(object):
    def __init__(self):
        self.mf_user_list = None
        self.min_drawout_amt = 100
        self.op_type = 'query'
        self.fetch_mf_data_state = 'complate'

mf_store = MfStore()


@mf.route('/get_account_list', methods=['POST'])
def get_account_list():
    """获取账户列表"""
    # 读取数据
    mf_store.mf_user_list = MfCache.load()
    return Response(RespData.ok(mf_store.mf_user_list))


@mf.route('/get_fetch_state', methods=['POST'])
def get_fetch_state():
    """获取蜜蜂数据状态"""
    return Response(RespData.ok(mf_store.fetch_mf_data_state))


@mf.route('/delete_account', methods=['POST'])
def delete_account():
    """删除账户"""
    del mf_store.mf_user_list[request.json['index']]
    MfCache.save(mf_store.mf_user_list)
    return Response(RespData.ok())


@mf.route('/add_account', methods=['POST'])
def add_account():
    """添加账户"""
    user_name = request.json['userName']
    # 判断是否存在
    for item in mf_store.mf_user_list:
        if item['userName'] == user_name:
            return Response(RespData.fail('账号已存在，添加操作中断'))
    # 初始化账号信息
    user = dict()
    user['userName'] = user_name
    user['password'] = request.json['password']
    user['cnName'] = ""
    user['isLogin'] = False
    user['drawOutAmt'] = 0.00
    user['Cookie'] = ""
    user['orderCount'] = 0
    user['refreshTime'] = ""
    user['drawOutTime'] = ""
    mf_store.mf_user_list.append(user)
    MfCache.save(mf_store.mf_user_list)
    return Response(RespData.ok())


@mf.route('/mf_reload_acct', methods=['POST'])
def mf_reload_acct():
    """批量自动登录，并获取最新数据"""
    mf_store.op_type = 'query'
    mf_store.fetch_mf_data_state = 'fetch'
    tr = Thread(target=sync_exec_batch)
    tr.start()
    return Response(RespData.ok())


def mf_batch_drawout():
    """批量提现"""
    mf_store.op_type = 'drawout'
    mf_store.fetch_mf_data_state = 'fetch'
    tr = Thread(target=sync_exec_batch)
    tr.start()
    return Response(RespData.ok())


def sync_exec_batch():
    # 加载，不分发多个线程，因为百度账号OCR的QPS不够用
    for user in mf_store.mf_user_list:
        exec_user_item(user)
    # 完成获取蜜蜂数据
    mf_store.fetch_mf_data_state = 'complate'


def exec_user_item(user):
    """执行单个用户"""
    mf_login = MfLogin(user['userName'], user['password'])
    # 登录并获取用户信息
    do_login_fetch(user, mf_login)


def do_login_fetch(user, mf_login):
    """登录并提现"""
    # 自动登录
    is_login = mf_login.login()
    if is_login is True:
        fetch_user_info(user, mf_login)
    else:
        # 递归调用
        time.sleep(1)
        do_login_fetch(user, mf_login)


def fetch_user_info(user, mf_login):
    """登录后获取用户信息"""
    user['isLogin'] = True
    user['cnName'] = mf_login.get_cn_name()
    user['drawOutAmt'] = mf_login.get_drawout_amt()
    user['Cookie'] = mf_login.session_id
    user['orderCount'] = mf_login.get_recharge_order_count()
    user['refreshTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    # 判断是否为提现操作
    # 3、pay_type（支付宝：3，银行卡：2）
    if mf_store.op_type == 'drawout':
        mf_login.do_withdraw(min_amt=mf_store.min_drawout_amt, pay_type=3)
        # 提现成功
        user['drawOutTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # 持久化
    MfCache.save(mf_store.mf_user_list)
