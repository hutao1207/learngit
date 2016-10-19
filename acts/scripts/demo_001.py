#coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
from selenium.webdriver.common.keys import Keys #引入keys类操作
import time
import sys
import logging

#print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')
    
option = webdriver.ChromeOptions()
#option.add_argument('--user-data-dir=C:\Users\hutao\AppData\Local\Google\Chrome\User Data\Default') 
option.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])#消除提示语句：您使用的是不受支持的命令行标记: --ignore-certificate-errors
browser = webdriver.Chrome(chrome_options=option)

browser.implicitly_wait(10)
browser.get('http://weixin.qq.com/')
#print '访问weixin'
log = "访问weixin"
logging.info(log)
try:
#    element = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "w3")))
    element = WebDriverWait(browser,30).until(EC.visibility_of_element_located((By.LINK_TEXT, "免费下载")))
except:
    logging.info("网络异常，请检查")
    browser.quit()
    sys.exit()
browser.maximize_window()
winHandleBefore = browser.current_window_handle
#print winHandleBefore

# time.sleep(2)
# js="var q=document.documentElement.scrollTop=10000"
# browser.execute_script(js)
# time.sleep(2)

# text = browser.find_element_by_xpath("html/body/div[1]/div/div[3]/div[1]/p").text
text = browser.find_element_by_xpath("//p[contains(text(), 'Tencent Inc')]").text
#print text #打印备案信息
logging.info(text)

#print browser.find_element_by_xpath("html/body/div[2]/div[1]/ul/li[2]/a/span").get_attribute('type')
# browser.find_element_by_xpath("html/body/div[1]/div/div[1]/ul/li[2]/a/span").click()
browser.find_element_by_xpath("//span[contains(text(), '帮助与反馈')]").click()
browser.implicitly_wait(10)
allHandles = browser.window_handles

for handle in allHandles:
    if handle != winHandleBefore:
        browser.switch_to_window(handle)
        try:
            browser.find_element_by_xpath(".//*[@id='top_4_tool']/li[1]/a/em").is_displayed() 
        except:
#            print "元素不存在, 测试失败"
            log = "元素不存在, 测试失败"
            logging.info(log)
        else:
#            print "元素存在, 测试成功"
            log = "元素存在, 测试成功"
            logging.info(log)
        browser.close()

browser.switch_to_window(winHandleBefore)

#print '现在我将打开网页w3school'
log = "现在我将打开网页w3school"
logging.info(log)
browser.implicitly_wait(20)
browser.get('http://www.w3school.com.cn/')
time.sleep(2)
try:
    browser.find_element_by_xpath(".//*[@id='navsecond']/h2[1]").is_displayed()
except:
#    print "1.元素不存在, 测试失败"
    log = "1.元素不存在, 测试失败"
    logging.info(log)
else:
    article = browser.find_element_by_xpath(".//*[@id='navsecond']/ul[1]/li[1]/a")
    ActionChains(browser).move_to_element(article).perform()#将鼠标移动到这里
    time.sleep(1)
#    ActionChaintime.sleep(browser).context_click(article).perform() #鼠标右击
#    ActionChaintime.sleep(browser).click_and_hold(article).perform()#鼠标左击
    ActionChains(browser).click(article).perform() #鼠标左键点击
    browser.implicitly_wait(30)
    try:   
#        browser.find_element_by_css_selector("#article-nav-older > div.article-nav-title").is_displayed()
#        browser.find_element_by_xpath(".//*[@id='intro']/h2").isdisplayed()
#        browser.find_element_by_id("tpn").is_displayed()
        browser.find_element_by_xpath("//h1[contains(text(), 'HTML 教程')]").is_displayed()
    except:
#        print "2.元素不存在, 测试失败" 
        log = "2.元素不存在, 测试失败"
        logging.info(log)
    else:
#        text1 = browser.find_element_by_css_selector("#article-nav-older > div.article-nav-title").text
#        text1 = browser.find_element_by_id("tpn").text
        text1 = browser.find_element_by_xpath("//h1[contains(text(), 'HTML 教程')]").text
#        print "2.元素:\"%s\" 存在, 测试成功" % (text1.decode('utf8'))
        log = "2.元素:" + "\"" + text1.decode('utf8') + "\"存在, 测试成功"
        logging.info(log)
    #将页面滚动条拖到底部
    # print "将页面滚动条拖到底部"
    # time.sleep(3)
    # js="var q=document.documentElement.scrollTop=10000"
    # browser.execute_script(js)
    # time.sleep(5)
    
        try:
            browser.find_element_by_xpath("//h2[contains(text(), 'HTML 教程')]").is_displayed() 
        except:
#            print "3.元素不存在, 测试失败"
            log = "3.元素不存在, 测试失败"
            logging.info(log)
        else:
            text2 = browser.find_element_by_xpath("//h2[contains(text(), 'HTML 教程')]").text
#            print "3.元素:\"%s\" 存在, 测试成功" % (text2.decode('utf8'))
            log = "3.元素:" + "\"" + text2.decode('utf8') + "\"存在, 测试成功"
            logging.info(log)
#将滚动条移动到页面的顶部
# print "将滚动条移动到页面的顶部"
# js_="var q=document.documentElement.scrollTop=0"
# browser.execute_script(js_)
# time.sleep(3)

browser.quit()
