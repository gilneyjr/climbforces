import os
import json
import requests

def getHandles(handles):

    _handles = ''
    for h in handles[:-1]:
        _handles = _handles + h + ';'
    _handles = _handles + handles[-1]

    URL = 'https://codeforces.com/api/user.info'
    PARAMS = { 'handles' : _handles }

    response = requests.get(url=URL, params=PARAMS)

    data = json.loads(response.text)
    
    if 'result' not in data:
        print('Error: ' + str(data['comment']))

    res = ''
    for user in data['result']:
        #print("handle: " + str(user['handle']))
        country = ''
        try:
            country = user['country']
        except Exception as e:
            country = 'OTHER'
        res = res\
             + str(user['handle']) + ';'\
             + str(country) + ';'\
             + str(user['rating']) + ';'\
             + str(user['maxRating']) + ';'\
             + str(user['registrationTimeSeconds']) + '\n'
    return res

if __name__ == '__main__':
    for root, dirs, files in os.walk('./data/submissions'):
        with open('./data/users.csv', 'w') as f:
            aux = 500
            count = 0

            while count < len(files):
                print('(' + str(count) + '/' + str(min(count+aux, len(files))) + ')')
                handles = [ h[:-4] for h in files[count:count+aux] ]
                res = getHandles(handles)
                f.write(res)
                count = count + aux

            # print('(' + str((len(files)//aux)*aux) + '/' + str(len(files)) + ')')
            # handles = [ h[:-4] for h in files[(len(files)//aux)*aux:] ]
            # res = getHandles(handles)
            # f.write(res)
            




# def getHandle(handle):
#     URL = 'https://codeforces.com/api/user.info'
#     PARAMS = { 'handles' : handle }

#     response = requests.get(url=URL, params=PARAMS)
    

#     data = json.loads(response.text)
    
#     user = data['result'][0]
#     country = ''
#     try:
#         country = user['country']
#     except Exception as e:
#         country = 'OTHER'
#     return str(user['handle']) + ';'\
#          + str(country) + ';'\
#          + str(user['rating']) + ';'\
#          + str(user['maxRating']) + ';'\
#          + str(user['registrationTimeSeconds'])

# if __name__ == '__main__':
#     for root, dirs, files in os.walk('./data/submissions'):
#         with open('./data/users.csv', 'w') as f:
#             count = 1
#             for filename in files:
#                 handle = filename[0:-4]
#                 print(handle + ' (' + str(count) + '/' + str(len(files)) + ')')
#                 f.write(getHandle(handle))
#                 f.write('\n')
#                 count = count + 1