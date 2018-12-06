# pandas json 转sql，直接存入mysql

import requests
import pandas as pd
from sqlalchemy import create_engine

yconnect = create_engine('mysql+pymysql://root:123456@localhost:3306/video?charset=utf8')


if __name__ == '__main__':
    url = "http://app.video.baidu.com/app?word=北京&pn=1&rn=50&order=1"

    r = requests.get(url)
    data = r.json()["result"]
    df = pd.DataFrame(data)

    del df['nsclick_v']
    # 表名baidu,数据库名video, 如果表以存在，追加数据
    pd.io.sql.to_sql(df, 'baidu', yconnect, schema='video', if_exists='append')