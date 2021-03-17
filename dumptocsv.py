import json
from pprint import pprint as pp
import gspread
from datetime import datetime, timedelta
import csv
import pendulum
import os
import copy
import codecs
import pandas as pd
import requests
import time



TeamToWorksheet = {
   "Canada":2,
   "UK":3,
   "India":4,
   "France":5,
   "USA":6,
   "SouthKorea":7,
   "Israel":8,
   "Japan":9,
   "Italy":10,
   "USSR":11
}

StravIdtoRowNum = {
   "70986510":44
}
def connect_to_spreadsheet(key):
    # connect to google sheet
    gc = gspread.oauth()
    # open spreadsheet
    sht1 = gc.open_by_key(key)
    return sht1

def find_col_number(localDate):
   startDate = "2021-03-11T00:00:00Z"
   d1 = datetime.strptime(startDate.split('T')[0], "%Y-%m-%d")
   d2 = datetime.strptime(localDate.split('T')[0], "%Y-%m-%d")
   dayNumber = (abs(d2 - d1).days)
   # Day 1 is Column D
   colRep = chr(ord('D') + dayNumber)
   return colRep


def get_user_activities_from_strava(start_date_epoch, end_date_epoch):
    # create dictionary of user activities
    activities = {}
    f = open('user-data.json')
    user_dict = json.load(f)
    # loop over users
    for user in user_dict:
        activities[user] = {}
        ## Get the tokens from file to connect to Strava
        ## If access_token has expired then use the refresh_token to get the new access_token
        strava_tokens = user_dict[user]
        if user_dict[user]['expires_at'] < time.time():
            #Make Strava auth API call with current refresh token
            response = requests.post(
                                url = 'https://www.strava.com/oauth/token',
                                data = {
                                        'client_id': 62869,
                                        'client_secret': '168e6d7e8e869d6d17abadfc9c3022f1c9bfe3da',
                                        'grant_type': 'refresh_token',
                                        'refresh_token': user_dict[user]['refresh_token']
                                        }
                            )
            #Save response as json in new variable
            strava_tokens = response.json()
            user_dict[user]['expires_at'] = strava_tokens['expires_at']
            user_dict[user]['access_token'] = strava_tokens['access_token']

        #Loop through all activities
        url = "https://www.strava.com/api/v3/athlete/activities"
        r = requests.get(url + '?after=' + str(start_date_epoch) + '&before=' + str(end_date_epoch), headers={"Authorization":"Bearer "+str(strava_tokens['access_token'])})
        r = r.json()
        if not r:
          break
        for entry in r:
          if entry['distance'] > 20000:
             colnum = find_col_number(entry['start_date_local'])
             if colnum in activities[user]:
                activities[user][colnum] += entry['distance']/1000
             else:
                activities[user][colnum] = entry['distance']/1000
    print(activities)




def main():
    # INPUT
    google_sheet_key = '1ex1PlvFHkxO6pwGPIqbD6Z9I0WzZx23PCF7c2Dk81d0'
   #  nbr_of_weeks = 13
   #  client_id = [CLIENT_ID]
   #  client_secret = '[CLIENT_SECRET]'

   #  # connect to google sheet
   #  sht = connect_to_spreadsheet(google_sheet_key)
   #  ws3 = sht.get_worksheet(3)
    get_user_activities_from_strava(1615401000, 1615900735)

   #  # create data structures to store user/activity data
   #  weekly_dict = create_weekly_dictionary(start_date, nbr_of_weeks)
   #  user_dict = get_user_info(sht)
   #  weekly_user_dict = create_weekly_user_dict(weekly_dict, user_dict)

   #  # get user activity from strava
   #  activities = get_user_activities_from_strava(user_dict, start_date_epoch, end_date_epoch, client_id, client_secret)

   #  # add weekly values to weekly/user data structure
   #  parse_activity_data(weekly_user_dict, user_dict, activities)

   #  # update google sheet with challenge values
   #  write_to_sheet(sht, weekly_user_dict, len(user_dict))


if __name__ == "__main__":
    main()