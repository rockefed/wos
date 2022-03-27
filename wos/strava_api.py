from urllib import response
import requests
import datetime
import config
import pandas as pd
import os

class strava_api:
    def __init__(self):
        self.athletes_df = None
        self.activities_df = None
        self.streams_df = None

        self.headers = {"access_token": ''}

    def RefreshAccessToken(self):
        try:
            client_id = os.getenv('STRAVA_CLIENT_ID')
            client_secret = os.getenv('STRAVA_CLIENT_SECRET')
            refresh_token = os.getenv('STRAVA_REFRESH_TOKEN')
            endpoint = 'https://www.strava.com/oauth/token?client_id={0}&client_secret={1}&refresh_token={2}&grant_type=refresh_token'.format(client_id, client_secret, refresh_token)
            if config.DEBUG: print('RefreshAccessToken endpoint: {0}, headers(excluded): {1}]]'.format(endpoint, self.headers))
            response_refresh_token = requests.post(endpoint)
            self.headers['access_token'] = response_refresh_token.json()['access_token']
        except:
            return 1

    def BuildApiCall(self, resource, endpoint, endpoint_base='https://www.strava.com/api/v3', page_size=config.PAGE_SIZE, page=0, start_date = '', activity_id = ''):
        try:
            if resource == 'athletes':
                return '{0}{1}'.format(endpoint_base, endpoint)
            elif resource == 'activities':
                return '{0}{1}?per_page={2}&before={3}'.format(endpoint_base, endpoint, config.PAGE_SIZE, start_date)
            elif resource == 'streams':
                pass
            else:
                'BuildApiCall failed'
        except:
            return 1

    ## ATHLETES
    def GetAthletes(self):
        try:
            endpoint = self.BuildApiCall('athletes', config.ATHLETE_ENDPOINT)
            if config.DEBUG: print('Athlete endpoint: {0}, headers: {1}]]'.format(endpoint, self.headers))
            response_athlete = requests.get(endpoint, self.headers)
            athletes = response_athlete.json()
            print(athletes)
        except:
            return 1

    ## ACTIVITIES
    def GetActivities(self):
        try:
            endpoint = self.BuildApiCall('activities', config.ACTIVITY_ENDPOINT)
            if config.DEBUG: print('Activities endpoint: {0}, headers: {1}]]'.format(endpoint, self.headers))
            response_activity = requests.get(endpoint, self.headers)
            activities = response_activity.json()
            print(activities)
        except:
            return 1

    ## STREAMS
    def GetStreams(self):
        pass

test = strava_api()
test.RefreshAccessToken()
test.GetAthletes()