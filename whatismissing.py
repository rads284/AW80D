import json

f = open('user-data-4.json',)
data = json.load(f)
missing = {}
for team in data:
   print(team+"\n")
   missing[team] = {}
   currentData = json.load(open('./AuthData/' + team + ".json"))
   for member in data[team]:
      if member not in currentData:
         missing[team][member] = data[team][member]

with open('user-diff-data-4.json', 'w') as f:
   json.dump(missing, f)
   print(data[team][member]['name'][0])


# import os

# filelist = ['SouthKorea.json', 'Japan.json', 'USSR.json', 'Italy.json', 'India.json', 'HongKong.json', 'UK.json', 'Canada.json', 'Brasil.json', 'France.json', 'USA.json', 'Israel.json']
# for filename in filelist:
#    with open(os.path.join('./AuthData/', filename), 'r') as f: # open in readonly mode
#       data = json.load(f)
#       for member in data:
#          if 'row' not in data[member]:
#             print(filename, member, data[member])
