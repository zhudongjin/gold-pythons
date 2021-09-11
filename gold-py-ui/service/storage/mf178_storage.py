from utils.json_storage import JsonStorage
from utils.config import conf

CACHE_FILE_PATH = "/conf/mf.json"


class MfCache:
    # 蜜蜂178JSON数据存储与读取

    @staticmethod
    def save(obj):
        """保存文件数据"""
        JsonStorage.save(obj, CACHE_FILE_PATH)

    @staticmethod
    def load():
        """读取文件数据"""
        return JsonStorage.load(CACHE_FILE_PATH)


if __name__ == '__main__':
    user_list = list()
    user = dict()
    user['name'] = "欧阳顺德"
    user['age'] = "19"
    user_list.append(user)
    MfCache.save(user_list)
    print(conf['APP_PROJECT_NAME'])
    print(MfCache.load())
