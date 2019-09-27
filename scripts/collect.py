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
        return '"' + str(self.handle) + '","' + str(self.country) + '",' + str(self.rating) + ',' + str(self.maxRating) + ',' + str(self.registrationTimeSeconds)

class Submission:
    def __init__(self, id, creationTimeSeconds, problem_id, verdict):
        self.id = id
        self.creationTimeSeconds = creationTimeSeconds
        self.problem_id = problem_id
        self.verdict = verdict

    def __str__(self):
        return str(self.id) + ',' + str(self.creationTimeSeconds) + ',' + str(self.problem_id) + ',"' + str(self.verdict) + '"'

# perform it, based in average
def getBestHandles(count, start=0):
    return getAllHandles()[start:count]

def getAllHandles():
    URL = "https://codeforces.com/api/user.ratedList"
    users = []
    
    print('Downloading data...')
    response = requests.get(url=URL)
    
    print('Parsing data...')
    data = json.loads(response.text)

    print('Extracting important data...')
    for user in data['result']:
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

def getHandleSubmissions(handle):
    submissions = []

    URL = "https://codeforces.com/api/user.status"
    PARAMS = {'handle' : handle}

    print('Downloading data...')
    response = requests.get(url=URL, params=PARAMS)
    
    print('Parsing data...')
    data = json.loads(response.text)

    print('Extracting important data...')
    for submission in data['result']:

        problem_id = submission['problem']

        submissions.append(
            User(
                int(submission['id']),
                int(submission['creationTimeSeconds']),
                int(problem_id), # ver
                str(submission['verdict'])
            )
        )

def testProblems():
    problems = {}

    URL = "https://codeforces.com/api/problemset.problems"
    
    print('Downloading data...')
    response = requests.get(url=URL)
    
    print('Parsing data...')
    data = json.loads(response.text)

    print('Testing if there is a name equal to another...')
    for problem in data['result']['problems']:
        if not str(problem['name']) in problems:
            problems[str(problem['name'])] = True
        else:
            print("ERRO: PROBLEM '" + str(problem['name']) + "'")

testProblems()

if __name__ == '__umain__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if path[-1] != '/':
            path = path+'/'
    else:
        path = './data/'

    if not os.path.exists(path+'all'):
        os.makedirs(path+'all')

    ratedList = open(path+'all/ratedList.csv', 'w')
    for user in getAllHandles():
        ratedList.write(str(user))
        ratedList.write('\n')
    ratedList.close();

