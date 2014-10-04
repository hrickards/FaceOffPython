import requests
import math
from PIL import Image
import urllib2 as urllib
import process
import io

def nose_stats(data):
	tags = data['photos'][0]['tags'][0]
	cen=tags['nose']
	cx=cen['x']
	cy=cen['y']
	fw=tags['width']
	fh=tags['height']
	print cx,cy
	print fw,fh


if __name__ == "__main__":
	url="http://tinyurl.com/673cksr"
	data=process.process_sky_biometry(url)
	nose_stats(data)

