import shutil, os

# 打包输出文件夹
BUILD_OUTPUT_DIR_NAME = './dist'
# App主文件
APP_MAIN_FILE = 'main.py'
# App名称
APP_NAME = '湘西-小金子'
# App图标
APP_ICON_FILE = 'logo.ico'


def clear():
    """删除打包文件夹，并创建空文件夹"""
    # 删除输出文件,并创建空文件夹
    if os.path.exists(BUILD_OUTPUT_DIR_NAME):
        shutil.rmtree(r'{}'.format(BUILD_OUTPUT_DIR_NAME))
    os.makedirs(r'{}'.format(BUILD_OUTPUT_DIR_NAME))


def build_view():
    cmd = "cd view"
    print('命令：{0}, 结果：{1}'.format(cmd, os.system(cmd)))
    cmd = "npm install"
    print('命令：{0}, 结果：{1}'.format(cmd, os.system(cmd)))
    cmd = "npm run build"
    print('命令：{0}, 结果：{1}'.format(cmd, os.system(cmd)))
    cmd = "cd ../"
    print('命令：{0}, 结果：{1}'.format(cmd, os.system(cmd)))


def copy_assets_dir():
    """复制资源"""
    # 复制conf[配置文件]文件夹到dist目录
    shutil.copytree(r'./conf', r'{}/conf'.format(BUILD_OUTPUT_DIR_NAME))
    # 复制cache[运行缓存文件]文件夹到dist目录
    shutil.copytree(r'./cache', r'{}/cache'.format(BUILD_OUTPUT_DIR_NAME))
    # 复制前端视图文件夹到dist目录
    shutil.copytree(r'./view/dist', r'{}/view/dist'.format(BUILD_OUTPUT_DIR_NAME))
    # 删除缓存文件,并创建空文件夹
    shutil.rmtree(r'{}/cache/verify'.format(BUILD_OUTPUT_DIR_NAME))
    os.makedirs(r'{}/cache/verify'.format(BUILD_OUTPUT_DIR_NAME))


def reset_dir():
    """重置日志及配置文件"""
    # 清空app.log
    with open(r'{}/cache/app.log'.format(BUILD_OUTPUT_DIR_NAME), 'w', encoding='utf-8') as f:
        f.write("")
    # 重置conf/mf.json
    with open(r'{}/conf/mf.json'.format(BUILD_OUTPUT_DIR_NAME), 'w', encoding='utf-8') as f:
        f.write("[]")


def build_exe_app():
    """自定义打包"""
    # 安装pyinstaller
    cmd = 'pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyinstaller'
    print('命令：{0}, 结果：{1}'.format(cmd, os.system(cmd)))
    # 进行项目打包，打包为main.exe
    # -c 有控制台窗口，方便打包后调试
    # -w 无控制台窗口
    cmd = 'pyinstaller -F -w -i {0} {1}'.format(APP_ICON_FILE, APP_MAIN_FILE)
    print('命令：{0}, 结果：{1}'.format(cmd, os.system(cmd)))


def rename_main_exe():
    """重命名文件"""
    os.rename(r'{}/main.exe'.format(BUILD_OUTPUT_DIR_NAME), r'{0}/{1}.exe'.format(BUILD_OUTPUT_DIR_NAME, APP_NAME))


def build_install_pkg():
    """自定义打包"""
    clear()
    build_exe_app()
    copy_assets_dir()
    reset_dir()
    rename_main_exe()


if __name__ == '__main__':
   # build_install_pkg()
    build_view()
    print("打包输出目录：{0}".format(os.path.join(os.path.dirname(__file__), BUILD_OUTPUT_DIR_NAME).replace('\.', '')))
    print("--------- 安装包文件打包已完成 ---------")
    pass