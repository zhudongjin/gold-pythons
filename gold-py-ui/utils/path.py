import os
from utils.config import conf


class Path:
    # 获取绝对路径
    @staticmethod
    def get_root_path(current_file_path):
        """获取当前目录地址"""
        # 借助dirname()从绝对路径中提取目录
        current_file_dir = os.path.dirname(current_file_path)
        return current_file_dir

    # 获取绝对路径
    @staticmethod
    def get_app_ab_path():
        """获取当前项目根地址"""
        return conf['APP_ROOT_PATH']


if __name__ == '__main__':
    print(Path.get_root_path())
