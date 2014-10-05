import requests
import sys
import math
from PIL import Image, ImageDraw
import urllib2 as urllib
import io
from numpy import *

def process_image(image_url):
	sb_data = analyze_sky_biometry(process_sky_biometry(image_url))
	im_data = image_process(image_url)
	return {
		'sky_biometry': sb_data,
		'image_processing': im_data
	}

def save_image(im, name="out.png"):
	draw=ImageDraw.Draw(im)
	im.save(name, "PNG")

def image_process(image_url):
	# Download image
	f = urllib.urlopen(image_url)
	image_file = io.BytesIO(f.read())
	im = Image.open(image_file)
	save_image(im)
	rgb_im=im.convert('RGB')
	# Do all your image processing PIL stuff here
	return rgb_im
def process_sky_biometry(image_url):
	print image_url
	#return the json file
	request_data = {
		"api_key": "eb140cfa76244c9585b3642b638084e4",
		"api_secret": "100a3f93223045d7ba0fd10f3634c752",
		"urls": image_url,
		"attributes": "all" 
	}
	request = requests.get("http://api.skybiometry.com/fc/faces/detect.json", params=request_data)
	print request.json()
	return request.json()

def analyze_sky_biometry(data):
	# Do all your data analysis on data here
	return {
		"face_size": face_size(data),
		"eye_distance": eye_distance(data)
	}
def  draw_line(idata, lef, rig,steps=200):
	(lx,ly)=lef
	(rx,ry)=rig
	dy=ry-ly
	dx=rx-lx
	pix=idata.load()
	for ii in xrange(0,steps):
		i=ii/(steps*1.0)
		nx=int(lx+dx*i)
		ny=int(ly+dy*i)
		pix[nx,ny]=(255,0,0)
	return idata

def eye_test(data,idata):
	tags = data['photos'][0]['tags'][0]
	a = tags['eye_left']
	la=(a['x'],a['y'])	
	b = tags['eye_right']
	lb=(b['x'],b['y'])	
	(iw,ih)=idata.size
	la=(la[0]*iw/100.0,la[1]*ih/100.0)
	lb=(lb[0]*iw/100.0,lb[1]*ih/100.0)
	#print la,lb
	save_image(draw_line(idata,la,lb))
	
	
def bdfs(x, y, idata):
	global bvis, bpink
	
	if(bvis[x][y]):
		return 0
	
	bvis[x][y] = 1;
	dx=[0, 0, 1, -1]
	dy=[1, -1, 0, 0]
	(iw,ih)=idata.size
	
	res = 1
	
	for g in range(0,4):
		xx = x + dx[g]
		yy = y + dy[g]
		if(xx >= 0 and yy >= 0 and xx < iw and yy < ih):
			if(bvis[xx][yy] == 0 and bpink[xx][yy] == 1):
				res += bdfs(xx, yy, idata)
				idata.putpixel((xx, yy), (0,255,0))
				
				
	return res
				
	
def eye_area(data, idata,brig):
	global bvis, bpink
	sys.setrecursionlimit(1000000)
	mx=0
	for person in range(len(data['photos'][0]['tags'])):
		bvis= [[0 for i in range(5000)] for j in range(5000)]
		bpink=[[0 for i in range(5000)] for j in range(5000)]
		tags = data['photos'][0]['tags'][person]
		aaa = tags['eye_left']
		bbb = tags['eye_right']
		(iw,ih)=idata.size
		(fw,fh)=face_size(data)
		
		for x in range(0, iw):
			for y in range(0, ih):	
				bpink[x][y] = 0
				bvis[x][y] = 0
		m=1.2* brig/100.0
		wm=m/3	
		for x in range(0, iw - 1):
			for y in range(0, ih - 1):
				(r,g,b)=idata.getpixel((x,y))
				if(r > 110 and g > 90*wm and b > g + 10*wm and r > g - 10*wm and r < g + 25*wm and abs(b - g) < 50*wm):
					#idata.putpixel((x, y), (255,0,255))
					#idata.putpixel((x + 1, y), (255,0,255))
					#idata.putpixel((x, y + 1), (255,0,255))
					bpink[x][y] = 1;
					#bpink[x + 1][y] = 1;
					#bpink[x][y + 1] = 1;
				if(r + g + b < 150*m and abs(b - g) < 50*m and abs(b -r) < 50*m):
					#idata.putpixel((x, y), (255,0,255))
					#idata.putpixel((x + 1, y), (255,0,255))
					#idata.putpixel((x, y + 1), (255,0,255))
					bpink[x][y] = 1;
					#bpink[x + 1][y] = 1;
					#bpink[x][y + 1] = 1;
					
		
		eye1 = bdfs(int(aaa['x'] * iw / 100), int(aaa['y'] * ih / 100), idata)
		eye2 = bdfs(int(bbb['x'] * iw / 100), int(bbb['y'] * ih / 100), idata)
		
		eye1 /= (fw * fh) / 100
		eye2 /= (fw * fh) / 100
		
		#print eye1, eye2
		
		#bdfs(int(b['x'] * iw / 100), int(b['y'] * ih / 100), idata)	
		save_image(idata,"bojan.png")
		
		mx=max(mx,(eye1 + eye2) / 2)
	return mx
	

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
	
	#picture="http://i61.tinypic.com/21k9qba.jpg"
	#picture="http://i58.tinypic.com/35a3gwk.jpg"
	#picture="http://i61.tinypic.com/xnursl.jpg"
	
	idata=image_process(picture)
	data=process_sky_biometry(picture)
	print eye_area(data,idata)


