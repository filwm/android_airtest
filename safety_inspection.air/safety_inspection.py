# -*- encoding=utf8 -*-
__author__ = "hallo"

from airtest.core.api import *

import threading
import time
import random

#ST.PROJECT_ROOT = "D:\\airtest_script\\"
ST.PROJECT_ROOT = "D:\\android_airtest\\"
from airtest.core.api import using

using("login.air")
from login import login

using("common_api.air")
from common_api import *

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

auto_setup(__file__)


#，拍照后，打开图片，定位，并退出
def pic_test():
    touch((130,330))  #点击图片位置查看图片
    swipe((1000,1000),(200,1000),duration=0.5) #从左到右画横线1秒
    pinch(in_or_out='out',center=(500,1300),percent=0.005)  #放大
    pinch(in_or_out='in',center=(500,1300),percent=0.005)   #缩小
    sleep(1)
    
    touch(Template(r"tpl1568708907804.png", record_pos=(-0.464, 0.832), resolution=(1080, 2340)))
    
    if exists(Template(r"20200406133547.png")):
        poco(name="转到上一层级").click()
    
    sleep(1)
    if exists(Template(r"tpl1586151572877.png", record_pos=(0.031, 0.867), resolution=(1080, 2340))):
        pinch(in_or_out='out',center=(500,1300),percent=0.005)  #放大
        sleep(0.5)
        pinch(in_or_out='in',center=(500,1300),percent=0.005)  
        sleep(1)
    
        #poco("android.widget.ImageView").click() #退出地图页
        touch(Template(r"tpl1571304212660.png", record_pos=(-0.368, -0.906), resolution=(1080, 2340)))
    
        poco(name="转到上一层级").click()

#长按删除照片
def delete_pic():
    swipe((130,330),(130,330),duration=0.5) #拖动到相对位置为0的地方，实现长按效果
    assert_exists(Template(r"tpl1585582863805.png", threshold=0.9, record_pos=(-0.324, -0.824), resolution=(1080, 2340)))
    while exists(Template(r"tpl1585582863805.png", threshold=0.9, record_pos=(-0.324, -0.824), resolution=(1080, 2340))):
        touch(Template(r"tpl1585582863805.png", threshold=0.9, record_pos=(-0.324, -0.824), resolution=(1080, 2340)))
    sleep(1)
    

#对检查项进行检查（通过与不通过）并提取不通过的检查项文本
def check_item():
    #遍历检查项，并随机对检查项进行检查（检查项数量、通过与不通过的按钮位置，）
    check_item = poco(type="androidx.recyclerview.widget.RecyclerView").children()  #获取所有检查项
    anyint = random.randint(0,len(check_item)-1)   #获取随意一个数作为指定的不通过检查项
    for item in check_item:    #遍历检查项，经过判断检查项名字相等，点击某一个组件
        if item.child().child().get_text() == check_item[anyint].child().child().get_text():
            false_item = item.child().child().get_text().rstrip(" icon")  #检查项的值（去掉右边的icon）
            print (false_item)
            item.child().child().set_text("1")  #将值设短，避免影响组件顺序
            item.child().child()[2].click() #点击×
        else:
            item.child().child().set_text("1")  #将值设短，避免影响组件顺序
            item.child().child()[1].click() #点击√ 
    return false_item
    
#新增合格检查，并断言结果    
def add_qualified():
    poco(text="新增检查记录").click()
    take_pic(2)
    sleep(1)
    
    pic_test()
    
    delete_pic()
    
    poco(text="补充描述").click()

    check_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    comment = "于 " + check_time +" 新增合格检查记录。"
    text(comment,enter=False)
    
    check_item()
        
    poco(text="检查合格",type="android.widget.Button").click()
    
    
    sleep(1)
    
    touch((500,680)) #通过坐标点击最新一条检查记录
    

    
    assert_exists(Template(r"tpl1586277235003.png", record_pos=(0.029, -0.618), resolution=(1080, 2340)), "新增不合格成功")
    
    poco(name="转到上一层级").click()

#选择是否发起整改流程    
def add_issue(add): # 0：否  1：是
    wait(Template(r"tpl1589820114424.png", record_pos=(-0.008, -0.032), resolution=(1080, 2340)))

    if  add ==0:
        poco(text='否').click()
    elif add==1:
        poco(text='是').click()
    sleep(1)
        
