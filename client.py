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
@app.route('/status',methods=['GET'])
def check_status(): # return 1 if can added
    global class_list
    """查看此时还能不能加入新c的任务"""
    for i in class_list: # 要是子进程已经折腾完了 那么从proc_dic里面把它删除掉
        if i.is_alive(): # 进程存在 
            if i.get_time() > 60: # 耗费的时间大于六十分钟的话
                kill(i.pid,9) # 杀死进程..不知道能不能杀死反正我已经杀了..
                class_list.remove(i)
                print('强行杀死了一个进程')
        else:
            class_list.remove(i) # 进程不存在 说明执行完毕了
            print('发现一个进程已经完了.')
    print('现在有-->个任务',len(class_list))
    if len(class_list)<MAX_PROC:
        print('可以添加')
        return '1'
    else:
        print('暂时还不可以添加')
        return '0'
                
#----------------------------------------------------------------------
@app.route('/new',methods=['POST'])
def get_task():
    global class_list
    try:
        f = request.files['target']
        print(request.files,'==')
        fname = '/tmp/t/%s'%secure_filename(f.filename)
        if path.exists(fname):
            return "任务已经存在于我的服务器之中"
        f.save(fname)
        pid = Popen('exec /home/fang/FromGithub/sqlmap/sqlmap.py -m %s --smart --threads 10 --batch '%(fname),shell=True,stdout=open('%s_log'%fname,'w+')).pid
        print('添加前-->%d  class list-->'%len(class_list))
        class_list.append(subProc(pid,fname,datetime.now()))
        print('添加后-->%d  class list-->'%len(class_list))
        #proc_dic[pid]=datetime.now()#.strftime('%H%M%S') # 时分秒 用来测试数据
        #Popen('ping www.baidu.com',shell=True)
        #Popen('wget http://localhost:5000/c229c2520755767f/',shell=True)
        #Popen('cat %s'%fname,shell=True)
        return "success"
    except EOFError:
        return '服务器返回了一个错误:->%s'%str(e)

if __name__ == '__main__':
    app.run(debug=True)