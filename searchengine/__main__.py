import sys
sys.path.append("./")
from crawler import Crawler
from searcher import Searcher
from searchnet import SearchNet
import url_handler
from bs4 import BeautifulSoup
import time

from collective_intelligence.recommendation import file_io


_DATSET_PATH = './dataset/wiki_pages/'
_DATABASE_PATH = "./collective_intelligence/searchengine/database/"

def read_urls(path):
    urls = []
    with open(path, 'r') as file:
        urls = file.readlines()
    return urls

if __name__ == "__main__":
    urls = read_urls(_DATSET_PATH + 'wiki_url')
  
#   NOTE: the crawler already run once
    # crawler = Crawler(_DATABASE_PATH +"index.db")

    # crawler.create_tables()

    # crawler.crawl(urls)

    #NOTE: crawler experiments are here
    # cursor = crawler.execute_sql("select rowid from wordlocation where wordid=1")
    # result = cursor.fetchall()

    # cursor = crawler.execute_sql("select * from wordlocation where wordid=1")
    # rows = cursor.fetchall()

    # print(result[:10])
    # print(rows[:10])

    #NOTE searcher experiements here
    # searcher = Searcher(_DATABASE_PATH)

    # init_time = time.time()
    # result = searcher.run_query("theoretical computer")
    # searcher.display_query_result_to_most_relevant(result)
    # end_time = time.time() - init_time
    # print("\nElapsed time {0:2f} sec".format(end_time))


    #NOTE searchnet experiments here
    searchnet = SearchNet(_DATABASE_PATH + "searchnet.db")

    # searchnet.drop_all_tables()

    # searchnet.execute_sql("insert into hiddenword values (1,144,113)")
    # searchnet.execute_sql("insert into hiddenurl values (122,11314,12)")
    # searchnet.dbcommit()

    # searchnet.drop_all_tables()
    # searchnet.update_strength(2,144,223,searchnet._WORD_LAYER)
    # searchnet.dbcommit()
    # wordids = [2,3,4]
    # urlids = [2,3,4,5]
    # searchnet.generate_hidden_node(wordids, urlids)
    # nodes = searchnet.get_relevant_hidden_ids(wordids, urlids)
    
    # result = searchnet.get_result(wordids, urlids)
    # print(result)
    
    
