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

# Opening JSON file
f = open('./aw80d-79986-default-rtdb-export.json',)
data = json.load(f)
athlete_token_dict = {}
for entry in data['auth-tokens-activity']:
   val = data['auth-tokens-activity'][entry]
   strava_id = val['athlete']['id']
   team = val['teamName']
   access_token = val['access_token']
   refresh_token = val['refresh_token']
   athlete_token_dict[strava_id] = {
      "team":team,
      "access_token":access_token,
      "refresh_token":refresh_token,
      "expires_at":val['expires_at']
   }
f.close()

# print(athlete_token_dict)

with open('user-data.json', 'w') as f:
   json.dump(athlete_token_dict, f)

# One Time
# Fetch riders data since 11th March

