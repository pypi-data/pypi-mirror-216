#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from current_all_recording_details import all_recording_details
from Start_SIP_recordings import account_hostname, api_user, apiKey_authenticate, stop_vc_recording, stop_multiple_vc_recordings

token = apiKey_authenticate(api_user)
headers = {'Authorization': token}

## stop multiple recordings
print('Stopping the following recordings:')
print(all_recording_details)
stop_multiple_vc_recordings(all_recording_details)

