import requests
import logging

from datetime import datetime

logging.basicConfig(filename="cronLogFile_{}.log".format(datetime.now()), level=logging.INFO)

response = requests.get('http://192.168.0.228:5000/cronjob')
logging.info(response.text)
logging.info("Status Code : " + str(response.status_code))


