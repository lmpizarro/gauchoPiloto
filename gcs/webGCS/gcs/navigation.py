import time
import random

class nav_data ():
    def __init__(self):
	self.lat = 0
	self.lon = 0
	self.alt = 0
	self.course = 0
	self.speed = 0
        pass
    
    def get_nav_data(self):
	    self.lat = -34.6
	    self.lon = -58.38
	    self.alt = 100
	    self.course = 40
	    self.speed = 11
            w =  {"lat":5, "lon": 4, "alt":100, "time": time.time()}
	    geoJSON = {"geometry": {"type": "Point", "coordinates": [125.41323247048113, -19.904350571977524]}, "type": "Feature", "properties": {'id':1}}
            geoJSON['geometry']['coordinates'][0] = self.lon + random.gauss(0,0.001)
            geoJSON['geometry']['coordinates'][1] = self.lat + random.gauss(0,0.001)
	    ref_data = {'geo':geoJSON, 'alt':self.alt, 'course': self.course, 'speed':self.speed, 'time':time.time()}
	    return geoJSON 
