from pymongo import MongoClient
import datetime
import pprint
import config
import time

class mongo_db:
    def __init__(self):
        self.client = None
        self.db = None
        self.log_coll = None
        self.apilog_coll = None
        self.acts_coll = None

    def ConnectDb(self, db='cyclestats'):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[db]
        # establish connection to relevant connections
        self.log_coll = self.db['log']
        self.apilog_coll = self.db['apilog']
        self.acts_coll = self.db['acts']

    ## LOGGING
    def Log(self, who, status, source, destination, misc) -> str:
        # TODO: check to make sure connected first
        if self.log_coll == None:
            self.log_coll = self.db['log']
        log = {'who' : who, 
               'status' : status, 
               'source' : source, 
               'destination' : destination, 
               'misc' : misc}
        return self.log_coll.insert_one(log).inserted_id

    ## API 
    def ApiLog(self):
        if self.apilog_coll == None:
            self.apilog_coll = self.db['apilog']

        apilog = {"timestamp" : datetime.datetime.now(), "hits" : 1}

        self.apilog_coll.insert_one(apilog)

    def CheckApiThreshold(self) -> dict:
        hour = 0
        day = 0
        # TODO: recode this using agg func native to mongodb
        for j in self.apilog_coll.find({}, {'_id':0, "timestamp":1}):
            # HOURLY LIMIT
            if j['timestamp'] + datetime.timedelta(hours=1) >= datetime.datetime.now():
                hour += 1

            # DAILY LIMIT
            if j['timestamp'] + datetime.timedelta(days=1) >= datetime.datetime.now():
                day += 1
        print("Hits within the past hour: {0}".format(hour))
        print("Hits within the past day: {0}".format(day))
        
        return {'hour': hour, 'day': day}

    ## ACTIVITIES
    def GetActsActIds(self):
        return self.acts_coll.find({}, {'_id':0, "id":1}).distinct()

    def InsertActs(self, acts_dict, curr_acts_act_ids):
        if curr_acts_act_ids == None:
            print("curr_acts_act_ids is None")
            print(type(acts_dict, ' is the type of acts-dict'))
            self.acts_coll.insert_many(acts_dict)

    ## STREAMS

        
## TESTING
test = mongo_db()
test.ConnectDb()
test.CheckApiThreshold()




