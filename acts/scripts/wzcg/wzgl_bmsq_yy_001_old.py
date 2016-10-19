# -*- coding: UTF-8 -*-
#---------------------------------------------------------
#脚本编号：wzgl_bmsq_yy_001
#功能：测试运营类物资编码申请---正常流程
#步骤：1、编码申请提交
#     2、检测物资编码申请单状态是否正常
#     3、估价员登录EMIS系统进行物资估价
#     4、检测物资编码申请单状态是否正常
#     5、审核员登录EMIS系统进行物资审核
#     6、检测物资编码是否正确产生
#作者：胡滔
#日期：2016.07.18
#---------------------------------------------------------

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.support.select import Select
#from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
#from selenium.webdriver.common.keys import Keys #引入keys类操作
import time
import logging
  
reload(sys)
sys.setdefaultencoding('utf-8')

option = webdriver.ChromeOptions()
#option.add_argument('--user-data-dir=C:\Users\hutao\AppData\Local\Google\Chrome\User Data\Default') #偶尔引发不响应最大化窗口指令，原因待查
option.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])#消除提示语句：您使用的是不受支持的命令行标记: --ignore-certificate-errors
browser = webdriver.Chrome(chrome_options=option)
browser.implicitly_wait(20)
browser.get('http://192.168.1.233:8180/aems-equipment/login.jsp;jsessionid=pv7sY4FBE7gPE0m-sCMNdB9D#page/homepage') #test环境
#browser.get('http://192.168.1.113:8888/aems-equipment/aems/home#page/homepage') #生产环境
#print '访问EMIS'
logging.info("访问EMIS")
time.sleep(1)
browser.maximize_window()
text = browser.find_element_by_xpath(".//*[@id='login-box']/div/div/h4").text
#print text
logging.info(text)

browser.find_element_by_xpath(".//*[@id='phone']").clear()
time.sleep(1)
browser.find_element_by_xpath(".//*[@id='phone']").send_keys(u'18612257445') #登录test环境
#browser.find_element_by_xpath(".//*[@id='phone']").send_keys(u'18515331229') #登录生产环境
time.sleep(1)
browser.find_element_by_xpath(".//*[@id='loginPassword']").clear()
time.sleep(1)
browser.find_element_by_xpath(".//*[@id='loginPassword']").send_keys(u'000000')#登录test环境
#browser.find_element_by_xpath(".//*[@id='loginPassword']").send_keys(u'123456') #登录生产环境
time.sleep(1)
browser.find_element_by_xpath(".//*[@id='loginButton']").click()

try:
    element = WebDriverWait(browser,30).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '物资管理')]")))
except:
#    print "网络异常，请检查"
    logging.info("网络异常，请检查")
    browser.quit()
    sys.exit()
  
#step1:进入物资管理，进行运营类物资编码申请  
text = browser.find_element_by_xpath("//span[contains(text(), '物资管理')]").text
#print "enter in: %s" % text
logging.info("enter in: %s" % text)
browser.find_element_by_xpath("//span[contains(text(), '物资管理')]").click()
time.sleep(1)
#进入物资编码申请
text = browser.find_element_by_link_text("物资编码申请").text
#print "enter in: %s" % text
logging.info("enter in: %s" % text)
browser.find_element_by_link_text("物资编码申请").click()
time.sleep(3)

if not browser.find_element_by_link_text("运营类物资申请").is_displayed():
#    print "物资编码申请页面失效，测试失败"
    logging.info("物资编码申请页面失效，测试失败")
    browser.quit()
    sys.exit()
else:
    #添加新物资编码申请
    browser.find_element_by_xpath(".//*[@id='Y']/a").click()
    time.sleep(1)
    browser.find_element_by_xpath(".//*[@id='grid-pager_left']/table/tbody/tr/td[1]/div/span").click()
    time.sleep(3)
    browser.find_element_by_xpath(".//*[@id='matName']").clear()
    time.sleep(1)
    
    wzName = "tay-" + time.strftime('%Y%m%d%H%M',time.localtime(time.time())) #taf:test-auto-fyy
#    print "物资名称为：%s" % wzName
    logging.info("物资名称为：%s" % wzName)
    browser.find_element_by_xpath(".//*[@id='matName']").send_keys(wzName)
    time.sleep(1)
    browser.find_element_by_xpath(".//*[@id='matVersion']").clear()
    time.sleep(1)
    browser.find_element_by_xpath(".//*[@id='matVersion']").send_keys(wzName)
    time.sleep(1)
    browser.find_element_by_xpath(".//*[@id='reportLabel']/span/span[1]/span/span[2]").click()
    time.sleep(1)

    browser.find_element_by_xpath("//*[@class='select2-results']/ul/li[1]").click() #选取大类中第一个值
    time.sleep(1)
