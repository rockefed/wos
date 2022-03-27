import mongo_db
import pg_db
import myfitnesspal_api
import strava_api
import os

class cyclestats:
    def __init__(self):
        self.mongodb = mongo_db.mongo_db()
        self.pg_db = pg_db.pg_db()
        self.myfitnesspal_api = myfitnespal_api.myfitnesspal_api()
        self.strava_api = strava_api.strava_api()

    def GetAthlete(self):
        pass

    def GetActivities(self):
        pass

    def GetStreams(self):
        pass

    def GetDiary(self):
        pass
