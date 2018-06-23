import RPi.GPIO as GPIO 
import time 
from datetime import datetime
import glob 
import urllib2
import datetime
import json
import calendar
import gcloud
from pyfcm import FCMNotification
from firebase import firebase


firebase = firebase.FirebaseApplication('https://monitoringapp-c5c2a.firebaseio.com/')


#userID taken from the user application entered below ensuring data goes into the right database table 
UID = ''
Token = firebase.get('users/'+UID+'/token', None)

#This will check input changes to the sensor, if input is detected it means the plants are watered, if there is no input detected it means the plants have fallen below the threshold and the user will be notified to water their plants
def read_moisture(channel):  
	if GPIO.input(channel):
		print "Plants watered" 
		dateWet = datetime.datetime.now().strftime("%H:%M %d/%m/%Y")
		moistureWet = str("Watered")
		sentWet = json.dumps(moistureWet, dateWet)
		firebase.post('Status/Moisture/CurrentStatus', sentWet)
		firebase.post('Status/Moisture/LastWatered', dateWet)
		
	else:
		print "20% Remaining"
		date = datetime.datetime.now().strftime("%H:%M %d/%m/%Y")
		moisture = str("Dry")
		sent = json.dumps(moisture, date)
		firebase.post('Status/Moisture/CurrentStatus', sent)
		pushNotification()


def pushNotification():
	push_service = FCMNotification(api_key="ENTER API KEY HERE")
	registration_id = Token
	message_title = 'Garden Gnome'
	message_body = 'Your plants need watered!'
	sound = 'default'
	result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body, sound=sound)

GPIO.setmode(GPIO.BCM)
channel = 17
GPIO.setup(channel, GPIO.IN)
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, read_moisture)



while True:
	time.sleep(0.1)
