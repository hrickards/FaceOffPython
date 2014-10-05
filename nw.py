import requests
import math
from PIL import Image
import urllib2 as urllib
from process import *
import io

def nose_stats(data, idata):
	tags = data['photos'][0]['tags'][0]
	cen=tags['nose']

	cx=cen['x']
	cy=cen['y']
	fw=tags['width']
	fh=tags['height']

	print cx,cy
	print fw,fh
	print idata.size


if __name__ == "__main__":
	url="http://tinyurl.com/673cksr"
	data=process_sky_biometry(url)
	idata=image_process(url)
	nose_stats(data,idata)

