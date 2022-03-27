import psycopg2
import pandas as pd
import numpy as np
import config
import os

class pg_db:
    def __init__(self, host, db, usr, pwd):
        self.conn = None
        self.host = os.getenv(POSTGRES_GCP_IP)
        self.db = os.getenv(POSTGRES_GCP_DB)
        self.usr = os.getenv(POSTGRES_GCP_USER)
        self.pwd = os.getenv(POSTGRES_GCP_PW)
        self.conn_string = self.DbConnString()

    # CONNECTION
    def DbConnString(self):
        return "host = '{0}' dbname = '{1}' user = '{2}' password = '{3}'".format(self.host[0], self.database[0], self.user[0], self.password)

    def Connect2Postgres(self):
        self.conn = psycopg2(database = self.db, 
                             user = self.usr, 
                             password = self.pwd, 
                             host = self.host,
                             port = '5432')
        return 0

    def CommitClosePostgres(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
        return 0

    ## LOGGING
    # Every interaction with the API & db should be logged, will introduce lookup tables & FKs eventually
    def Log(self, _who, _status, _action_type, resource, is_connected = False, _curs = None):
        if self.conn is None or self.conn == None:
            self.ConnectToPostgres()
            with self.conn: #THINK I NEED TO REMOVE THIS
                with self.conn.cursor() as curs:
                    curs.execute(self.insert_log_config, self.insert_log_params)
            self.CommitClosePostgres()
        else:
            _curs.execute(self.insert_log_config, self.insert_log_params)
        return 0

    ## API
    # This is ultimately going to have to query a View
    def CheckApiThreshold(self):        
        self.ConnectToPostgres()  
        api_calls_15min = 0
        api_calls_1day = 0
        with self.conn: #THINK I NEED TO REMOVE THIS
            with self.conn.cursor() as curs:
                curs.execute(config.SELECT_API_HITS_15M) # TODO: switch to curs.callproc()
                api_calls_15min = curs.fetchall()
                curs.execute(config.SELECT_API_HITS_1D)
                api_calls_1day = curs.fetchall()
                
                if config.DEBUG: print("API Calls in past 15min: {0}".format(api_calls_15min[0][0]))
                if config.DEBUG: print("API Calls in past 1day: {0}".format(api_calls_1day[0][0])) 
                
        #Terminate the app if over the limit
        if (api_calls_15min[0][0] >= api_call_lim_15min) | (api_calls_1day[0][0] >= api_call_lim_1day):
            print("You exceeded the API limit for now, exiting.")
            self.exit()
            
        self.CommitClosePostgres()
        return api_calls_15min, api_calls_1day

    ## ATHLETE
    def InsertAthletes(self, activities_df:pd.DataFrame):
        try:
            self.ConnectToPostgres()
            
            cursor = self.conn.cursor() # Create a cursor
            
            for record in activities_df.itertuples(): # Loop through df, store each value in a temp var and then insert to postgres
                #athletes_values = (str(record.id), str(record.)) TODO
                cursor.execute(config.ATHLETES_INSERT, athletes_values)

            self.CommitCloseFromPostgres() # Commit the inserts to the db & close the connection
            return 0
        except:
            return 1

    ## ACTIVITIES
    def InsertActivities(self, activities_df:pd.DataFrame):
        try:
            self.ConnectToPostgres()
            
            cursor = self.conn.cursor() # Create a cursor
            
            for record in activities_df.itertuples(): # Loop through df, store each value in a temp var and then insert to postgres
                #activities_values = (str(record.id), str(record.)) TODO
                cursor.execute(config.ACTIVITIES_INSERT, activities_values)

            self.CommitCloseFromPostgres() # Commit the inserts to the db & close the connection
            return 0
        except:
            return 1

    ## STREAMS
    def GetActivitiesWithoutStreams(self):
        self.ConnectToPostgres()
        cursor = self.conn.cursor()
        cursor.callproc('GetActivitiesWithoutStreams') #TODO: build func in pg
        dt = cursor.fetchone()[0]
        return ids

    def InsertStreams(self, streams_df:pd.DataFrame):
        try:
            self.ConnectToPostgres()
            
            cursor = self.conn.cursor() # Create a cursor
            
            for record in streams_df.itertuples(): # Loop through df, store each value in a temp var and then insert to postgres
                #streams_values = (str(record.id), str(record.)) TODO
                cursor.execute(config.STREAMS_INSERT, streams_values)

            self.CommitCloseFromPostgres() # Commit the inserts to the db & close the connection
            return 0
        except:
            return 1