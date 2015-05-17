import time
import random
import math

class nav_data ():
    def __init__(self):
	self.lat = -34.6
	self.lon = -58.38
	self.alt = 100
	self.course = 40
	self.speed = 11
        pass
        self.angle = 0
	self.counter = 0
   
    def random_gen(self):
	self.lon += random.gauss(0,0.0001)
	self.lat += random.gauss(0,0.0001)

    def linear_lon_gen(self):
	self.lon = self.lon - 0.0005   

    def linear_lat_gen(self):
	self.lat = self.lat - 0.0005   

    def circle_gen (self, r, v, s, lat0, lon0):
	self.lat = lat0 + r * math.sin(self.angle)   
	self.lon = lon0 + r * math.cos(self.angle) 
        self.counter += s
	self.angle = self.counter * v


    def get_nav_data(self):
            w =  {"lat":5, "lon": 4, "alt":100, "time": time.time()}
	    geoJSON = {"geometry": {"type": "Point", "coordinates": [125.41323247048113, -19.904350571977524]},\
			    "type": "Feature", "properties": {'id':1}}
            #self.linear_lon_gen()
            #self.linear_lat_gen()
	    self.circle_gen(0.01, 0.1, 1, -34.6, -58.38)
	    self.random_gen()
            geoJSON['geometry']['coordinates'][0] = self.lon 
            geoJSON['geometry']['coordinates'][1] = self.lat 
	    ref_data = {'geo':geoJSON, 'alt':self.alt, 'course': self.course, 'speed':self.speed, 'time':time.time()}
	    return geoJSON 
