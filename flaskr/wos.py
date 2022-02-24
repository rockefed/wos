import pg_db
import api

class cyclestats:
    def __init__(self):
        self.mongodb = None
        self.pg_db = None
        self.api = None

        self.acts_df = None
        self.athlete_df = None
        self.streams_df = None

        self.api_acts_act_ids = None
        self.db_acts_act_ids = None

    def Connect2Postgres(self, host, db, usr, pwd):
        self.pg_db = db.db(host, db, usr, pwd)

    def Connect2Mongo(self):
        self.mongodb = self.mongodb.ConnectDb()

    def EstablishApiConnection(self):
        self.api = self.api.Connect2Api(token='')

    def CheckApiThreshold(self):
        hits = self.mongodb.CheckApiThreshold()
        if hits['hour'] >= 100:
            return '{0} hits in the past hour'.format(hits['hour'])
        if hits['day'] >= 1000:
            return '{0} hits in the past hour'.format(hits['day'])
        return True

    def GetAthleteFromApi(self):
        pass

    def GetActivitiesFromApi(self):
        # LOG START
        self.acts_df = self.api.Activities2DF(self.api.GetActivities())
        self.api_acts_act_ids = self.api.ParseActsActIds(self.acts_df)
        self.db_acts_act_ids = self.db.ParseActsActIds(self.db.GetActsActIds())
        # LOG END

    def GetStreamsFromApi(self):
        pass

    def InsertActivities2Postgres(self):
        if self.CheckApiThreshold(): 
            pass
        else:
            return 'API threshold reached'
        # make sure GetActivities() ran successfully already
        if self.acts_df & self.db_acts_act_ids:
            # LOG START
            self.db.InsertActivities(self.acts_df, self.db_acts_act_ids)
            # LOG END

test = cyclestats()
#test.Connect2Postgres(host="localhost", 
#                      db="CycleStats", 
#                      usr="postgres", 
#                      pwd="soccer18")
