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


def revoke_access(strava_id, strava_tokens):
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
            print(response.status_code )
            if response.status_code == 200:
               strava_tokens['expires_at'] = new_strava_tokens['expires_at']
               strava_tokens['access_token'] = new_strava_tokens['access_token']
               strava_tokens['refresh_token'] = new_strava_tokens['refresh_token']
               url = "https://www.strava.com/oauth/deauthorize"
               r = requests.post(url + '?access_token=' + str(strava_tokens['access_token']))
               print(url + '?access_token=' + str(strava_tokens['access_token']))
               print(r.status_code)
            else:
               return

def main():
   filelist = ['USA.json', 'Canada.json','SouthKorea.json', 'Japan.json', 'USSR.json', 'Italy.json', 'India.json', 'HongKong.json', 'UK.json', 'Brasil.json', 'France.json',  'Israel.json']
   for filename in filelist[4:]:
      with open(os.path.join('./AuthData/', filename), 'r') as f: # open in readonly mode
         print(filename)
         curr_team = (json.load(f))
         for strava_id in curr_team:
            print(curr_team[strava_id]['name'])
            revoke_access(strava_id, curr_team[strava_id])


if __name__ == "__main__":
    main()