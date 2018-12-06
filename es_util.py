from elasticsearch import Elasticsearch
from elasticsearch import helpers

class ESutill():
    def __init__(self,hosts,index,doc_type,body):
        self.index = index
        self.body = body
        self.doc_type = doc_type
        self.hosts = hosts
        self.es = Elasticsearch(hosts=self.hosts)
        if not self.es.indices.exists(index=self.index):
            self.es.indices.create(index=self.index)
            self.es.indices.put_mapping(index=self.index,doc_type=self.doc_type,body=self.body)

    # mapping 示例
    """
    self.es.indices.put_mapping(
        index=self.index,
        doc_type="spider_status",
        body={
            "_all": {
                "enabled": True  #准许动态插入
            },
            "properties": {
                "table_name": {
                    "type": "keyword"
                },
                "source": {
                    "type": "keyword"
                },
                "monitoring_time": {
                    "type": "date",
                    "format": "epoch_second"
                },
                "total_count": {
                    "type": "long"
                },
                "new_count": {
                    "type": "long"
                }
            }
        })
    """
    #批量插入
    def put_data(self, inputdata):
        """
        批量传入数据---写入数据库
        :param inputdata: [] 列表数据
        :return: 无
        """
        helpers.bulk(self.es, inputdata)
        self.es.indices.refresh(index=self.index)

    #hits查询
    def hits_search(self,body):

        #es 无脑操作填空模板
        #111#简单查询
        """
        GET/products/p/ _search
        {
            "query": {
            }
        }

        GET / products / p / _search
        {
            "query": {
                "match": {
                    "title": "北京"
                }
            }
        }
        GET / products / p / _search
        {
            "query": {
                "multi_match": {
                    "query": "北京",
                    "fields": ["title", "tag"]
                }
            }
        }

        GET / products / p / _search
        {
            "query": {
                "range": {
                    "price": {
                        "gte": 1000,
                        "lt": 2000
                    }
                }
            }
        }

        GET / products / p_search
        {
            "query": {
                "term": {
                    "tag": "北京"
                }
            }
        }

        GET / products / p / _search
        {
            "query": {
                "exists": {
                    "field": "comment"  #是否存在comment 这一列
                }
            }
        }

    """
        #222
        #bool 组合查询
        #例如搜索 苍井空北京
        #term 精确匹配，中间不能有空  所得结果 "苍井空北京"
        # es5.X  should, must，mustnot, filter 同级

        # match/term/terms,matchall,range 同级




        body = {
            "_source": {
                "includes": []
            },
            "query": {
                "bool": {
                    "should": [{
                        "term": {
                            "title": "标题是 XXX中东XXX 一定匹配的就是中东"
                        }
                    }, {
                        "match": {
                            "title": "标题是 XXX中东XXX 由于分词影响分词后可能匹配上 中 或 东 或 中XXX东"
                        }
                    }, {
                        "terms": {
                             "field" : "make",

                            "exclude" : ["rover", "jensen"]
                        }
                    }],
                    "must": [{
                        "term": {
                            "cpu_status": 0
                        }
                    }, {
                        "match": {
                            "title": "标题中含北京的"
                        }
                    }, {
                        "terms": {
                            "memory_status": 0
                        },
                    }, {
                        "match_all": {

                        },
                    }, {
                         "range": {
                            "monitoring_time": {
                                "gt": "大于",
                                "lt": "小于",
                                "format": "epoch_second"
                            }
                        }
                    }

                    ],
                    "mustnot": [{
                        "term": {
                            "cpu_status": 0
                        }
                    }, {
                        "match": {
                            "swap_status": 0
                        }
                    }, {
                        "terms": {
                            "memory_status": 0
                        }
                    }],
                    "filter": [{
                        "term": {
                            "cpu_status": 0
                        }
                    }, {
                        "must": {
                            "swap_status": 0
                        }
                    }, {
                        "mustnot": {
                            "memory_status": 0
                        }
                    }],
                }
            },
            "size":10,
            "sort": [
                {"publish_time": {"order": "desc"}},
            ],
        }
        try:

            data_es = self.es.search(index=self.index, doc_type=self.doc_type, body=self.body)
            result_es = data_es["hits"]["hits"]
            return result_es
        except:
            return None

        #333
        #分组聚合

        #分组聚合需要分组策略
        #1按照固定区间
        #按照自定义区间
        #过滤聚合
        #分组聚合可以有子聚合，可以嵌套

        #1按值分组 terms
        #按直方图分组 histogram 定义区间，date_histogram 日期区间
        #范围聚合 range , data_range

        #过滤聚合 filter,filters

        #aggs聚合查询
        def aggs_search(self,body):
            query_abnormal = {

                "size": 0,   #忽略详细内容，只返回聚合结果 max,min，avg,value_count(count(*)), cardinality(count(distinct(**)))
                "query": {
                    "bool": {
                        "must": [{
                            "match_all": {}
                        }, {
                            "range": {
                                "monitoring_time": {
                                    "gt": "大于",
                                    "lt": "小于",
                                    "format": "epoch_second"
                                }
                            }
                        }],
                        "must_not": []
                    }
                },
                "_source": {
                    # 填排除哪些列
                    "excludes": []
                },
                "aggs": {
                    #此处为填空题
                    "groupby spider_time as nickname(按 filed 里面 的spider_time  分组，给分组 取一个别名)": {
                        #以日期直方图显示
                        "date_histogram": {
                            "field": "spider_time", # 填列名，按列分组聚合
                            "interval": "1d",
                            "time_zone": "Asia/Shanghai",
                            "min_doc_count": 1
                        },
                        "aggs": {
                            # 此处为填空题
                            "groupby price as nickname(按照 filed 里面 的price   分组，给分组 取一个别名)": {
                                #平均值
                                "avg": {
                                    "field": "price", #填列名，按列分组聚合
                                    "size": 1000,    # 返回多少个
                                    "order": {
                                        "time(填XX列)": "desc"  # 按照XX列 排序
                                    }
                                },

                            }
                        }
                    }
                }
            }


            try:

                data_es = self.es.search(index=self.index, doc_type=self.doc_type, body=self.body)

                #示范  返回哪个桶的值
                result_es = data_es["aggregations"]["groupby spider_time as nickname(填桶的别名)"]["buckets"]
                return result_es
            except:
                return None
