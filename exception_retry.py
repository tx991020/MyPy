
#通用异常重试，主从备份,随机延时，心跳检测，使用主要靠思想

import logging
from tenacity import *

# import time
# def test(timeout,num):
# 	try:
# 		a = 1/0
# 		return a
# 	except Exception as e:
# 		print(e)
# 		time.sleep(timeout)
# 		if num > 0:
# 			return test(timeout, num-1)



import requests
from tenacity import *




#爬虫专用
def scraping(url):
    try:
        r = requests.get(url,timeout=3)
        return r.text
    except Exception as e:
        print(e)

        return Exception




#尝试5次，每次间隔1-2秒
@retry(stop=stop_after_attempt(5),wait=wait_random(min=1, max=2))
def feaching():
    raise scraping()



#尝试5次，每次间隔5秒
@retry(stop=stop_after_attempt(5),wait=wait.wait_fixed(5))
def feaching1():
    raise scraping()



#用法二，定时心跳检测
#每隔3秒请求一次
@retry(wait=wait.wait_fixed(3))
def ticker():
    print("haha")
    raise 1



if __name__ == '__main__':
   #feaching()
   ticker()

