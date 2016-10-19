# -*- coding: UTF-8 -*-
# Filename: logRecord.py

import logging
import logging.handlers
import time

def logConfig(logFileName):
    #配置日志信息
    fileName = logFileName + '_' + time.strftime('%Y%m%d%H%M',time.localtime(time.time())) + '.log'
    print fileName
    logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename=fileName,
                filemode='w')
    #定义一个Handler打印INFO及以上级别的日志到sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # 设置日志打印格式
    formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    # 将定义好的console日志handler添加到root logger
    logging.getLogger('').addHandler(console)

def mylog(self, log):
    logging.info(log)
    return