#    browser.find_element_by_xpath(".//*[@id='aData']/a").click() #点击“提交”按钮
    time.sleep(1)

#step2:检查提交信息状态是否正确
    browser.find_element_by_xpath(".//*[@id='main-container']/div[2]/div[2]/div[2]/div[1]/div[1]").click() #for test. click "返回" 需提交时注释掉
    time.sleep(2)
    numberStr =str(browser.find_element_by_xpath(".//*[@id='grid-pager_right']/div").text)
    if "无数据显示" in numberStr:
#        print "%s:物资编码申请提交失败，请检查，测试失败" % numberStr
        logging.info("%s:物资编码申请提交失败，请检查，测试失败" % numberStr)
        browser.quit()
        sys.exit() 
    else:
        i = 0
        for s in numberStr.split():
            if i == 3:
                number = filter(str.isdigit, s)
            i += 1
        parentPath = "//*[@id=\'grid-table\']/tbody/tr["
        for i in range(int(number)):
            path = parentPath + str(i+2) + "]/td[4]" 
            text = browser.find_element_by_xpath(path).text
            if wzName in text:
                path = parentPath + str(i+2) + "]/td[12]"
                text = browser.find_element_by_xpath(path).text
                print text, i
                if "估价中" in text:
#                    print "物资编码申请已提交！！" 
                    logging.info("物资编码申请已提交！！")
                    browser.find_element_by_xpath(".//*[@id='navbar-container']/div[2]/ul/li/a/i").click()
                    time.sleep(1)
                    browser.find_element_by_xpath(".//*[@id='navbar-container']/div[2]/ul/li/ul/li[2]/a").click()
                    time.sleep(3)
                    break
                else:
#                    print "物资编码申请状态信息不正确，请检查，测试失败"    
                    logging.info("物资编码申请状态信息不正确，请检查，测试失败")
                    browser.quit()
                    sys.exit()
        print i
        if i >= range(int(number)):
#            print "物资编码申请提交失败，请检查，测试失败"
            logging.info("物资编码申请提交失败，请检查，测试失败")
            browser.quit()
            sys.exit()
        
#step3:物资估价人登录EMIS系统，进行物资估价
#browser.get('http://192.168.1.233:8180/aems-equipment/login.jsp;jsessionid=pv7sY4FBE7gPE0m-sCMNdB9D#page/homepage')
#time.sleep(1)
browser.find_element_by_xpath(".//*[@id='phone']").clear()
time.sleep(1)
browser.find_element_by_xpath(".//*[@id='phone']").send_keys(u'18515331229')
time.sleep(1)
browser.find_element_by_xpath(".//*[@id='loginPassword']").clear()
time.sleep(1)
browser.find_element_by_xpath(".//*[@id='loginPassword']").send_keys(u'123456')
time.sleep(1)
browser.find_element_by_xpath(".//*[@id='loginButton']").click()
time.sleep(3)

#进入物资估价
text = browser.find_element_by_xpath("//span[contains(text(), '物资管理')]").text
#print "enter in: %s" % text
logging.info("enter in: %s" % text)
browser.find_element_by_xpath("//span[contains(text(), '物资管理')]").click()
time.sleep(1)
text = browser.find_element_by_link_text("物资估价").text
#print "enter in: %s" % text
logging.info("enter in: %s" % text)
browser.find_element_by_link_text("物资估价").click()
time.sleep(2)

sendKey = wzName
#print "对名称为%s的物资进行估价" % sendKey 
logging.info("对名称为%s的物资进行估价" % sendKey)
numberStr =str(browser.find_element_by_xpath(".//*[@id='grid-pager_right']/div").text)
if "无数据显示" in numberStr:
#    print "%s:没有任何物资估价单，请检查，测试失败" % numberStr
    logging.info("%s:没有任何物资估价单，请检查，测试失败" % numberStr)
    browser.quit()
    sys.exit() 
else:
    i = 0
    for s in numberStr.split():
        if i == 3:
            number = filter(str.isdigit, s)
        i += 1
    parentPath = "//*[@id=\'grid-table\']/tbody/tr["
    for i in range(int(number)):
        path = parentPath + str(i+2) + "]/td[3]" 
        text = browser.find_element_by_xpath(path).text
        if wzName in text:
            path = parentPath + str(i+2) + "]/td[11]"
            text = browser.find_element_by_xpath(path).text
            print text, i
            if "估价中" in text:
                break
            else:
#                print "物资编码申请状态信息不正确，请检查，测试失败"   
                logging.info("物资编码申请状态信息不正确，请检查，测试失败") 
                browser.quit()
                sys.exit()
    if i >= range(int(number)):
