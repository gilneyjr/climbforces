#!/usr/bin/python3

import sys
import os
import requests
import json

def saveSubmissions(handle, path):
    URL = "https://codeforces.com/api/user.status"
    PARAMS = {'handle' : handle}
    
    # Getting submissions
    response = requests.get(url=URL, params=PARAMS)

    # Parsing JSON
    data = json.loads(response.text)

    # Saving in file
    with open(path, 'w') as f:
        for submission in data['result']:
            try:
                f.write('{},{},{},{}\n'.format(\
                    int(submission['id']),\
                    int(submission['creationTimeSeconds']),\
                    str(submission['problem']['contestId']) + str(submission['problem']['index']),\
                    str(submission['verdict'])\
                ))
            except Exception as e:
                # Ignore submissions not related to contest problems
                pass

def getHandles(path):
    users = []

    with open(path, 'r') as f:
        line = f.readline()
        while line:
            users.append(line.split(',')[0])
            line = f.readline()
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

    if not os.path.exists(path+'submissions/'):
        os.makedirs(path+'submissions/')
    
    count = 1
    handles = getHandles(path+'users.csv')
    for handle in handles:
        print('Collecting ' + handle + '\'s submissions (' + str(count) + '/' + str(len(handles)) + ')')
        if not os.path.exists(path+'submissions/'+handle+'.csv'):
            saveSubmissions(handle, path+'submissions/'+handle+'.csv')
        count = count+1