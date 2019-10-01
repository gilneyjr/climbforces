#!/usr/bin/python3

import sys
import os
import requests
import json

class User:
    def __init__(self, handle, country, rating, maxRating, registrationTimeSeconds):
        self.handle = handle
        self.country = country # can be absent
        self.rating = rating
        self.maxRating = maxRating
        self.registrationTimeSeconds = registrationTimeSeconds

    def __str__(self):
        return  str(self.handle) + ',' + str(self.country) + ',' + str(self.rating) + ',' + str(self.maxRating) + ',' + str(self.registrationTimeSeconds)

def getBestHandles(count, start=0):
    return getAllHandles()[start:count]

def getHandles(count=-1,start=0):
    URL = "https://codeforces.com/api/user.ratedList"
    users = []
    
    print('Downloading data...')
    response = requests.get(url=URL)
    
    print('Parsing data...')
    data = json.loads(response.text)

    if count < 0:
        count = len(data['result'])

    print('Extracting important data...')
    for user in data['result'][start:count]:
        if int(user['rating']) > 1500:
            country = ''
            try:
                country = user['country']
            except Exception as e:
                country = 'OTHER'

            users.append(
                User(
                    str(user['handle']),
                    str(country),
                    int(user['rating']),
                    int(user['maxRating']),
                    int(user['registrationTimeSeconds'])
                )
            )

    print('Done!')
    return users

if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if path[-1] != '/':
            path = path+'/'
    else:
        path = './data/all/'

    if not os.path.exists(path):
        os.makedirs(path)

    ratedList = open(path+'users.csv', 'w')
    for user in getHandles():
        ratedList.write(str(user))
        ratedList.write('\n')
    ratedList.close()