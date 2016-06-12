#!/usr/bin/env python
#coding:utf-8
"""
  Author:  fiht --<fiht@qq.com>
  Purpose: 一个简单的用来驱动sqlmap的客户端
  Created: 2016年06月09日
"""
from flask import Flask
from flask import request
from werkzeug.utils import secure_filename
from datetime import datetime
from subprocess import Popen
from subprocess import PIPE
from os import kill
from os import path
from simpleClass import subProc
from lib import check
app = Flask('client')
log_file = '/tmp/log/'
class_list = []
MAX_PROC = 8
password = 'c229c2520755767f'

#----------------------------------------------------------------------
@app.route('/info')
def get_info():
    """"""
    import psutil
    info = psutil.virtual_memory()
    mem_info = '总共内存:%.2fM 已用内存:%.2fM 占用比例:%s'%(info.total/(1014*1024),info.used/(1014*1024),info.percent)
    cpu_info = 'cpu核心数:%s cpu使用率:%s'%(psutil.cpu_count(),psutil.cpu_percent())
    return mem_info+'<br>'+cpu_info
#----------------------------------------------------------------------
def get_procNum(procName):
    """"""
    
    p = Popen('ps -ef | grep "%s" | wc'%procName,shell=True,stdout=PIPE)
    i  = p.stdout.readline()
    return int(i.decode().strip().split(' ')[0])-1
#----------------------------------------------------------------------
@app.route('/status',methods=['GET'])
def check_status(): # return 1 if can added
    global class_list
    """查看此时还能不能加入新c的任务"""
    procNum = get_procNum('sqlmap')
    print('现在有-->个任务',procNum)
    if procNum<MAX_PROC:
        print('可以添加')
        return '1'
    else:
        print('暂时还不可以添加')
        return '0'
                
#----------------------------------------------------------------------
@app.route('/new',methods=['POST'])
def get_task():
    global class_list
    f = request.files['target']
    print(request.files,'==')
    fname = './toScan/%s'%secure_filename(f.filename)
    log_name = './log/%s'%secure_filename(f.filename)
    if path.exists(fname):
        return "任务已经存在于我的服务器之中"
    f.save(fname)
    #pid = Popen('exec /home/fang/FromGithub/sqlmap/sqlmap.py -m %s --smart --threads 10 --batch '%(fname),shell=True,stdout=open('%s_log'%fname,'w+')).pid
    Popen('exec /home/fang/FromGithub/sqlmap/sqlmap.py -m %s --smart -v 0 --threads 10 --batch '%(fname),shell=True,stdout=open('%s_log'%log_name,'w+'))
#    class_list.append(subProc(pid,fname,datetime.now()))
    print('添加一个任务,系统当前状态为: %s'%get_info())
    return "success"
#----------------------------------------------------------------------
@app.route('/neaaaw',methods=['POST'])
def get_ff():
    """轻量级的测试方法"""
    f = request.files['target']
    fname = './toScan/%s'%secure_filename(f.filename)
    print(fname)
    log_name = './log/%s'%secure_filename(f.filename)
    if path.exists(fname):
        return '任务已经存在'
    f.save(fname)
    print('fname->%s log_file->%s'%(fname,log_name))
    Popen('echo %s >> %s'%(fname,log_name),shell=True)
    return '任务添加成功'
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
#    print(get_procNum('sqlmap'))
