import requests


class RequestHelper(object):
    """请求帮助类"""

    @staticmethod
    def get_dispatcher(api_url, params, msg_call_back, headers=None):
        """GET请求调度器"""
        msg_call_back("-" * 30)
        log = """请求链接：{} \n请求头：{} \n请求主体：{}""".format(api_url, headers, params)
        msg_call_back(log)
        result = requests.post(url=api_url, params=params, headers=headers).content.decode()
        msg_call_back("-" * 30)
        log = """响应报文：{}""".format(result)
        msg_call_back(log)
        return result

    @staticmethod
    def post_dispatcher(api_url, params, msg_call_back, headers=None):
        """POST请求调度器"""
        msg_call_back("-" * 30)
        log = """请求链接：{} \n请求头：{} \n请求主体：{}""".format(api_url, headers, params)
        msg_call_back(log)
        result = requests.post(url=api_url, data=params, headers=headers).content.decode()
        msg_call_back("-" * 30)
        log = """响应报文：{}""".format(result)
        msg_call_back(log)
        return result