def create_issue(check_item,area):   #需设置为不通过的检查项； 检查部位列表；
    exists(Template(r"tpl1590423070275.png", record_pos=(-0.264, -0.774), resolution=(1080, 2340)))
    
    #搜索检查项，选择、断言
    poco(text="检查项",type='android.widget.TextView').click()
    result_item ='.*' + search_check_item(check_item) + '.*$'
    
    poco.wait_for_any(poco(textMatches=result_item))
    
    #添加语音
    create_audio()
    
    #断言描述内容
    content="如题如题发现如下问题：" + check_item +";" 
    poco.wait_for_any(poco(text=content))
    
    #搜索检查部位、选择、断言
    poco(text='检查部位').click()
    search_area(area)
    sleep(1)
    poco.wait_for_any(poco(text='-'.join(area)))
    
    #标记图纸
    poco(text='图纸位置').click()
    mark_drawing()
    poco.wait_for_any(poco(text='已标识(1)'))  #只标记一个点的断言
    
    #人员、期限

        
        
#新增不合格检查，并断言结果    
def add_unqualified():
    poco(text="新增检查记录").click()
    take_pic(2)
    sleep(1)
    
    
    poco(text="补充描述").click()

    check_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    comment = "于 " + check_time +" 新增不合格检查记录。"
    text(comment,enter=False)
    
    check_item()
        
    poco(text="检查不合格",type="android.widget.Button").click()
    
    sleep(1)
    
    add_issue(0)

    touch((500,680)) #通过坐标点击最新一条检查记录
    
    assert_exists(Template(r"tpl1589819373127.png", record_pos=(0.005, -0.619), resolution=(1080, 2340)), "新增不合格成功")
    
    poco(name="转到上一层级").click()

#新增不合格检查，并发起问题    
def add_unqualified_issue():
    poco(text="新增检查记录").click()
    take_pic(2)
    sleep(1)    
    
    poco(text="补充描述").click()

    check_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    comment = "于 " + check_time +" 新增不合格检查记录。"
    text(comment,enter=False)
    
    false_item = check_item()
        
    poco(text="检查不合格",type="android.widget.Button").click()
    
    sleep(1)
    
    add_issue(1)
    
    

    
    

#任务列表页，搜索并选择任务   
def select_task(task_name):
    #等待刷新任务列表
    poco.wait_for_any(poco(type="androidx.recyclerview.widget.RecyclerView"))#等待任务列表
    
    #选择任务检查
    poco(text="请输入关键词").click()
    text(task_name,enter=False)
    
    poco(text=task_name,touchable=False).click()  #单纯对text匹配会匹配到输入框
    

#检查对象列表页，搜索并选择检查对象
def select_object(object_name):
    #等待刷新对象列表
    poco.wait_for_any(poco(type="androidx.recyclerview.widget.RecyclerView"))#等待对象列表

    #选择检查对象
    poco(text="请输入关键词").click()
    text(object_name,enter=False)
    object_match = '^' + object_name + '.*$'  #匹配以object_name开头的字符串
    poco(textMatches=object_match,type="android.widget.TextView").parent().click()

def safetyInspection():
    '''
    apk = "cn.smartinspection.combine"
    clear_app("cn.smartinspection.combine")
    print ("111111111111111111111111111111111")
    start_app(apk)
    '''
    
    #authApp()
    '''
    #login('kentestgrp10','12345678','p1','kentestgrp10')
    '''
    
    #start_app(apk)
    #login('kentest50','12345678','p1','kentest50')
    '''
    selectMode("组织架构聚合")
    selectOrg_0(org_name='公司1项目贰')
    selectApp("安全检查") 
    
    
    select_task(task_name="综合--每周--排查")
    select_object(object_name="消防箱A啊")
    
    add_qualified()
    add_unqualified()
    '''
    #add_unqualified_issue()
    create_issue('安全员')
    
        
def networdTest():
    #网络异常登录重试
    while poco(text="重试"):
        poco(text="重试").click()
        sleep(2)
    

'''

if __name__ == '__main__':
    
    threads = []

    t1 = threading.Thread(target=safetyInspection)
    threads.append(t1)

    t2 = threading.Thread(target=networdTest)
    threads.append(t2)
    
    
    for t in threads:
        t.setDaemon(True)
        t.start()
        
    for t in threads:
        print (t)
        t.join()
    
    print ("完成测试")

 '''  

threads = []

t1 = threading.Thread(target=safetyInspection)
threads.append(t1)

t2 = threading.Thread(target=networdTest)
threads.append(t2)


for t in threads:
    t.setDaemon(True)
    t.start()

for t in threads:
    print (t)
    t.join()

print ("完成测试")




#home_edit

#branch_test




