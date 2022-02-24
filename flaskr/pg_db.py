import psycopg2
import pandas as pd
import numpy as np
import sql
import config

class pg_db:
    def __init__(self, host, db, usr, pwd):
        self.conn = None
        self.host = host
        self.db = db
        self.usr = usr
        self.pwd = pwd
        self.conn_string = self.DbConnString()

    # Makes a string to connect to the Postgres db based on values used to create the class
    def DbConnString(self):
        return "host = '{0}' dbname = '{1}' user = '{2}' password = '{3}'".format(self.host[0], self.database[0], self.user[0], self.password)

    def ConnectDb(self):
        self.conn = psycopg2.connect(self.conn_string)

    def CloseDb(self):
        self.conn.close()

    ## LOGGING
    # Every interaction with the API & db should be logged, will introduce lookup tables & FKs eventually
    def Log(self, _who, _status, _source, _action_type, _db_table, _db_column, _db_value, is_connected = False, _curs = None):
        # self.insert_log_params = (_who, _status, _source, _action_type, _db_table, _db_column, _db_value)
        if is_connected == False:
            self.ConnectDb()
            
            with self.conn:
                with self.conn.cursor() as curs:
                    
                    curs.execute(self.insert_log_sql, self.insert_log_params)

            self.CloseDb()
        else:
            _curs.execute(self.insert_log_sql, self.insert_log_params)

    ## API
    # This is ultimately going to have to query a View
    def CheckApiThreshold(self):        
        self.ConnectDb()
        
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(sql.SELECT_API_HITS_15M)
                self.api_calls_15min = curs.fetchall()
                curs.execute(sql.SELECT_API_HITS_1D)
                self.api_calls_1day = curs.fetchall()
                
                if self.verbose: print("API Calls in past 15min: {0}".format(self.api_calls_15min[0][0]))
                if self.verbose: print("API Calls in past 1day: {0}".format(self.api_calls_1day[0][0])) 
                
        #Terminate the app if over the limit
        if (self.api_calls_15min[0][0] >= self.api_call_lim_15min) | (self.api_calls_1day[0][0] >= self.api_call_lim_1day):
            print("You exceeded the API limit for now, exiting.")
            self.exit()
            
        self.CloseDb()
        return self.api_calls_15min, self.api_calls_1day

    ## ACTIVITIES
    # Pull Activity Ids from db to make sure dups arent inserted
    def GetActsActIds(self):
        db_act_ids = None
        self.conn = psycopg2.connect(self.conn_string)
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(sql.SELECT_ACTS_ACT_IDS)
                db_act_ids = curs.fetchall()
        
        self.CloseDb()
        #self.DbLog(self.athlete_name, config.SUCCESS, 'DB', 'SELECT', 'activities', 'Id', '')
        return db_act_ids

    #These results of a postgres query are returned as a tuple, parsing them into a 1d list to compare against db Activity Ids 
    #to make sure dups aren't inserted
    def ParseActsActIds(self, db_activity_ids): 
        act_ids = []
        for rec in db_activity_ids:
             act_ids.append(rec[0])     
        return act_ids                  
    
    #Insert activities from the Strava API into the Postgres CyclingStats db
    def InsertActivities(self, acts_df:pd.DataFrame, curr_acts_act_ids:list):
        #self.CheckApiThreshold()
        self.ConnectDb()
        with self.conn:
            with self.conn.cursor() as curs:
                # TODO: need to make sure at max __ records to not go over api limit
                for record in acts_df.itertuples():
                    #Make sure the Activity isnt already in the db
                    if record.id not in curr_acts_act_ids:
                        insert_params = (record.achievement_count, str(record.athlete), record.athlete_count, str(record.attribute_map), record.average_speed, record.average_watts, record.comment_count, record.commute, str(record.device_watts), str(record.discriminator), record.distance, record.elapsed_time, record.elev_high, record.elev_low, str(record.end_latlng), str(record.external_id), record.flagged, str(record.gear_id), record.has_kudoed, record.id, record.kilojoules, record.kudos_count, record.manual, str(record.map), record.max_speed, record.max_watts, record.moving_time, str(record.name), record.photo_count, record.private, record.start_date, record.start_date_local, str(record.start_latlng), str(record.swagger_types), str(record.timezone), record.total_elevation_gain, record.total_photo_count, record.trainer, str(record.type), record.upload_id, record.weighted_average_watts, record.workout_type)
                        curs.execute(sql.INSERT_ACTS_SQL, insert_params)
                        self.DbLog(self.athlete_name, config.SUCCESS, 'DB', 'INSERT', 'activities', 'id', record.id, True, curs)
                        if self.verbose == True: print('Inserted Activity {0} successfully'.format(str(record.id)))
                    else:
                        if self.verbose == True: print('Activity {0} already in the database'.format(str(record.id)))
        self.CloseDb()

    def acts_df_Setter(self, acts_df:pd.DataFrame):
        self.acts_df = acts_df