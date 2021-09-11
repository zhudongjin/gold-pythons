import os.path
import sys

import webview
from flask import Flask, render_template
from controller import mf

from utils.path import Path
from utils.config import conf

from utils.logger_factory import LoggerFactory

LOGGER = LoggerFactory.get_logger()
APP_NAME = "湘西-小金子"

ui_dir_name = 'view'
gui_dir = os.path.join(os.path.dirname(__file__), ui_dir_name)
if not os.path.exists(gui_dir):
    gui_dir = '{}/{}'.format(Path.get_root_path(sys.executable), ui_dir_name)
    LOGGER.info("打包 -> {}".format(gui_dir))
server = Flask(__name__, static_folder=gui_dir + "/dist/static", template_folder=gui_dir + "/dist")
server.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1

server.register_blueprint(mf)


@server.route("/")
def index():
    return render_template("index.html")


def app_init():
    # 设置根目录
    conf['APP_ROOT_PATH'] = gui_dir.replace("view", '')
    LOGGER.info("项目配置：{}".format(conf))


def push_log_info(msg):
    """输出Loger日志"""
    try:
        MAIN_WINDOW.evaluate_js('window.receiveAppLog("{0}")'.format(msg))
    except Exception as e:
        pass


def app_start():
    """AppStart"""
    # 启动准备
    app_init()
    global MAIN_WINDOW
    MAIN_WINDOW = webview.create_window(title=APP_NAME, url=server, resizable=False, width=1180, height=720,
                                        confirm_close=True,
                                        text_select=False)
    # 日志输出
    LoggerFactory.add_push_handler(push_log_info)
    # 启动WebView
    chinese = {
        'global.quitConfirmation': u'确定关闭{}?'.format(APP_NAME),
    }
    webview.start(http_server=True, localization=chinese, debug=True)


if __name__ == '__main__':
    mode = "dev"
    if Path.get_root_path(sys.executable).find("script") > -1:
        server.run()
    else:
        app_start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
