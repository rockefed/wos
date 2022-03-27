## CONFIG
DEBUG = False

## APIs 
# STRAVA ENDPOINTS
ATHLETE_ENDPOINT = ''
ACTIVITY_ENDPOINT = ''
STREAM_ENDPOINT = ''
# MYFITNESSPAL ENDPOINTS


# PARAMS
API_DELAY = 0.01 # delay after each api call, limit is 200/sec this is < 1/2 that
PAGE_SIZE = 1000 # still messing with this
HOURLY_STRAVA_API_LIMIT = 100
DAILY_STRAVA_API_LIMIT = 1000 
INSERT_BATCH_SIZE = 10

## SQL
# LOGGING
LOG_INSERT = 'INSERT INTO logs(who, status, action_type, resource) VALUES(%s,%s,%s,%s);'

# ATHLETES
ATHLETE_INSERT = ''

# ACTIVITIES
ACTIVITIES_INSERT = 'INSERT INTO Activities(achievement_count, athlete, athlete_count, attribute_map, average_speed, average_watts, comment_count, commute, device_watts, discriminator, distance, elapsed_time, elev_high, elev_low, end_latlng, external_id, flagged, gear_id, has_kudoed, id, kilojoules, kudos_count, manual, map, max_speed, max_watts, moving_time, name, photo_count, private, start_date, start_date_local, start_latlng, swagger_types, timezone, total_elevation_gain, total_photo_count, trainer, type, upload_id, weighted_average_watts, workout_type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;;'

# STREAMS
STREAMS_INSERT = 'INSERT INTO Activities_Streams(time, distance, altitude, velocity_smooth, heartrate, cadence, watts, moving, grade_smooth, lat, lng, activity_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning db_id;'
