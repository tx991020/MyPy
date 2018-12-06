from apscheduler.schedulers.blocking import BlockingScheduler
import apscheduler.events
#需要引用日志
from log_demo import get_log
err_logger = get_log()


def err_listener(ev):
    #异常监听
    if ev.exception:
        err_logger.exception('%s error.'%(str(ev.jobstore)))
    else:
        err_logger.info('%s miss'%(str(ev.job_id)))


def days():
    #每天
    pass
def minutes():
    #每分钟
    print("hahha")
def always():
    #直接运行
    print("1234")
def hours1():
    #每小时
    pass


if __name__ == '__main__':
    sched = BlockingScheduler()
    #天
    sched.add_job(days, 'interval', days=1, start_date='2017-01-01 00:07:00')
    #分钟 范围(0-59)
    sched.add_job(minutes, 'interval', minutes=1, start_date='2017-01-01 00:07:00')
    #小时
    #直接运行
    sched.add_job(always)

    try:
        print('开始咯')
        sched.add_listener(err_listener,
                           apscheduler.events.EVENT_JOB_ERROR | apscheduler.events.EVENT_JOB_MISSED | apscheduler.events.EVENT_JOB_EXECUTED)
        sched.start()
    except Exception as ex:
        err_logger.info(ex)
