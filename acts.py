# -*- coding: UTF-8 -*-
# Filename: acts.py

import sys
import os

#import re
#import datetime
import time
#import logRecord
import logging

configDict = {}
scriptList = []

logFileName = "D:\\testLog\\" + time.strftime('%Y%m%d%H%M',time.localtime(time.time())) + ".log"
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename=logFileName,
                filemode='w')
#定义一个Handler打印INFO及以上级别的日志到sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# 设置日志打印格式
formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
# 将定义好的console日志handler添加到root logger
logging.getLogger('').addHandler(console)

def analyzeFile(filename):
    '''Analyze the config file.'''
    try:
        f = file(filename)
        while True:
            line = f.readline()
            if len(line) == 0:
                break
            if "loop" in str(line):
                configDict[line[0:4]] = int(line[5:])
#                print configDict
            if "logFileDir" in str(line):
                configDict[line[0:10]] = line [11:]
#                print configDict
#            print line, # notice comma
    except IOError, e:
        print 'file open error:', e
    logging.info("loop = %s" % configDict['loop'])
    f.close()

def getScript(filename):
    '''Analyze the script file.'''
    try:
        f = file(filename)
        while True:
            line = f.readline()
            if len(line) == 0:
                break
            if not str(line).startswith("#"):
                scriptList.append(str(line))
#                print scriptList
    except IOError, e:
        print 'file open error:', e
    logging.info("共有%s条测试脚本 " % len(scriptList))
    logging.info(scriptList)
    f.close()

def scriptExec(num):
    '''Scripts execute'''
#     logFileNameStr = configDict['logFileDir'] + scriptList[num][:-4]
#     print logFileNameStr
#     logRecord.logConfig(logFileNameStr)
#    for i in range(len(scriptList)):
#        print "测试脚本: %s" % scriptList[i]
    log = "测试脚本: " + scriptList[num][:-1]
    logging.info(log)
    for j in range(configDict['loop']):
#       print "[%s]第%s次测试开始：" % (datetime.datetime.now(), str(j+1))
        log = "第" + str(j+1) + "次测试开始"
        logging.info(log)
#       os.system("C:\Python27\python %s" % scriptList[i])
#         output = os.popen("C:\Python27\python %s" % scriptList[num])
#         logging.info(output.read())
        execfile(scriptList[num][:-1])  #去除字符串末尾的\n        

def changePath(filename):
    regex = "\\"
    newstr = "/"
    newFilename = filename.replace(regex, newstr)
    return newFilename[:-1] #去除字符串末尾的\n

# Script starts from here
if __name__ == '__main__':
    if len(sys.argv) < 5:
        print 'Missing Parameters, please check!'
        sys.exit()

    if sys.argv[1].startswith('-c'):
#        dir = os.getcwd()
#        parent_dir = os.path.dirname(dir)
        filename1 = sys.argv[2]
        analyzeFile(filename1) #解析配置文件
    else:
        print "运行配置不正确，请正确配置-c参数"
        sys.exit() 
#    logRecord.logConfig("D:\\testLog\\")
    if sys.argv[3].startswith('-tf'):
        filename2 = sys.argv[4]
        getScript(filename2) #解析脚本列表文件
        i = 0
        for i in range(len(scriptList)):
            newFilename = changePath(scriptList[i])
            if os.path.exists(newFilename):
                scriptExec(i) #执行测试脚本
                i += 1
            else:
                logging.info("脚本: %s 不存在，请检查！" % scriptList[i])
    else:
        print "运行配置不正确，请正确配置-tf参数"
        sys.exit() 
        
