import json
from utils.path import Path


class JsonStorage:
    # JSON数据存储与读取

    @staticmethod
    def save(obj, file_path):
        """保存文件数据"""
        file_path = Path.get_app_ab_path() + file_path
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(obj))

    @staticmethod
    def load(file_path):
        """读取文件数据"""
        file_path = Path.get_app_ab_path() + file_path
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.loads(f.read())

        # 空数据返回
        return None


if __name__ == '__main__':
    file_path = "data.json"
    data = dict()
    data['name'] = "欧阳顺德"
    data['age'] = "19"
    JsonStorage.save(data, file_path)
    print(JsonStorage.load(file_path))
