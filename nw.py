import requests
import math
from PIL import Image
import urllib2 as urllib
from process import *
import io


nc=16

def norm(x,y):
	nx=((int)(x/nc))*nc
	ny=((int)(y/nc))*nc
	return (nx,ny)

vis=[[]]

dirs=[(1,0),(0,1),(-1,0),(0,-1)]

def dfs(i,j):
	if vis[i][j]==1:
		return
	for dx,dy in dirs:

	print vis[i][j]

def nose_stats(data, idata):
	tags = data['photos'][0]['tags'][0]
	cen=tags['nose']

	save_image(idata,"andrew.png")

	cx=cen['x']
	cy=cen['y']
	fw=tags['width']
	fh=tags['height']
	(iw,ih)=idata.size

	vis=[[0]*iw]*ih
	print vis

	sr=0.20*(fw/100.0)*iw #search radius for nostril




if __name__ == "__main__":
	url="http://tinyurl.com/673cksr"
	data=process_sky_biometry(url)
	idata=image_process(url)
	nose_stats(data,idata)

