# Start and Stop multiple SIP Recordings with Rev

Configuration:
	account_hostname - your Rev tenant hostname
	api_user - your user's API key and secret key (user must have appropriate permissions in Rev)
	
	sip_address - your SIP address
	
	recording_title - recordings will start with this with the recording_counter value appended to the end
	recording_counter - appended to the end of recording_title and incremented by 1 after each SIP call is started
	iterations - number of recordings to start in this run

	Example:
		recording_title = 'Recording '
		recording_counter = 1
		iterations = 10
		
		This will start 10 recordings, titled "Recording 1", "Recording 2" ... "Recording 10"
		
		
After starting each recording, the video titles and videoIds will be output to a file called "current_all_recording_details.py" which will contain the details, like this:
	
	all_recording_details = [{'title': 'Recording 1', 'videoId': 'f57fe5eb-9d84-4fc4-8f7f-623b0101ede6'}, {'title': 'Recording 2', 'videoId': 'da9e8079-1478-419d-b252-cf5c569528d3'}, {'title': 'Recording 3', 'videoId': 'a6eb020d-8323-42d6-ae98-378e4e6d7fd0'}, {'title': 'Recording 4', 'videoId': '0c1c0721-05df-4170-929f-695ce107ed2b'}]

These details are needed by "Stop_SIP_recordings.py" to call the Stop VC Recording API. 