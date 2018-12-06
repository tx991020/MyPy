import re
import requests

r = requests.get('http://www.bsrtv.com/xw/ttgz/55010845.shtml')
s = '稿源：央视网 编辑：孙佩 发布时间：2017-09-15 15:31'
print(s.split('：'))
a = re.findall(r'[^:：\s]+[:：]([^\s]+)',"稿源：央视网 编辑：孙佩 发布时间：2017-09-15 15:31")
r.encoding = 'gbk2312'

c = '来源： 发布时间：2017-09-19 编辑：ynbsdst 点击量：114'
print(r.text)
d = re.findall(r'[^:：\s]+[:：]([^\s]+)', r.text)
print(d)
s2 = 'http:'
s1 = 'http://www.interoem.com/messageinfo.asp?id=35'
result1 = re.sub(r'[^:：\s]+[:：]([^\s]+)',lambda x : x.group(1),"稿源：央视网 编辑：孙佩 发布时间：2017-09-15 15:31")



