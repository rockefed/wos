from stravaio import strava_oauth2
from stravaio import StravaIO
import pandas as pd
import numpy as np
import psycopg2
import datetime
import random
import time
import os
import config

class api:
    def __init__(self):
        self.api_calls_15min = 0
        self.api_calls_1day = 0
        self.api_call_lim_15min = 100
        self.api_call_lim_1day = 1000
        self.client = None
        self.athlete = None #used for logging

    def Connect2Api(self, token):
        self.client = StravaIO(access_token = token)

    ## ATHLETE
    # get the athlete for logging to the db
    # TODO: this should return a dict
    def GetAthlete(self) -> dict:
        # TODO: check api threshold
        athlete_dict =  self.client.get_logged_in_athlete().to_dict()
        self.athlete = self.ParseAthlete(athlete_dict)
        self.DbLog(self.athlete_name, '200', 'API', 'GET', 'athlete', '', '')
        return athlete_dict

    # store the athlete as a dict of the name & id
    def ParseAthlete(self, athlete_dict):
        dict = {}
        dict['name'] = athlete_dict['firstname'] + ' ' + athlete_dict['lastname']
        dict['id'] = athlete_dict['id']

        return dict

    ## ACTIVITIES
    # Pulls a list of activities for the current athlete from the Strava API
    def GetActivities(self) -> list:
        #self.CheckApiThreshold()
        acts = self.client.get_logged_in_athlete_activities()
        self.DbLog(self.athlete_name, config.SUCCESS, 'API', 'GET', 'activities', '', '')
        return acts
                   
    #Parses the list of activities into a pandas dataframe
    def Activities2DF(self, acts):
        activities = []
        #Parse out each activities and store each record in a list
        for obj in acts:
            record = [obj.achievement_count, obj.athlete, obj.athlete_count, obj.attribute_map, obj.average_speed, obj.average_watts, obj.comment_count, obj.commute, obj.device_watts, obj.discriminator, obj.distance, obj.elapsed_time, obj.elev_high, obj.elev_low, obj.end_latlng, obj.external_id, obj.flagged, obj.gear_id, obj.has_kudoed, obj.id, obj.kilojoules, obj.kudos_count, obj.manual, obj.map, obj.max_speed, obj.max_watts, obj.moving_time, obj.name, obj.photo_count, obj.private, obj.start_date, obj.start_date_local, obj.start_latlng, obj.swagger_types, obj.timezone, obj.total_elevation_gain, obj.total_photo_count, obj.trainer, obj.type, obj.upload_id, obj.weighted_average_watts, obj.workout_type]
 
            activities.append(record)
            
        #Build a dataframe from the activities
        acts_df = pd.DataFrame(self.activities, columns=self.cols_activities)
        return acts_df

    # Make the list of activity id's from acts to compare against to make sure not inserting dups
    def ParseActsActIds(self, acts_df):
        acts_ids = []
        for record in acts_df.itertuples():
            acts_ids.append(record.id)
        return acts_ids

###############################
# TESTING
test = api()
test.Connect2Api('dfd6336fa6376d24d31cd3f99a74888af775e917')
test.GetAthlete()
print(test.athlete)