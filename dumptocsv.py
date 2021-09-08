import json
from pprint import pprint as pp
import gspread
# from authlib.integrations.requests_client import AssertionSession
from datetime import datetime, timedelta, date
import csv
import pendulum
import os
import copy
import codecs
import pandas as pd
import requests
import time



TeamToWorksheet = {
   "Canada":1,
   "UK":2,
   "India":3,
   "France":4,
   "USA":5,
   "SouthKorea":6,
   "Israel":7,
   "Japan":8,
   "Italy":9,
   "USSR":10,
   "Brasil":11,
   "HongKong":12
}

# StravIdtoRowNum = {
#    "70986510":44,
#    "78107660":28
# }
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
   # print(ord('D'))
   if ((ord('D') + dayNumber) > 90):
      secChar = (int(ord('D') + dayNumber - 90))
      # print()
      # colRep = "A" + str(secChar)
      colRep = "%s%s" % ("A", chr(secChar + 65 - 1))
      return colRep
   else:
      colRep = chr(ord('D') + dayNumber)
      return colRep


def get_user_activities_from_strava(start_date_epoch, end_date_epoch, strava_id, strava_tokens):
    # create dictionary of user activities
    master_activities = {}
    activities = {}
   #  f = open('user-data.json')
   #  main_dict = json.load(f)
   #  for teams in main_dict:
    # loop over users
      # user_dict = main_dict[teams]
    activities[strava_id] = {}
   # activities[user]["wsNum"] = TeamToWorksheet[user_dict[user]['team']]
    activities[strava_id]["dist"] = {}
   ## Get the tokens from file to connect to Strava
   ## If access_token has expired then use the refresh_token to get the new access_token
   # print(strava_tokens)
    if strava_tokens['expires_at'] < time.time():
         #Make Strava auth API call with current refresh token
         response = requests.post(
            url = 'https://www.strava.com/oauth/token',
            # ?client_id=62896&client_secret=168e6d7e8e869d6d17abadfc9c3022f1c9bfe3da&refresh_token=38db0f661604e86d486ed93ff7b8279c23e0bd29&grant_type=refresh_token
                           #   url = 'https://www.strava.com/oauth/token',
                           data = {
                                    'client_id': 62896,
                                    'client_secret': '168e6d7e8e869d6d17abadfc9c3022f1c9bfe3da',
                                    'grant_type': 'refresh_token',
                                    'refresh_token': strava_tokens['refresh_token']
                                    }
                        )
         #Save response as json in new variable
         new_strava_tokens = response.json()
         strava_tokens['expires_at'] = new_strava_tokens['expires_at']
         strava_tokens['access_token'] = new_strava_tokens['access_token']
         strava_tokens['refresh_token'] = new_strava_tokens['refresh_token']

   #Loop through all activities
    retry = 0
    while retry < 3:
       url = "https://www.strava.com/api/v3/athlete/activities"
       r = requests.get(url + '?after=' + str(start_date_epoch) + '&before=' + str(end_date_epoch) + "&per_page=200", headers={"Authorization":"Bearer "+str(strava_tokens['access_token'])})
       if r.status_code > 300:
         #  Retry upto 3 times?
          time.sleep(100)
          retry += 1
       elif r.status_code == 200:
          break

    r = r.json()
    if not r:
       return activities
   #  print(r)
    for entry in r:
      try:
       if entry['distance'] >= 19999 and ((entry['type'] == "Ride" or entry['type'] == "VirtualRide") or entry['workout_type'] in [10,12]):
         colnum = find_col_number(entry['start_date_local'])
         print(colnum)
         start_time = entry['start_date']
         utc_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S%fZ")
         epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds()
         end_time = epoch_time + entry['elapsed_time']
         if colnum not in activities[strava_id]['dist']:
            activities[strava_id]['dist'][colnum] = {}
         if entry['manual']:
            with open('manual.csv', 'a') as ff:
               ff.write("{},{},{},{},{}\n".format(strava_id, strava_tokens['name'][0], entry['name'], entry['distance']/1000, entry['id']))
            continue
         if entry['from_accepted_tag']:
            with open('tagged.csv', 'a') as ff:
               ff.write("{},{},{},{},{}\n".format(strava_id, strava_tokens['name'][0], entry['name'], entry['distance']/1000, entry['id']))
            continue
         activities[strava_id]['dist'][colnum][entry['id']] =  {
            'dist':entry['distance']/1000,
            'start':epoch_time,
            'end':end_time,
            'tagged':entry['from_accepted_tag']
         }
         if entry['max_speed']*3.6 > 60:
            with open('fishy.csv', 'a') as ff:
               ff.write("{},{},{},{},{},{},{}\n".format(strava_id, strava_tokens['name'][0], entry['name'], entry['distance']/1000, entry['max_speed']*3.6, entry['average_speed']*3.6, entry['id']))
      except Exception as e:
         # print(e)
         with open('error.json', 'a') as ff:
               ff.write(json.dumps(entry))
   #  master_activities[teams] = activities
    for day in activities[strava_id]['dist']:
       allrides = activities[strava_id]['dist'][day]
      #  if len(allrides) == 1:
      #     return activities
       totalDist = 0
       # Find out if there are duplicate entries
       intervals = []
       remove_ids = []
       for ride in allrides:
          intervals.append((allrides[ride]['start'], allrides[ride]['end'], ride))
       intervals = sorted(intervals, key=lambda i: (i[0], i[1]))
       print(intervals)
       for i in range(1,len(intervals)):
          if(intervals[i][0] < intervals[i-1][1]):
            #  Find greater distance
             if allrides[intervals[i][2]]['dist'] >= allrides[intervals[i-1][2]]['dist']:
                remove_ids.append(intervals[i-1][2])
             else:
                remove_ids.append(intervals[i][2])
       for ride_id in remove_ids:
          del allrides[ride_id]
       for ride in allrides:
         totalDist += allrides[ride]['dist']
       activities[strava_id]['dist'][day]['total'] = totalDist
       print(remove_ids)
    return activities




