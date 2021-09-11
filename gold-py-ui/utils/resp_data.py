import json
from utils.json_format import *
# 成功标识
RESP_CODE_OK = '0000'
# 成功消息
RESP_MESSAGE_OK = 'ok'
# 失败标识
RESP_CODE_FAIL = '9999'


class RespData(object):
    """数据响应主体"""

    @staticmethod
    def ok(data=None):
        resp = RespData(RESP_CODE_OK, RESP_MESSAGE_OK, data)
        return resp.json()

    @staticmethod
    def fail(message, data=None):
        resp = RespData(RESP_CODE_FAIL, message, data)
        return resp.json()

    def __init__(self, code, msg, data=None):
        self.code = code
        self.msg = msg
        self.data = data

    def __call__(self, *args, **kwargs):
        format_call = '[code={}],[msg={}],[data={}]'.format(self.code, self.msg, self.data)
        return format_call

    def json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, cls=DataEncoder, sort_keys=True, indent=2,
                          ensure_ascii=False)
