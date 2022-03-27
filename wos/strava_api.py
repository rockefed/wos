import requests
import datetime
import config
import pandas as pd

class strava_api:
    def __init__:
        self.athletes_df = None
        self.activities_df = None
        self.streams_df = None

    def BuildApiCall(self, page_size, page, start_date, resource, endpoint, endpoint_base='https://www.strava.com/api/v3', activity_id = ''):
        if resource == 'athletes':
            pass
        elif resource == 'activities':
            pass
        elif resource == 'streams':
            pass
        else:
            return 1

    ## ATHLETES
    def GetAthletes(self):
        pass

    ## ACTIVITIES
    def GetActivities(self):
        pass

    ## STREAMS
    def GetStreams(self):
        pass
