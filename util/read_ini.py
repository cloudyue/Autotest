# coding = utf-8

import configparser
import os


class ReadIni:
    """
    @note: 读取配置文件ini的类，可以配置文件，默认文件为config.ini
    @isPageView:是否为页面元素配置文件，@file_name:文件名称
    """

    def __init__(self, isPageView=True, file_name=None):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        default_cfg = 'config.ini'
        if file_name == None and isPageView == False:
            file_path = os.path.join(base_dir + r'/config/' + default_cfg)
        elif isPageView == False and file_name != None:
            file_path = os.path.join(base_dir + r'/config/' + file_name)
        else:
            file_path = os.path.join(base_dir + r'/pageView/' + file_name)
        self.cfg = configparser.ConfigParser()
        self.cfg.read(file_path, encoding="utf-8-sig")

    def Read_config(self, para1, para2):
        """
        @para1: 配置文件模块
        @para2: 配置文件子模块
        @return:data 子模块内容
        """
        data = self.cfg.get(para1, para2)
        return data
