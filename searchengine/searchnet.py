import sqlite3
import math

def dtanh(x):
    return 1.0 - x**2

class SearchNet:
    def __init__(self, dbpath):
        self.__db_connection = sqlite3.connect(dbpath)
        #check if table exists

        self._WORD_LAYER = 0
        self._URL_LAYER =1      

        self.HIDDEN_WORD_TABLE = "hiddenword"
        self.HIDDEN_URL_TABLE = "hiddenurl"
        self.HIDDEN_NODE_TABLE ="hiddennode"
    
        self.create_table()

    def __del__(self):
        self.__db_connection.close()
    
    def execute_sql(self, statement):
        ''' returns a cursor '''
        cursor = self.__db_connection.execute(statement)
        return cursor 
    def dbcommit(self):
        self.__db_connection.commit()
    
    def create_table(self):
        try:
            self.execute_sql("create table {}(create_key text)".format(self.HIDDEN_NODE_TABLE))
            self.execute_sql("create table {}(fromid integer, toid integer, strength integer)".format(self.HIDDEN_WORD_TABLE))
            self.execute_sql("create table {}(fromid integer, toid integer, strength integer)".format(self.HIDDEN_URL_TABLE))
            self.dbcommit()
        except sqlite3.OperationalError as e:
            print(e)
    
    def drop_all_tables(self):
        try:
            self.execute_sql("drop table hiddennode")
            self.execute_sql("drop table hiddenword")
            self.execute_sql("drop table hiddenurl")
            self.dbcommit()
        except sqlite3.OperationalError as e:
            print(e)
        
    def get_strength(self, fromid, toid, layer):
        default_value = 0.0
        table_name = ""
        if layer == self._WORD_LAYER:
            table_name = self.HIDDEN_WORD_TABLE
            default_value = -0.2
        else:
            table_name = self.HIDDEN_URL_TABLE
            default_value = 0.0
        value = self.execute_sql("select strength from {} where fromid={} and toid={}".format(table_name, fromid, toid)).fetchone()
        if value == None:
            return default_value
        else:
            return value[0]

    def set_strength(self, fromid, toid, strength, layer,create_new=True):
        table_name = ""
        if layer == self._WORD_LAYER:
            table_name = self.HIDDEN_WORD_TABLE
        else:
            table_name = self.HIDDEN_URL_TABLE
        row = self.execute_sql("select rowid from {} where fromid={} and toid={}".format(table_name, fromid, toid)).fetchone()

        if row == None:
            if create_new:
                self.execute_sql("insert into {} values ({},{},{})".format(table_name, fromid, toid, strength))
        else:
            rowid = row[0]
            self.execute_sql("update {} set strength={} where rowid={}".format(table_name, strength, rowid))

    def generate_hidden_node(self, wordids, urlids):
        if len(wordids)<=3:
            create_key = "_".join(sorted([str(wordid) for wordid in wordids]))
            row = self.execute_sql("select rowid from {} where create_key='{}'".format(self.HIDDEN_NODE_TABLE, create_key)).fetchone()

            if row == None:
                # create a new node
                row = self.execute_sql("insert into {} values ('{}')".format(self.HIDDEN_NODE_TABLE, create_key))
                rowid = row.lastrowid
                for wordid in wordids:
                    self.set_strength(wordid, rowid, 1/len(wordids), self._WORD_LAYER)
                
                for urlid in urlids:
                    self.set_strength(rowid, urlid, 0.1, self._URL_LAYER)

                self.dbcommit()
        
    def get_relevant_hidden_ids(self, wordids, urlids):
        nodes = set()
        for wordid in wordids:
            rows = self.execute_sql("select toid from {} where fromid={}".format(self.HIDDEN_WORD_TABLE, wordid))
            for row in rows:
                nodes.add(row[0])
        for urlid in urlids:
            rows = self.execute_sql("select fromid from {} where toid={}".format(self.HIDDEN_URL_TABLE, urlid))
            for row in rows:
                nodes.add(row[0])
        return nodes

    def setup_network(self, wordids, urlids):
        ''' set up network for a specific query'''
        #value lists
        self.wordids = wordids
        self.urlids = urlids
        self.hiddenids = self.get_relevant_hidden_ids(wordids, urlids)
        
        #node ouputs, 'a' stands for activation
        self.a_input = [1.0]*len(wordids)
        self.a_hidden = [1.0]*len(self.hiddenids)
        self.a_ouput = [1.0]*len(urlids)

        #create weights matrix
        self.weight_input = [[self.get_strength(wordid, hiddenid, self._WORD_LAYER)
                                for hiddenid in self.hiddenids] for wordid in self.wordids]
        self.weight_output = [[self.get_strength(hiddenid, urlid, self._URL_LAYER) 
                                 for urlid in self.urlids] for hiddenid in self.hiddenids]
        
    def feed_foward(self):
        
        for i in range(len(self.wordids)):
            self.a_input[i] = 1.0
        
        for j in range(len(self.hiddenids)):
            sum = 0
            for i in range(len(self.wordids)):
                sum += self.a_input[i] * self.weight_input[i][j]
            self.a_hidden[j] = math.tanh(sum)
        
        for j in range(len(self.urlids)):
            sum = 0
            for i in range(len(self.hiddenids)):
                sum += self.a_hidden[i] * self.weight_output[i][j]
            self.a_ouput[j] = math.tanh(sum)

        return self.a_ouput

    def get_result(self, wordids, urlids):
        self.setup_network(wordids, urlids)
        return self.feed_foward()
        
    #backpropagation is not implemented yet
    #because furthur understanding in neuron network is required
    #NOTE Implement backpropagation here

        
        





        