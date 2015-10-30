import time
import serial
import requests
from bs4 import BeautifulSoup as bs


connected = False
r = requests.get("http://www.surfline.com/surf-forecasts/"
                 "northern-california/sf-san-mateo-county_2957/")

s = bs(r.text, "html.parser")
# Get the first day-slider-container
container = s.find('div', class_="day-slider-container")
# Get all <strong> element children in that container
conditions = container.find("strong")
wavesize = container.find("h1")
allwinds = s.find_all('div', class_="bar-chart-bar windbar bar-chart-five_day_column", limit=4)
periods = s.find_all('div', class_="bar-chart-period bar-chart-five_day_column", limit=4)
period = (int(periods[0].text[0]) + int(periods[1].text[0]) + int(periods[2].text[0]) + int(periods[3].text[0]))/4


while not connected:
    try:
        arduino = serial.Serial('/dev/cu.usbmodem1421', 9600)
        time.sleep(2) 
    except Exception as e:
        print e
        continue
    connected = True

arduino.write(str(conditions.text[0]))
time.sleep(1)
indicate = arduino.readline()

while True:
        arduino.write("Swell condition:" + str(conditions.text) + " at " + str(wavesize.text))
        time.sleep(1)

	indicate = arduino.readline()
	arduino.write("Winds at 5am:" + str(allwinds[0].text[2])  + " knots")
	time.sleep(1)

	indicate = arduino.readline()
	arduino.write("Winds at 11am:" + str(allwinds[1].text[2])  + " knots")
	time.sleep(1)

	indicate = arduino.readline()
	arduino.write("Winds at 5pm:" + str(allwinds[2].text[2])  + " knots")
	time.sleep(1)

	indicate = arduino.readline()
	arduino.write("Winds at 11pm:" + str(allwinds[3].text[2])  + " knots")
	time.sleep(1)
	indicate = arduino.readline()