#        print "没有该物资的估价单，请检查，测试失败"
        logging.info("没有该物资的估价单，请检查，测试失败")
        browser.quit()
        sys.exit()
path = parentPath + str(i+2) + "]/td[2]/div/span[1]/a"
browser.find_element_by_xpath(path).click()
time.sleep(2)
browser.find_element_by_xpath(".//*[@id='matPrice']").send_keys('1')
browser.find_element_by_xpath(".//*[@id='matCycle']").send_keys('10')
browser.find_element_by_xpath(".//*[@id='contractCycle']").send_keys('5')
Select(browser.find_element_by_id("userUnit")).select_by_index(1)
browser.find_element_by_xpath(".//*[@id='reportLabel']/span/span[1]/span/span[2]").click()
time.sleep(1)
browser.find_element_by_xpath("//*[@id='select2-purchasingCategory-results']/li[2]").click() 
time.sleep(1)
#browser.find_element_by_xpath(".//*[@id='tData']").click() #测试，暂不提交
time.sleep(1) 

#step4: 检测物资估价申请单状态是否正常
browser.find_element_by_xpath(".//*[@id='main-container']/div[2]/div[2]/div[2]/div[1]/div/div[1]").click() #for test. 不提交，点击返回
numberStr =str(browser.find_element_by_xpath(".//*[@id='grid-pager_right']/div").text)
if "无数据显示" in numberStr:
#    print "%s:没有任何物资估价单，请检查，测试失败" % numberStr
    logging.info("%s:没有任何物资估价单，请检查，测试失败" % numberStr)
    browser.quit()
    sys.exit() 
else:
    wzName = "E2E-X5E1" #only for temporary test
    i = 0
    for s in numberStr.split():
        if i == 3:
            number = filter(str.isdigit, s)
        i += 1
    parentPath = "//*[@id=\'grid-table\']/tbody/tr["
    for i in range(int(number)):
        path = parentPath + str(i+2) + "]/td[3]" 
        text = browser.find_element_by_xpath(path).text
        if wzName in text:
            path = parentPath + str(i+2) + "]/td[11]"
            text = browser.find_element_by_xpath(path).text
            print text, i
            if "核实中" in text:
                break
            else:
#                print "物资估价申请状态信息不正确，请检查，测试失败"   
                logging.info("物资估价申请状态信息不正确，请检查，测试失败") 
                browser.quit()
                sys.exit()
    if i >= range(int(number)):
#        print "没有该物资的估价单，请检查，测试失败"
        logging.info("没有该物资的估价单，请检查，测试失败")
        browser.quit()
        sys.exit()
        
#    print "物资估价已经完成!!!"
    logging.info("物资估价已经完成!!!")
    browser.find_element_by_xpath(".//*[@id='navbar-container']/div[2]/ul/li/a/i").click()
    time.sleep(1)
    browser.find_element_by_xpath(".//*[@id='navbar-container']/div[2]/ul/li/ul/li[2]/a").click()
    time.sleep(2)

#step5:物资核实人员登录EMIS进行物资核实
browser.find_element_by_xpath(".//*[@id='phone']").clear()
time.sleep(1)
browser.find_element_by_xpath(".//*[@id='phone']").send_keys(u'18515331229')
time.sleep(1)
browser.find_element_by_xpath(".//*[@id='loginPassword']").clear()
time.sleep(1)
browser.find_element_by_xpath(".//*[@id='loginPassword']").send_keys(u'123456')
time.sleep(1)
browser.find_element_by_xpath(".//*[@id='loginButton']").click()
time.sleep(2)
    
#进入物资核实
text = browser.find_element_by_xpath("//span[contains(text(), '物资管理')]").text
#print "enter in: %s" % text
logging.info("enter in: %s" % text)
browser.find_element_by_xpath("//span[contains(text(), '物资管理')]").click()
time.sleep(1)
text = browser.find_element_by_link_text("物资核实").text
#print "enter in: %s" % text
logging.info("enter in: %s" % text)
browser.find_element_by_link_text("物资核实").click()
time.sleep(2)

#sendKey = wzName
sendKey = "行程开关" #only for temporary test
#print "对名称为%s的物资进行核实" % sendKey 
logging.info("对名称为%s的物资进行核实" % sendKey)
numberStr =str(browser.find_element_by_xpath(".//*[@id='grid-pager_right']/div").text)
if "无数据显示" in numberStr:
#    print "%s:没有任何物资核实单，请检查，测试失败" % numberStr
    logging.info("%s:没有任何物资核实单，请检查，测试失败" % numberStr)
    browser.quit()
    sys.exit() 
