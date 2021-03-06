#!/usr/bin/env python
#coding:utf-8
"""
Author:  fiht --<fiht@qq.com>
  Purpose: 分发任务
  Created: 2016年06月09日
"""
import requests
import time
import os
# 服务器检查客户端的负载状态 如果客户端比较空闲 那么分发任务
# 采用web交互的方式
#----------------------------------------------------------------------
def sendTask(filename,url):
    """"""
    url = url+'/new'
    try:
        files = {'target':open(filename,'rb')}
        r = requests.post(url,files=files)
        print(r.text)
    except FileExistsError:
        print('错误 没有找到要传的文件,请检查')
#----------------------------------------------------------------------
def check_status(host):
    """查看服务器是否允许推送任务"""
    try:
        req = requests.get('%s/status'%host)
        if req.text == '1':
            return True
        elif req.text=='0':
            return False
    except TimeoutError:
        print('连接到%s超时'%host)
        return False
#----------------------------------------------------------------------
def main(host_list,target_dir):
    """对一个客户端"""
    import shutil
    file_list = os.listdir(path=target_dir)
    while(len(file_list)): # target_dir不为空的时候
        for host in host_list:
            if check_status(host):
                sendTask('%s/%s'%(target_dir,file_list[0]),host)
                print('成功发送一个任务-->%s'%file_list[0])
                shutil.move('./target/%s'%file_list[0],'hasChecked/')
                file_list.remove(file_list[0])
                time.sleep(2)
            else:
                print('节点 %s 正忙'%host)
                time.sleep(2)

if __name__=='__main__':
    #sendTask('/tmp/ips','http://localhost:5000/')
    #host = ['http://localhost:5000','http://nofiht.ml:5000','http://139.129.25.173:5000']
    host = ['http://localhost:5000']
    try:
        main(host,'./target')
    except Exception as e:
        print(e)
