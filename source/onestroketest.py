#!/usr/bin/env python
# @Time : 2020/4/2 11:15 
# @Author : lifei
#@desc:构建云测平台
import time

from appium import webdriver
import os
class OneStrokeTest:
    def __init__(self,device_name,platform_version,port):
        apk_path = os.path.join(os.getcwd(),'yibijizhang.apk')
        self.deviceName= device_name
        self.desired_caps = {
            "automationName":"UiAutomator1",#针对appium1.13.1以上版本注意测试Android系统5.0以下版本必须增加此项配置
            "platformName":"Android",
            "platformVersion":platform_version,
            "deviceName":self.deviceName,
            "appPackage":"com.mobivans.onestrokecharge",
            "appActivity":"com.stub.stub01.Stub01",
            "app":apk_path,
            "unicodeKeyboard":"true"
        }
        self.url = "http://127.0.0.1:%d/wd/hub"% (port)
        print('url',self.url)

    def start_test(self):
        driver = webdriver.Remote(self.url,self.desired_caps)
        driver.implicitly_wait(120)
        try:
            # 现在我们用这种方式来代替by_name的方法，要注意的是字符串必须外单内双
            driver.find_element_by_android_uiautomator('text("记一笔")').click()
            # 实现滚动
            # driver.scroll(driver.find_element_by_android_uiautomator('text("医疗)'),
            #               driver.find_element_by_android_uiautomator('text("餐饮)'))
            driver.find_element_by_android_uiautomator('text("书籍")').click()
            time.sleep(2)
            editor = driver.find_element_by_id('add_et_remark')
            # 先清空编辑框 再输入
            editor.clear()
            editor.send_keys('购买学习书籍')
            time.sleep(2)
            # driver.find_element_by_accessibility_id()
            driver.find_element_by_id('keyb_btn_2').click()
            driver.find_element_by_id('keyb_btn_3').click()
            driver.find_element_by_id('keyb_btn_8').click()
            driver.find_element_by_id('keyb_btn_finish').click()
            driver.find_element_by_android_uiautomator('text("长按记录可删除")').click()
            time.sleep(3)
            remarks = driver.find_elements_by_id('account_item_txt_remark')
            print('remarks=====',remarks)
            money = driver.find_elements_by_id('account_item_txt_money')

            if remarks[0].text == "购买学习书籍" and money[0].text == '-238':
                print('test success')
            else:
                print('test fail')
        except Exception as e:
            with open(os.path.join(os.getcwd(),'report%s_error.log' % self.deviceName),'w') as f:
                f.write(str(e) + '\n')
            timestamp = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
            driver.get_screenshot_as_file(os.path.join(os.getcwd(),'report%s_%s.png' % (self.deviceName,timestamp)))
        # driver.quit()

if __name__ == '__main__':
    OneStrokeTest('Android_7.1','7.1',4723).start_test()