else:
    i = 0
    for s in numberStr.split():
        if i == 3:
            number = filter(str.isdigit, s)
        i += 1
    parentPath = "//*[@id=\'grid-table\']/tbody/tr["
    for i in range(int(number)):
        path = parentPath + str(i+2) + "]/td[3]" 
        text = browser.find_element_by_xpath(path).text
        if sendKey in text:
            path = parentPath + str(i+2) + "]/td[10]"
            text = browser.find_element_by_xpath(path).text
            if "核实中" in text:
                break
            else:
#                print "物资核实申请状态信息不正确，请检查，测试失败"   
                logging.info("物资核实申请状态信息不正确，请检查，测试失败") 
                browser.quit()
                sys.exit()
    if i >= range(int(number)):
#        print "没有该物资的核实单，请检查，测试失败"
        logging.info("没有该物资的核实单，请检查，测试失败")
        browser.quit()
        sys.exit()
path = parentPath + str(i+2) + "]/td[2]/div/span[1]/a"
browser.find_element_by_xpath(path).click()
time.sleep(2)

#browser.find_element_by_xpath(".//*[@id='tData']").click() #测试，暂不提交
time.sleep(1) 

#检测物资核实申请单状态是否正常
browser.find_element_by_xpath(".//*[@id='main-container']/div[2]/div[2]/div[2]/div[1]/div[1]").click() #for temporary test. 不提交，点击返回
numberStr =str(browser.find_element_by_xpath(".//*[@id='grid-pager_right']/div").text)
if "无数据显示" in numberStr:
#    print "%s:没有任何物资核实单，请检查，测试失败" % numberStr
    logging.info("%s:没有任何物资核实单，请检查，测试失败" % numberStr)
    browser.quit()
    sys.exit() 
else:
    wzName = "碳滑靴" #only for temporary test
    i = 0
    for s in numberStr.split():
        if i == 3:
            number = filter(str.isdigit, s)
        i += 1
    parentPath = "//*[@id=\'grid-table\']/tbody/tr["
    for i in range(int(number)):
        path = parentPath + str(i+2) + "]/td[3]" 
        text = browser.find_element_by_xpath(path).text
        if wzName in text:
            path = parentPath + str(i+2) + "]/td[10]"
            text = browser.find_element_by_xpath(path).text
            print text, i
            if "完成" in text:
#                print "物资核实已经完成!!!"
                logging.info("物资核实已经完成!!!")
                break
            else:
#                print "物资核实申请状态信息不正确，请检查，测试失败"   
                logging.info("物资核实申请状态信息不正确，请检查，测试失败") 
                browser.quit()
                sys.exit()
    if i >= range(int(number)):
#        print "没有该物资的核实单，请检查，测试失败"
        logging.info("没有该物资的核实单，请检查，测试失败")
        browser.quit()
        sys.exit()
        
#step6: 检查物资编码是否生成
#进入物资编码申请
text = browser.find_element_by_link_text("物资编码申请").text
#print "enter in: %s" % text
logging.info("enter in: %s" % text)
browser.find_element_by_link_text("物资编码申请").click()
time.sleep(3)
browser.find_element_by_xpath(".//*[@id='Y']/a").click()
time.sleep(2) 
numberStr =str(browser.find_element_by_xpath(".//*[@id='grid-pager_right']/div").text)
if "无数据显示" in numberStr:
#    print "已物资核实，无数据，请确认核实流程，测试失败"
    logging.info("已物资核实，无数据，请确认核实流程，测试失败")
    browser.quit()
    sys.exit() 
else:
    wzName = "test-1" #only for temporary test
    i = 0
    for s in numberStr.split():
        if i == 3:
            number = filter(str.isdigit, s)
        i += 1
    parentPath = "//*[@id=\'grid-table\']/tbody/tr["
    for i in range(int(number)):
        path = parentPath + str(i+2) + "]/td[4]" 
        text = browser.find_element_by_xpath(path).text
        if wzName in text:
            path = parentPath + str(i+2) + "]/td[12]"
            text = browser.find_element_by_xpath(path).text
            print text, i
            if "完成" in text:
                path = parentPath + str(i+2) + "]/td[3]"
                text = browser.find_element_by_xpath(path).text
#                print "物资编码  = %s" % text
                logging.info("物资编码  = %s" % text)
                break
            else:
#                print "物资编码申请状态信息不正确，请检查，测试失败"  
                logging.info("物资编码申请状态信息不正确，请检查，测试失败")  
                browser.quit()
                sys.exit()
    if i >= range(int(number)):
#        print "物资编码申请提交失败，请检查，测试失败"
        logging.info("物资编码申请提交失败，请检查，测试失败")
        browser.quit()
        sys.exit()

time.sleep(3)

#print "运营类物资编码申请流程测试成功！！"
logging.info("物资编码申请提交失败，请检查，测试失败")
browser.quit()