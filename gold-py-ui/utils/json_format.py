import json
import datetime
import decimal


class DataEncoder(json.JSONEncoder):
    """通用的数据特殊处理"""

    def default(self, obj):
        # 时间格式化
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        # 日期格式化
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        # 金额数字格式化
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        # 默认格式化
        else:
            return json.JSONEncoder.default(self, obj)
