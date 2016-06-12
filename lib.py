import os
#----------------------------------------------------------------------
def check(pid):
    """查看是否有这个进程"""
    try:
        os.kill(pid,0)
    except ProcessLookupError:
        return False
    finally:
        return True