from aip import AipOcr
from utils.logger_factory import LoggerFactory
import configparser
from utils.path import Path

"""
百度图片识别
"""

# 全局日志单例
LOGGER = LoggerFactory.get_logger()
# 加载实例化
config = configparser.ConfigParser()


class BaiduOcr(object):

    def __init__(self):
        config.read(Path.get_app_ab_path() + "/conf/app.ini")
        self.APP_ID = config['baidu-ocr']['APP_ID']
        self.API_KEY = config['baidu-ocr']['API_KEY']
        self.SECRET_KEY = config['baidu-ocr']['SECRET_KEY']
        self.OCR_TYPE = config['baidu-ocr']['OCR_TYPE']

    def get_file_content(self, file_path):
        with open(file_path, 'rb') as fp:
            return fp.read()

    def do_ocr(self, image):
        """根据不同类型的方法进行OCR"""
        client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        ret = None
        if self.OCR_TYPE == 'basicGeneral':
            ret = client.basicGeneral(image)
        elif self.OCR_TYPE == 'basicAccurate':
            ret = client.basicAccurate(image)
        elif self.OCR_TYPE == 'general':
            ret = client.general(image)
        elif self.OCR_TYPE == 'accurate':
            ret = client.general(image)
        elif self.OCR_TYPE == 'enhancedGeneral':
            ret = client.general(image)
        elif self.OCR_TYPE == 'webImage':
            ret = client.general(image)

        return ret

    # 调用百度图片识别
    def ocr(self, image_path):
        """ 你的 APPID AK SK """
        image = self.get_file_content(image_path)
        """ 调用网络图片文字识别, 图片参数为本地图片 """
        ret = self.do_ocr(image)
        LOGGER.info("[支持OCR类型] - [basicGeneral，basicAccurate，general，accurate，enhancedGeneral，webImage]")
        LOGGER.info("[百度响应] - 识别类型[{}] - {}".format(self.OCR_TYPE, ret))
        words = ret.get('words_result')
        if words:
            return ''.join(words[0]['words'].split(' '))
        else:
            return ''


if __name__ == '__main__':
    baiduOcr = BaiduOcr()
    ret = baiduOcr.ocr('verify/mf178_verify.png')
    LOGGER.info("百度识别结果：{}".format(ret))