def main():
    # INPUT
    google_sheet_key = '1ex1PlvFHkxO6pwGPIqbD6Z9I0WzZx23PCF7c2Dk81d0'

   #  # connect to google sheet
    sht = connect_to_spreadsheet(google_sheet_key)

   # Enter Correct Strava Ids.
    filelist = ['USA.json', 'Canada.json','SouthKorea.json', 'Japan.json', 'USSR.json', 'Italy.json', 'India.json', 'HongKong.json', 'UK.json', 'Brasil.json', 'France.json',  'Israel.json']
    for filename in filelist[4:]:
       filename = "SouthKorea.json"
       with open(os.path.join('./AuthData/', filename), 'r') as f: # open in readonly mode
         print(filename)
         wsNum = TeamToWorksheet[filename.split(".")[0]]
         ws = sht.get_worksheet(wsNum)
         curr_team = (json.load(f))
         for strava_id in curr_team:
            strava_id = '29280769'
            print(curr_team[strava_id]['name'])
            if 'row' in curr_team[strava_id]:
               rownum = curr_team[strava_id]['row']
               # address = ("C"+str(rownum))
               # ws.update(address, strava_id)
      # do your stuff
               CHALLENGE_START = 1615401000
               SINCE_TMINUS3 = 1618857000
               BEFORE_T = 1619289000
               # PREVIOUS_DAY_START = int((datetime.combine(date.today(), datetime.min.time())-datetime(1970,1,1)).total_seconds())
               activities = get_user_activities_from_strava(SINCE_TMINUS3, BEFORE_T, strava_id, curr_team[strava_id])
               print(activities)
               for activity in activities[strava_id]['dist']:
                  address = activity + str(rownum)
                  if 'total' in activities[strava_id]['dist'][activity]:
                     ws.update(address, activities[strava_id]['dist'][activity]['total'])
            exit()
         # Update master last edit board
         address = 'Y2'
         ws.update(address, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time()))))
         # exit()
         time.sleep(60)
         # exit()
   #  with open('user-activity-data.json', 'w') as f:
   #    json.dump(activities, f)
   # To Update Sheet with activty
   #  for id in activities:
   #    ws = sht.get_worksheet(activities[id]['wsNum'])
   #    rowNum = StravIdtoRowNum[id]
   #    for dist in activities[id]['dist']:
   #       ws.update(dist+str(rowNum) , activities[id]['dist'][dist])


if __name__ == "__main__":
    main()