from httpx import head
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import pyscopg2

header = {"access_token" : "47c35ff9c3d1da4b02688d8e30c295672a0bc318"} # manually refresh and update this from the strava client temp
athlete = requests.get("https://www.strava.com/api/v3/athlete", header)
acts = requests.get("https://www.strava.com/api/v3/athlete/activities?per_page=100&before=1648126057.458698", header) # just need to use page_num

#stream = requests.get("https://www.strava.com/api/v3/activities/6587200425/streams?type=time?type=distance?type=latlng?type=altitude?type=velocy_smooth?type=heartrate?type=cadence?type=watts?type=moving?type=grade_smooth", header) # will get 401/404 if the act id isn't found which happens if push up from garmin watch
print(dir(athlete))
print(dir(acts))

acts_df = pd.DataFrame.from_dict(acts.json()) # NEXT: loop over each page appending to this df

# TIMESTAMP FOR FILTERING
ts = datetime.timestamp(datetime.now()) # THE ARG WILL ACTUALLY NEED TO BE THE MAX DATE RETURNED FROM THE DB FOR ACTS/STREAMS

def ConnectToPostgres():
    conn = psycopg2