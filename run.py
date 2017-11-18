import json
import requests
import time


def is_json(myjson):
	try:
		json.dumps(myjson)
		return True
	except:
		return False

num_pages = 0

# World Bank public API for documents is on: http://search.worldbank.org/api/v2/wds
# Use filters in the GUI to generate the URL
# Do a first request to the API to discover the total number of pages
# Loop in the different pages, and get the txturl field of each document
# Save the files locally using a streaming and keep a log of the last downloaded file and page number
document_type = "Working+Paper"
start_date = "2014-01-01"
end_date = "2015-01-01"

url = "http://search.worldbank.org/api/v2/wds?format=json&docty_exact=" + document_type  +"&str_docdt=" + start_date + "&end_docdt=" + end_date + "&srt=docdt&order=desc"
response = requests.get(url).json()
num_pages = response['total']

# Loop in the pages
for page in range(1863, int(num_pages) + 1):
	print (str(page) + " of " + str(num_pages))
	req = "http://search.worldbank.org/api/v2/wds?format=json&os=" + str(page) + "&docty_exact=" + document_type  +"&str_docdt=" + start_date + "&end_docdt=" + end_date + "&srt=docdt&order=desc"
	# print(json.dumps(response, indent=4, sort_keys=True))
	time.sleep(0.01)

	response = requests.get(req).json()

	# test if the response is a json, sometimes the json returned by API are not valid
	if is_json(response):
		# For every item in the page, get the txturl field
		for item in response['documents']:
			# Test if a txturl field exists for this specific item
			if "txturl" in response["documents"][item]:
				# Get the url of the file to download
				txturl = (response["documents"][item]["txturl"])
				# Get the name of the file
				file_name = "txt/" + txturl.split('/')[-1]
				# Notify the user of the download progress
				print ("Downloading " + txturl + "\n \n")
				# Trigger the download as a stream (stream is good to use in case file is too big)
				download = requests.get(txturl, stream=True)
				# A workaround to ensure there is no connection reset by peer error
				time.sleep(0.01)
				# Save the file in chunks of 500000 byles (~0.5 MB)

				with open(file_name, 'wb') as fd:
					for chunk in download.iter_content(500000):
						fd.write(chunk)

				with open('log.txt', 'w') as log_file:
					log_file.write("page: " + str(page) + ', guid: ' + response["documents"][item]["guid"])
