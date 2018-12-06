#统计必备，节省一万行代码
#pandas 聚合统计得出结果再转为python的dict

import pandas as pd
import json

b = [{'source': 'baidu', 'num': 61}, {'source': 'cctv', 'num': 14}, {'source': 'cntv', 'num': 3}, {'source': 'cntv', 'num': 1}, {'source': 'cntv', 'num': 1}]

if __name__ == '__main__':

    df =pd.DataFrame(b)

    c = df["num"].groupby(df['source']).sum()[:5]

    gg = pd.DataFrame(c)
    pandas_to_dict = gg.to_dict()
    pandas_to_json = gg.to_json()