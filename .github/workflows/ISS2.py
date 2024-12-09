import json 
import turtle
import urllib.request 
import time 
import webbrowser 
import geocoder

# Fetch the current astronauts on the ISS
url = "http://api.open-notify.org/astros.json"
response = urllib.request.urlopen(url) 
result = json.loads(response.read())

# Write the astronaut information to a text file
file = open("iss.txt", "w") 
file.write("There are currently " + str(result["number"]) + " astronauts on the ISS: \n\n")
people = result["people"]

# Write the names of the crew
for p in people:
    file.write(p['name'] + " - on board" + "\n") 

# Get and write the current latitude and longitude
g = geocoder.ip('me') 
file.write("\nYour current lat / long is: " + str(g.latlng))
file.close()

# Open the text file in the default web browser
webbrowser.open("iss.txt")

# Setup the world map in turtle module
screen = turtle.Screen()
screen.setup(1280, 720)
screen.setworldcoordinates(-180, -90, 180, 90)

# Load the world map image
screen.bgpic("map.gif")

# Register and set the ISS icon shape
screen.register_shape("iss.gif")
iss = turtle.Turtle()
iss.shape("iss.gif")
iss.setheading(45)
iss.penup()

# Continuously update the ISS location on the map
while True:
    # Load the current status of the ISS in real-time
    url = "http://api.open-notify.org/iss-now.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())

    # Extract the ISS location
    location = result["iss_position"]
    lat = location['latitude']
    lon = location['longitude']

    # Output longitude and latitude to the terminal
    lat = float(lat)
    lon = float(lon)
    print("\nLatitude: " + str(lat))
    print("\nLongitude: " + str(lon))

    # Update the ISS location on the map
    iss.goto(lon, lat)

    # Refresh every 5 seconds
    time.sleep(5)

