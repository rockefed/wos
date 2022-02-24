# All the SQL statements should be stored here

# API
SELECT_API_HITS_15M = "select CalculateApiHits15mins();"
SELECT_API_HITS_1D = "select CalculateApiHits1day();"

## LOGGING
INSERT_LOG_SQL = 'INSERT INTO logs(who, status, source, action_type, db_table, db_column, db_value) VALUES(%s,%s,%s,%s,%s,%s,%s);'
INSERT_LOG_PARAMS = (None, None, None, None, None, None, None) # LEGACY CODE
SELECT_LOGS_BYDATE = "select * from GetLogs('{0}', '{1}')" # for exporting

## ACTIVITIES
INSERT_ACTS_SQL = 'INSERT INTO Activities(achievement_count, athlete, athlete_count, attribute_map, average_speed, average_watts, comment_count, commute, device_watts, discriminator, distance, elapsed_time, elev_high, elev_low, end_latlng, external_id, flagged, gear_id, has_kudoed, id, kilojoules, kudos_count, manual, map, max_speed, max_watts, moving_time, name, photo_count, private, start_date, start_date_local, start_latlng, swagger_types, timezone, total_elevation_gain, total_photo_count, trainer, type, upload_id, weighted_average_watts, workout_type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;;'
INSERT_ACTS_PARAMS = (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None) # LEGACY CODE
SELECT_ACTS_ACT_IDS = 'SELECT id from activities;' # to only GET acts after the last one in the db
SELECT_ACTS_BYDATE = "select * from GetActivities('{0}', '{1}')" # for exporting

## ATHLETE


## STREAMS
INSERT_STREAMS_SQL = 'INSERT INTO Activities_Streams(time, distance, altitude, velocity_smooth, heartrate, cadence, watts, moving, grade_smooth, lat, lng, activity_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning db_id;'
INSERT_STREAMS_PARAMS = (None, None, None, None, None, None, None, None, None, None, None, None) # LEGACY CODE
SELECT_STREAMS_ACT_IDS = 'select distinct cast(activity_id as bigint) from activities_streams;' # to only GET streams after the last one in the db
SELECT_STREAMS_BYDATE = "select * from GetStreams('{0}', '{1}')" # for exporting

## PROCESSED ACTIVITIES
SELECT_PROC_ACTS_BYDATE = "select * from GetProcessedActivities('{0}', '{1}')" # for exporting