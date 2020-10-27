# -*- encoding=utf8 -*-
__author__ = "hallo"

import os

#包名
apk = "cn.smartinspection.combine"


#项目根路径
project_root = os.path.dirname(os.path.realpath(__file__)) +'\case'


#日志路径
safety_logdir = os.path.dirname(os.path.realpath(__file__))+ '\log\safety'

docs_logdir = os.path.dirname(os.path.realpath(__file__))+ '\log\docs'


#运行日志文件
logfile = "log.txt"

#输出报告文件
safety_output= os.path.dirname(os.path.realpath(__file__))+r"\report\安全检查回归报告.html"

docs_output= os.path.dirname(os.path.realpath(__file__))+r"\report\图纸文档回归报告.html"

