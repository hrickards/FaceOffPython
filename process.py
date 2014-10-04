import requests
import math
from PIL import Image
import urllib2 as urllib
import io


def process_image(image_url):
	sb_data = process_sky_biometry(image_url)
	im_data = image_process(image_url)
	return {
		'sky_biometry': sb_data,
		'image_processing': im_data
	}

def image_process(image_url):
	# Download image
	f = urllib.urlopen(image_url)
	image_file = io.BytesIO(f.read())
	im = Image.open(image_file)
	rgb_im=im.convert('RGB')
	r,g,b=rgb_im.getpixel((1,1))
	print r,g,b
	# Do all your image processing PIL stuff here
	return {
		'size': im.size
	}

def process_sky_biometry(image_url):
	request_data = {
		"api_key": "eb140cfa76244c9585b3642b638084e4",
		"api_secret": "100a3f93223045d7ba0fd10f3634c752",
		"urls": image_url,
		"attributes": "all" 
	}
	request = requests.get("http://api.skybiometry.com/fc/faces/detect.json", params=request_data)
	return analyze_sky_biometry(request.json())

def analyze_sky_biometry(data):
	# Do all your data analysis on data here
	return {
		"face_size": face_size(data),
		"eye_distance": eye_distance(data)
	}

def face_size(result):
	tags = result['photos'][0]['tags'][0]
	w = result['photos'][0]['width'] / 100.0
	h = result['photos'][0]['height'] / 100.0

	return [tags['width']*w, tags['height']*h]

def eye_distance(result):
	tags = result['photos'][0]['tags'][0]
	a = tags['eye_left']
	b = tags['eye_right']
	x = (a['x'] - b['x']) * result['photos'][0]['width'] / 100.0
	y = (a['y'] - b['y']) * result['photos'][0]['height'] / 100.0

	return math.sqrt(x*x + y*y)

# If file is run directly
if __name__ == "__main__":
	print process_image("http://tinyurl.com/673cksr")


