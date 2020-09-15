import pandas as pd
import psycopg2
import json
with open('project/credentials/db_credentials.json') as db_file:
    data_base = json.load(db_file)
DB_HOST = data_base['DB_HOST']
DB_USER = data_base['DB_USER']
DB_PASS = data_base['DB_PASS']
DB_PORT = data_base['DB_PORT']
DB_NAME = data_base['DB_NAME']
sleep_i = """ INSERT INTO oura_sleep (awake, bedtime_end, bedtime_end_delta, bedtime_start, bedtime_start_delta, breath_average, deep, duration, efficiency, hr_5min, hr_average, hr_lowest, hypnogram_5min, is_longest, light, midpoint_at_delta, midpoint_time, onset_latency, period_id, rem, restless, rmssd, rmssd_5min, score, score_alignment, score_deep, score_disturbances, score_efficiency, score_latency, score_rem, score_total, summary_date, temperature_delta, temperature_deviation, temperature_trend_deviation, timezone, total, user_id)
VALUES (%(awake)s, %(bedtime_end)s, %(bedtime_end_delta)s, %(bedtime_start)s, %(bedtime_start_delta)s, %(breath_average)s, %(deep)s, %(duration)s, %(efficiency)s, %(hr_5min)s, %(hr_average)s, %(hr_lowest)s, %(hypnogram_5min)s, %(is_longest)s,%(light)s, %(midpoint_at_delta)s, %(midpoint_time)s, %(onset_latency)s, %(period_id)s, %(rem)s, %(restless)s, %(rmssd)s, %(rmssd_5min)s, %(score)s, %(score_alignment)s, %(score_deep)s, %(score_disturbances)s, %(score_efficiency)s, %(score_latency)s, %(score_rem)s, %(score_total)s, %(summary_date)s, %(temperature_delta)s, %(temperature_deviation)s, %(temperature_trend_deviation)s, %(timezone)s, %(total)s, %(user_id)s );"""
sleep_u = """ UPDATE oura_sleep 
SET awake = %(awake)s, bedtime_end = %(bedtime_end)s, bedtime_end_delta = %(bedtime_end_delta)s, bedtime_start = %(bedtime_start)s, bedtime_start_delta = %(bedtime_start_delta)s, breath_average = %(breath_average)s, deep = %(deep)s, duration = %(duration)s, efficiency = %(efficiency)s, hr_5min = %(hr_5min)s, hr_average = %(hr_average)s, hr_lowest = %(hr_lowest)s, hypnogram_5min = %(hypnogram_5min)s, is_longest = %(is_longest)s, light = %(light)s, midpoint_at_delta = %(midpoint_at_delta)s, midpoint_time = %(midpoint_time)s, onset_latency = %(onset_latency)s, period_id = %(period_id)s, rem = %(rem)s, restless = %(restless)s, rmssd = %(rmssd)s, rmssd_5min = %(rmssd_5min)s, score = %(score)s, score_alignment = %(score_alignment)s, score_deep = %(score_deep)s, score_disturbances = %(score_disturbances)s, score_efficiency = %(score_efficiency)s, score_latency = %(score_latency)s, score_rem = %(score_rem)s, score_total = %(score_total)s, temperature_delta = %(temperature_delta)s, temperature_deviation = %(temperature_deviation)s, temperature_trend_deviation = %(temperature_trend_deviation)s, timezone = %(timezone)s, total = %(total)s
WHERE user_id = %(user_id)s AND summary_date = %(summary_date)s"""
reainess_i = """ INSERT INTO oura_readiness (period_id, score, score_activity_balance, score_hrv_balance, score_previous_day, score_previous_night, score_recovery_index, score_resting_hr, score_sleep_balance, score_temperature, summary_date, user_id)
VALUES (%(period_id)s, %(score)s, %(score_activity_balance)s, %(score_hrv_balance)s, %(score_previous_day)s, %(score_previous_night)s, %(score_recovery_index)s, %(score_resting_hr)s, %(score_sleep_balance)s, %(score_temperature)s, %(summary_date)s, %(user_id)s);"""
readiness_u = """UPDATE oura_readiness
SET period_id = %(period_id)s, score = %(score)s, score_activity_balance = %(score_activity_balance)s, score_hrv_balance = %(score_hrv_balance)s, score_previous_day = %(score_previous_day)s, score_previous_night = %(score_previous_night)s, score_recovery_index = %(score_recovery_index)s, score_resting_hr = %(score_resting_hr)s, score_sleep_balance = %(score_sleep_balance)s, score_temperature = %(score_temperature)s
WHERE user_id =%(user_id)s AND summary_date = %(summary_date)s"""
activity_i = """ INSERT INTO oura_activity (average_met, cal_active, cal_total, class_5min, daily_movement, day_end, day_start, high, inactive, inactivity_alerts, low, medium, met_1min, met_min_high, met_min_inactive, met_min_low, met_min_medium, non_wear, rest, score, score_meet_daily_targets, score_move_every_hour, score_recovery_time, score_stay_active, score_training_frequency, score_training_volume, steps, summary_date, target_calories, target_km, target_miles, timezone, to_target_km, to_target_miles, total, user_id)
VALUES (%(average_met)s, %(cal_active)s, %(cal_total)s, %(class_5min)s, %(daily_movement)s, %(day_end)s, %(day_start)s, %(high)s, %(inactive)s, %(inactivity_alerts)s, %(low)s, %(medium)s, %(met_1min)s, %(met_min_high)s, %(met_min_inactive)s, %(met_min_low)s, %(met_min_medium)s, %(non_wear)s, %(rest)s, %(score)s, %(score_meet_daily_targets)s, %(score_move_every_hour)s, %(score_recovery_time)s, %(score_stay_active)s, %(score_training_frequency)s, %(score_training_volume)s, %(steps)s, %(summary_date)s, %(target_calories)s, %(target_km)s, %(target_miles)s, %(timezone)s, %(to_target_km)s, %(to_target_miles)s, %(total)s, %(user_id)s);"""
activity_u = """ UPDATE oura_activity
SET average_met = %(average_met)s, cal_active = %(cal_active)s, cal_total = %(cal_total)s, class_5min = %(class_5min)s, daily_movement = %(daily_movement)s, day_end = %(day_end)s, day_start = %(day_start)s, high = %(high)s, inactive = %(inactive)s, inactivity_alerts = %(inactivity_alerts)s, low = %(low)s, medium = %(medium)s, met_1min = %(met_1min)s, met_min_high = %(met_min_high)s, met_min_inactive = %(met_min_inactive)s, met_min_low = %(met_min_low)s, met_min_medium =%(met_min_medium)s, non_wear = %(non_wear)s, rest = %(rest)s, score = %(score)s, score_meet_daily_targets = %(score_meet_daily_targets)s, score_move_every_hour = %(score_move_every_hour)s, score_recovery_time = %(score_recovery_time)s, score_stay_active = %(score_stay_active)s, score_training_frequency = %(score_training_frequency)s, score_training_volume = %(score_training_volume)s, steps = %(steps)s, target_calories = %(target_calories)s, target_km = %(target_km)s, target_miles = %(target_miles)s, timezone = %(timezone)s, to_target_km = %(to_target_km)s, to_target_miles = %(to_target_miles)s, total = %(total)s
WHERE user_id = %(user_id)s AND summary_date = %(summary_date)s"""
insert_dict = {
    'sleep':sleep_i,
    'activity':activity_i,
    'readiness':reainess_i
}
update_dict = {
    'sleep':sleep_u,
    'activity':activity_u,
    'readiness':readiness_u
}
def to_db(summary,test,user_id):
    con = psycopg2.connect(database=DB_NAME,user=DB_USER,host=DB_HOST,password=DB_PASS,port=DB_PORT)
    cur = con.cursor()
    print("length of test :",len(test))
    for row in test:
        row['user_id'] = user_id
        cur.execute("""SELECT summary_date FROM oura_""" + summary + """ WHERE user_id = %s AND summary_date = %s""",(row['user_id'],row['summary_date']))
        x = cur.fetchall()
        if x:
            cur.execute(update_dict[summary],row)
            print("update:",row['summary_date'])
        else:
            cur.execute(insert_dict[summary],row)
            print('insert:',row['summary_date'])
    con.commit()
    cur.close()
    con.close()
    return True
