#!/usr/bin/env python
#coding:utf-8
"""
  Author:  fiht --<fiht@qq.com>
  Purpose: 把sqlmap抽象成一个进程
  Created: 2016年06月09日
"""
from datetime import datetime
import os

if __name__ == '__main__':
    unittest.main()
########################################################################
class subProc:
    """一个sqlmap进程需要有的东西"""
    #----------------------------------------------------------------------
    def __init__(self,pid,file_name,start_time):
        """Constructor"""
        self.pid = pid
        self.file_name = file_name
        self.start_time = start_time
        self.log_file = '%s_log'%file_name
    #----------------------------------------------------------------------
    def get_time(self):
        """返回该进程执行的时间,以分钟的方式"""
        return (datetime.now() - self.start_time).seconds/60
    #----------------------------------------------------------------------
    def is_alive(self):
        """看看自己是不是还活着"""
        try:
            os.kill(self.pid,0)
            return True 
        except ProcessLookupError:
            print('%d-->进程不存在'%self.pid)
            return False
        except Exception as e:
            print('%d-->发现异常'%self.pid)
            print(e)
            return True
    #----------------------------------------------------------------------
    def __str__(self):
        """"""
        return self.pid