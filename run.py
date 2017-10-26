import json
import requests
import time

num_pages = 0

# World Bank public API for documents is on: http://search.worldbank.org/api/v2/wds
# Use filters in the GUI to generate the URL
# Do a first request to the API to discover the total number of pages
url = "http://search.worldbank.org/api/v2/wds?format=json&fl=abstracts,admreg,alt_title,authr,available_in,bdmdt,chronical_docm_id,closedt,colti,count,credit_no,disclosure_date,disclosure_type,disclosure_type_date,disclstat,display_title,docdt,docm_id,docna,docty,dois,entityid,envcat,geo_reg,geo_reg,geo_reg_and_mdk,guid,historic_topic,id,isbn,issn,keywd,lang,listing_relative_url,lndinstr,loan_no,majdocty,majtheme,ml_abstract,ml_display_title,new_url,owner,pdfurl,prdln,projectid,projn,publishtoextweb_dt,repnb,repnme,seccl,sectr,src_cit,subsc,subtopic,teratopic,theme,topic,topicv3,totvolnb,trustfund,txturl,unregnbr,url_friendly_title,versiontyp,versiontyp_key,virt_coll,vol_title,volnb&docty_exact=Policy+Note%5EPolicy+Research+Working+Paper%5EStaff+Working+Paper%5EWBI+Working+Paper%5EWorking+Paper%5EWorking+Paper+%28Numbered+Series%29&srt=docdt&order=desc"
response = requests.get(url).json()
num_pages = response['total']


# Loop in the pages
for page in range(1, int(num_pages)):
	req = "http://search.worldbank.org/api/v2/wds?format=json&os=" + str(page) + "&fl=abstracts,admreg,alt_title,authr,available_in,bdmdt,chronical_docm_id,closedt,colti,count,credit_no,disclosure_date,disclosure_type,disclosure_type_date,disclstat,display_title,docdt,docm_id,docna,docty,dois,entityid,envcat,geo_reg,geo_reg,geo_reg_and_mdk,guid,historic_topic,id,isbn,issn,keywd,lang,listing_relative_url,lndinstr,loan_no,majdocty,majtheme,ml_abstract,ml_display_title,new_url,owner,pdfurl,prdln,projectid,projn,publishtoextweb_dt,repnb,repnme,seccl,sectr,src_cit,subsc,subtopic,teratopic,theme,topic,topicv3,totvolnb,trustfund,txturl,unregnbr,url_friendly_title,versiontyp,versiontyp_key,virt_coll,vol_title,volnb&docty_exact=Policy+Note%5EPolicy+Research+Working+Paper%5EStaff+Working+Paper%5EWBI+Working+Paper%5EWorking+Paper%5EWorking+Paper+%28Numbered+Series%29&srt=docdt&order=desc"
	response = requests.get(req).json()
	# For every item in the page, get the txturl field 
	for item in response['documents']:
		# Test if a txturl field exists for this specific item (otherwise might throw an error)
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
			time.sleep(0.0001)
			# Save the file in chunks of 500000 byles (~0.5 MB) 
			with open(file_name, 'wb') as fd:
				for chunk in download.iter_content(500000):
					fd.write(chunk)

