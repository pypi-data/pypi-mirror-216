#!/usr/bin/env python
# coding: utf-8

# In[9]:


import requests
import json
import time

### START CONFIGURATION ###
account_hostname = 'https://alextest.rev-qa.vbrick.com'
api_user = {
    'ApiKey': 'PeonATawHHW8Vw7pvKIK6PwpGA2k0JXzTm6QMQSJcfk_',
    'Secret': 'yG0mESo_nu6c0kPkWB_vWMaf4OlGqzxmmMpxwtWCOJBZUyjcOP6_UmVDAf7yzNgkEJEKXsN9K7Ihw_ej0D4QbTVFuARoRkOH87kMyty261xAuzQ5F_e8tcp14YB9AwyhIDExpTBERj1VpkGgll4FIWIoYdGVDaF6kkvLu_i8p1c_'
}

recording_title = 'Recording '   #'recording_counter' will be appended to the video title
recording_counter = 1    # number to start with
sip_address = 'alex.mcintosh@vb.webex.com'
iterations = 1   #number of SIP recordings to start

### END CONFIGURATION ###

all_recording_details = []

# POST /api/v2/authenticate. Returns formatted Vbrick access token
# user_keys should be a dictionary with keys 'ApiKey' and 'Secret'
def apiKey_authenticate(user_keys, hostname=account_hostname):
    url = hostname + '/api/v2/authenticate'
    authenticate_response = requests.post(url, data=user_keys) #post to /authenticate API
    if authenticate_response.status_code == 200:
        auth_token = json.loads(authenticate_response.text).get('token') #converts the json response body to a dictionary and gets the token value
        return 'VBrick ' + auth_token
    else:
        print('/authenticate API request failed with status code', authenticate_response.status_code)
        print(authenticate_response.text)

token = apiKey_authenticate(api_user)
headers = {'Authorization': token}

# start a VC recording with SIP address. Returns the videoId of the recording.
def start_vc_recording(video_title, sipAddress, headers=headers, hostname=account_hostname):
    video_id = ''
    url = hostname + '/api/v2/vc/start-recording'
    payload = {'title': video_title, 'sipAddress': sipAddress}
    start_recording_response = requests.post(url, data=payload, headers=headers)
    if start_recording_response.status_code == 200:
        video_id = json.loads(start_recording_response.text).get('videoId')
        print(f'Call placed to {sipAddress}. Title: {video_title};   Id: {video_id}')
        return video_id
    else:
        print('Start recording failed with status code: ' + start_recording_response.status_code)
        print(start_recording_response.text)

def stop_vc_recording(video_id, headers=headers, hostname=account_hostname):
    url = hostname + '/api/v2/vc/stop-recording'
    payload = {'videoId': video_id}
    stop_recording_response = requests.post(url, data=payload, headers=headers)
    if stop_recording_response.status_code == 200:
        print(f'Recording {video_id} stopped.')
    else:
        print('Stop recording failed with status code: ' + stop_recording_response.status_code)
        print(stop_recording_response.text)

def get_vc_recording_status(video_id, headers=headers, hostname=account_hostname):
    url = hostname + '/api/v2/vc/recording-status/' + video_id
    recording_status_response = requests.get(url, headers=headers)
    if recording_status_response.status_code == 200:
        print(f'Recording {video_id} status: {recording_status_response.text}')
    else:
        print('Failed to get recording status: ' + stop_recording_response.status_code + '  ' + stop_recording_response.text)
        
def start_multiple_vc_recordings(video_title=recording_title, recording_counter=recording_counter, sipAddress=sip_address, iterations=iterations, headers=headers, hostname=account_hostname):
    multiple_recording_details = []
    for x in range(0, iterations):
        current_recording_title = recording_title
        current_recording_title += str(recording_counter)
        current_recording_id = start_vc_recording(current_recording_title, sip_address)
        multiple_recording_details.append({'title': current_recording_title, 'videoId': current_recording_id})
        recording_counter += 1
        time.sleep(5)
    return multiple_recording_details

def stop_multiple_vc_recordings(recording_details=all_recording_details, headers=headers, hostname=account_hostname):
    for recording in recording_details:
        stop_vc_recording(recording.get('videoId'))
        

## start multiple recordings
if __name__ == '__main__':
    print(f'Starting {iterations} calls. Please answer the calls at the VC endpoint.')
    all_recording_details = start_multiple_vc_recordings()
        
    with open('current_all_recording_details.py', 'w') as file:
        file.write(f'all_recording_details = {all_recording_details}\n')
        
    print('Recording details exported to "current_all_recording_details.py" and printed below:')
    print()
    print(all_recording_details)

