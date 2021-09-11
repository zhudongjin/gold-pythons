from PIL import Image
import pytesseract

"""
本地图片识别
"""


class OsheepOcr(object):

    def __init__(self):
        pass

    @staticmethod
    def image_to_text(image_path):
        """
        传入文本(jpg、png)的绝对路径,读取文本
        :param text_path:
        :return: 文本内容
        """
        # 验证码图片转字符串
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        if text.find("\n") > -1:
            text = text.split('\n')[0]
        return text

    # 调用本地图片识别
    def ocr(self, image_path):
        """ 调用本地图片识别 """
        return OsheepOcr.image_to_text(image_path)


if __name__ == '__main__':
    ssheepOcr = OsheepOcr()
    ret = ssheepOcr.ocr('verify/mf178_verify.png')
    print("本地识别结果：{}".format(ret))
