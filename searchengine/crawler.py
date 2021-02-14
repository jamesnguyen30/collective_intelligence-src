import sqlite3
import url_handler
from collective_intelligence.clustering import remove_text_noise
from bs4 import BeautifulSoup
import pyperclip
import json

_NOISE_PATTERN = "([\[[\d]+\])|([^\w\s\-])|(\d+)|(vte)" 


class Crawler:
    def __init__(self, dbname):
        self.dbname = dbname
        self.__db_connection = sqlite3.connect(self.dbname)
    
    def __del__(self):
        self.__db_connection.close()
    
    def dbcommit(self):
        self.__db_connection.commit()

    def crawl(self, urls, depth = 2):
        for i in range(depth):
            new_links = set()
            counter = 0
            total = len(urls)
            for url in urls:
                counter+=1
                if self.is_url_indexed(url):
                    continue
                else:
                    #load url and pass to BeautifulSoup
                    html = url_handler.load_raw_html('https://en.wikipedia.org' + url)

                    soup_obj = BeautifulSoup(html,'html.parser')
                    
                     #use this soup object to run index 
                    print("[{} / {}]-[DEPTH] = {} : {}".format( counter, total, i, url))
                    self.get_index_from_page(url, soup_obj)
                        
                    #find all the links in this page
                    #union old new_links and new new_links
                    new_links = new_links.union(self.get_links_from_url(soup_obj))

                    #save the new links from old links to the db
                    self.dbcommit()
            urls = new_links
    
    # parses the text and index it to the database
    # NOTE: Specically designed for wikipedia
    # Do not use to extract other pages
    def get_index_from_page(self, url, soup_obj):
        if self.is_url_indexed(url)==True:
                return
        
        # if not, get te text, split to words, and save every word as index to db
        desired_content = soup_obj.find('div', {'id':'mw-content-text'})
        if len(desired_content)>0:
            content = desired_content.find('div',{'class':'mw-parser-output'})
            # decompose the reference area in the page 
            # who has div class = "reflist columns references-column-width"
            for delete_div in content.find_all('div', {'class':'reflist columns references-column-width'}):
                delete_div.decompose()

            # remove other not-interested ares such as "Futher Reading", "Other Books", ...
            for delete_div in content.find_all('div', {'class':'refbegin columns references-column-width'}):
                delete_div.decompose()

            #remove the style tag
            for style in content.find_all('style'):
                style.decompose()
            
            # get all the text and lower it
            extracted_text = content.get_text().lower()

            #remove text noise: not-letter chars, numbers, brackets, ...
            cleaned_text = remove_text_noise.remove_with_pattern(_NOISE_PATTERN, extracted_text)
            
            #remove common words from the text
            cleaned_text = remove_text_noise.remove_common_words(cleaned_text)
            
            # split words in cleaned text
            words =cleaned_text.split()

            #get the id of this url
            urlid = self.get_entry_id('urllist','url',url)

            #link each word to this url
            #use i as a location
            for i in range(len(words)):
                word = words[i]
                wordid = self.get_entry_id('wordlist', 'word', word)

                #save new row to wordlocatoin
                self.__db_connection.execute("INSERT INTO wordlocation VALUES ({},{},{})".format(urlid, wordid, i))
        
    def get_entry_id(self, table, field, value, create_new = True):
        # the following statement is insecured,
        # for the purpose of running in local machine is perfectly fine
        # but this potentially expose the db to SQL Injection attack 
        # if deployed in business enviroment
        cursor = self.__db_connection.execute("SELECT rowid FROM {} WHERE {}='{}'".format(table, field, value))

        entry_id = cursor.fetchone()
        if entry_id == None:
            # create new row
            cursor = self.__db_connection.execute("INSERT INTO {} ({}) VALUES ('{}')".format(table,field,value))
            return cursor.lastrowid     
     
        else:
            return entry_id[0]

    def is_url_indexed(self, url):
        #check is this url in database already
        try:
            cursor = self.__db_connection.execute("SELECT rowid FROM urllist WHERE url='{}'".format(url))
        except sqlite3.OperationalError as e:
            print("[ERROR] {}".format(str(e)))
            return True
        a = cursor.fetchone()
        if a!=None:
            #if the url is in the database, check if it has been crawled 
            # this is a safe check, ideally, url should be saved after hava been crawled
            cursor = self.__db_connection.execute("SELECT * FROM wordlocation WHERE urlid={}".format(a[0]))
            b = cursor.fetchone()
            if b!=None:
                return True
        return False

    # this returns a new list of urls to index
    def get_links_from_url(self, soup_obj):
        ''' returns a set of new links '''
        _IGNORE_LINKS=['ISBN', 'BNE', 'BNF', 'GND', 'HDS', 'LCCN', 'Article', 'Read', "", 'Main page']
        new_urls = set()
        contents = []

        links = soup_obj('a')
        for link in links:
            href = link.get('href')

            # get the text of the element
            content = link.text
            contents.append(content)
            
            # there some links in the /wiki/ABC fomat but we don't want 
            # such as the link to the main page
            if content in _IGNORE_LINKS:
                continue

            # check if href found and starts with format: '/wiki/ABC
            # it's the link we want
            # if after wiki, there's a :, that is  not what we want
            # and href must not exists in new_urls since we don't want to have identical links to crawl
            if href!=None and href.startswith("/wiki/") and href.find(':')==-1 and href not in new_urls:
                new_urls.add(href)

        return new_urls

    # recursively get the text in the element and go to sub elements    
    
    # def extract_text(self, soup_obj):
    #     '''returns string as extracted text'''
    #     text = soup


    def save_to_link_words_table(self, from_url, to_url, content):
        pass
        
    def drop_all_tables(self):
        #drop the tables
        self.__db_connection.execute("drop table urllist")
        self.__db_connection.execute("drop table wordlist")
        self.__db_connection.execute("drop table wordlocation")
        self.__db_connection.execute("drop table link")
        self.__db_connection.execute("drop table linkwords")
        # #drop index tables
        # self.__db_connection.execute("drop index urllistidx on urllist")
        # self.__db_connection.execute("drop index wordlocationidx on wordlocation")
        # self.__db_connection.execute("drop index wordidx on wordlist")
        # self.__db_connection.execute("drop index urltoidx on link")
        # self.__db_connection.execute("drop index urlfromidx on link")
        
    def execute_sql(self, statement):
        ''' returns a cursor '''
        cursor = self.__db_connection.execute(statement)
        return cursor

    def create_tables(self):
        try:
            self.__db_connection.execute("create table urllist(url text)")
            self.__db_connection.execute("create table wordlist(word text)")
            self.__db_connection.execute("create table wordlocation(urlid integer, wordid integer, location integer)")
            self.__db_connection.execute("create table link(fromid integer, toid integer)")
            self.__db_connection.execute("create table linkwords(wordid integer, linkid integer)")
            #create index tables
            self.__db_connection.execute("create index urllistidx on urllist(url)")
            self.__db_connection.execute("create index wordlocationidx on wordlocation(wordid)")
            self.__db_connection.execute("create index wordidx on wordlist(word)")
            self.__db_connection.execute("create index urltoidx on link(toid)")
            self.__db_connection.execute("create index urlfromidx on link(fromid)")
            self.__db_connection.commit()
        except sqlite3.OperationalError as e:
            print('ERROR : {}'.format(e))

    

    