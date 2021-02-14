import sqlite3
import pyperclip
import math

class Searcher:
    
    def __init__(self, dbname):
        self.dbname = dbname
        self.__db_connection = sqlite3.connect(self.dbname) 
        
    def __del__(self):
        self.__db_connection.close()

    def execute_sql(self, statement):
        ''' returns a cursor '''
        cursor = self.__db_connection.execute(statement)
        return cursor

    # NOTE: this function will returns an error 
    # if the query has a wrong spelling words because
    # that word is not in the database
    # will fix this later
    def run_query(self, query, sort_result=True):
        #get matched rows
        rows, wordids = self.get_matched_rows(query)

        #get scored list
        scores = self.get_scored_list(rows, wordids)

        #sort the result
        if sort_result:
            sorted_result = sorted([(score, urlid) for urlid, score in scores.items()], reverse=True)
            return sorted_result

        #display the result
        return scores

    def get_matched_rows(self,query):
        
        #construct an SQL statement : 
        # ex: 
        # SELECT w0.urlid, w0.location, w1.location
        # FROM wordlocation w0, wordlocation w1
        # WHERE w0.urlid = w1.urlid
        # AND w0.wordid = 10
        # AND w1.wordid = 18
        query = query.lower().strip()
        words = query.split()
        wordids = []
        # get word ids
        for word in words:
            cursor = self.execute_sql("select rowid from wordlist where word='{}'".format(word))
            wordid = cursor.fetchone()[0]
            wordids.append(wordid)

        number_of_words_in_query = len(words)
        select_clause="w0.urlid,"
        from_clause=""
        identical_urlid_condition_clause=""
        wordid_condition_clause=""
        for i in range(number_of_words_in_query):
            select_clause+="w{}.location,".format(i)
            from_clause+="wordlocation w{},".format(i)
            if i < number_of_words_in_query-1:
                identical_urlid_condition_clause+=" w{}.urlid = w{}.urlid and".format(i, i+1)
            wordid_condition_clause+=" w{}.wordid = {} and".format(i, wordids[i])
        
        select_clause = select_clause[:-1]
        from_clause = from_clause[:-1]
        if number_of_words_in_query <=1: 
            identical_urlid_condition_clause = ""
        wordid_condition_clause = wordid_condition_clause[:-4]

        sql_statement = "select {} from {} where {}{}".format(select_clause, from_clause, identical_urlid_condition_clause, wordid_condition_clause)
        
        rows = self.execute_sql(sql_statement).fetchall()

        return rows, wordids 

    def get_scored_list(self, rows, wordids):
        # the weight of frequency is 1.0
        # the weight of location is 1.5
        # ...
        weights = [
                    (1.0,self.frequency_ranking(rows)),
                    (1.5,self.location_ranking(rows)),
                    (1.5,self.word_distance_ranking(rows))
                    ]

        total_score = dict([(row[0],0) for row in rows])
        for (weight, scores) in weights:
            for url in total_score:
                total_score[url]+=weight*scores[url]
        
        return total_score
    
    def normalize_score(self, scores_dict, smaller_is_better=False):
        ''' returns a dict format: { urlid : normalized_score }'''
        vsmall = 0.000001
        if smaller_is_better:
            min_value = min(scores_dict.values())
    
            return dict([(item, min_value/ max(vsmall, score)) for item, score in scores_dict.items()])
        else:
            max_value = max(scores_dict.values())
    
            if max_value<=0:
                max_value = vsmall
            return dict([(item, score/ max_value) for item, score in scores_dict.items()])
    
    def frequency_ranking(self, rows, normalized = True):
        # initiate the counts dict
        # returns dict with format:
        # { urlid : count_reference}
        counts = dict()
        for row in rows:
            counts.setdefault(row[0],0)
            counts[row[0]]+=1
        if normalized:
            return self.normalize_score(counts)
        else:
            return counts

    def location_ranking(self, rows, normalize_score = True):
        # The relevant based on the total distance of the query words
        # the smaller the distance, the better
        
        locations = dict()
        INF = math.inf
        for row in rows:
            location_temp = sum(row[1:])
            locations.setdefault(row[0], INF)
            if locations[row[0]]>location_temp:
                locations[row[0]]=location_temp
        if normalize_score:
            return self.normalize_score(locations, smaller_is_better=True)
        return locations

    def word_distance_ranking(self, rows, normalize_score = True):
        # if just one word was queried, return the 1.0 score for every url
        if len(rows[0]) <2:
            return dict([(row[0], 1.0) for row in rows])

        else:
            INF = math.inf
            distances = dict()
            row_len = len(rows[0])
            for row in rows:
                distance_temp = sum([abs(row[i] - row[i-1]) for i in range(2,row_len)])
                distances.setdefault(row[0], INF)
                if distances[row[0]] > distance_temp: 
                    distances[row[0]] = distance_temp
            return self.normalize_score(distances, smaller_is_better=True)
                
    
    def display_query_result_to_most_relevant(self, query_result, number_of_results = 10):
        ''' query_result is an array with format [ ( score, urlid ), ... ]'''
        total_result = len(query_result)
        top_results=query_result[:10]
        
        print("10 in {} results :".format(total_result))
        for (score, urlid) in top_results:
            #get url string in database
            url_string = self.execute_sql("select url from urllist where rowid={}".format(urlid)).fetchone()
            print("{} - {}".format(url_string, score))
        







            

        




