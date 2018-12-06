from pyspider.libs.base_handler import *
import time


class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            "Connection": "close",
            'content-type': 'application/json',

            "Host": "apiparty.xinhuaapp.com",
            "User-Agent": "Paw/3.1.4 (Macintosh; OS X/10.11.6) GCDHTTPRequest",
            "Cookie": "acw_tc=AQAAANfF0ml/bgkABoR/fKcQqC4OuXeK; aliyungf_tc=AQAAAC1BQB9W0wcABoR/fI6cxwrGgA4+",
            "Token": "88ac4b4e55b7c254d6c37da1b4e49465b9b6e6fcb80745c4186df7165c4adbe15a229b52af87e1bade19111bb3d9a44bb93f5b17d50196c637df570ffda04e4d1511922785765",
        },
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.yxtv.cn/portal.php?mod=list&catid=194';, callback = self.index_page)

        @config(age=24 * 60 * 60)
        def index_page(self, response):
            for each in response.doc('.portal_block_summary > p > a').items():
                self.crawl(each.attr.href, callback=self.index_page1)

        @config(priority=2)
        def index_page1(self, response):

            for each in response.doc('dl').items():
                self.crawl(each('dt a').attr.href, callback=self.detail_page, save={'img': each('img').attr.src},
                           fetch_type='js', js_script='''
               function() {
                   return flashvars["f"]
               }
               ''')
            next = response.doc('.nxt').attr.href
            self.crawl(next, callback=self.index_page1)

        @config(priority=10)
        def detail_page(self, response):
            try:
                a = re.findall(r'编辑：(\S*)', response.text)[0]
                print(a)
            except:
                a = ''
            try:
                t = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', response.text)[0]
                s = time.mktime(time.strptime(t, "%Y-%m-%d %H:%M:%S"))
                print(s)
            except:
                s = time.time()

            try:
                vurl = response.js_script_result[0].replace('->video/mp4', '')
                print(vurl)
            except:
                vurl = ''

            tag1 = response.doc('.b02 > a').text()
            tag = tag1.split()
            print(tag)
            try:
                b = tag[1]
                c = tag[2]
                d = b + ";" + c
            except:
                b, c, d = '', '', ''

            return {
                       "url": response.url,
                       "project": self.project_name,
                       "program_name": response.doc('title').text(),
                       "content": "",
                       "actor": "",
                       "spider_time": time.time(),
                       "poster": response.save['p'],
                       "create_time": time.time(),
                       "publish_time": s,
                       "director": "",
                       "author": a,
                       "source": "云南网络广播电视台",
                       "accountcode": "15_STWZ_YNTVCN_00_530000",
                       "video_url": vurl,
                       "root_column_name": b,
                       "root_column_id": "",
                       "column_id": "",
                       "column_name": c,
                       "program_id": "",
                       "tags": d,
                   "episode": 1
            }


