import requests
import logging

from datetime import datetime


logging.basicConfig(filename="/home/praveen/Desktop/github_repos/Saama-Twitter_App/cronLogFile_{}.log".format(datetime.now()), level=logging.INFO)

try:
	

	response = requests.get('http://192.168.0.228:5000/cronjob')
	logging.info(response.text)
	logging.info("Status Code : " + str(response.status_code))


except Exception as error:
	logging.error("Error in execution scheduled task : " + str(error))	
