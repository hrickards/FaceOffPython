import requests
import math
from PIL import Image
import urllib2 as urllib
from process import *
import io


nc=16

def norm(inp):
	return inp
	(x,y,z)=inp
	nx=((int)(x/nc))*nc
	ny=((int)(y/nc))*nc
	nz=((int)(z/nc))*nc
	return (nx,ny,nz)


dirs=[(1,0),(0,1),(-1,0),(0,-1)]


def check(i,j):
	if i<0:
		return 0
	if j<0:
		return 0
	if i>=iw:
		return 0
	if j>=ih:
		return 0
	if dist((i,j),(cx,cy))>=sr:
		return 0
	#print i,iw,j,ih
	if vis[(i,j)]==1:
		return 0
	return 1

def dist(a,b):
	sum=0
	for i in range(len(a)):
		dif=b[i]-a[i]
		dif=dif*dif
		sum=sum+dif
	return math.sqrt(sum)

def dfs(i,j,pix):
	global tx,ty,cn
	#print i,j,iw,ih
	##print pix[i,j]
	pix[i,j ]=(255,0,0)
	tx+=i
	ty+=j 
	cn+=1
	#print tx,ty,cn
	vis[(i,j)]=1
	for el in range(len(dirs)):
		nx=dirs[el][0]+i
		ny=dirs[el][1]+j
		if check(nx,ny)==1 and dist(tar,pix[nx,ny])<thresh:
			dfs(nx,ny,pix)


def nose_stats(data, idata):
	global iw,ih,cx,cy,sr,tar,tx,ty,cn,vis,tar,thresh
	pix=idata.load()
	mx=0
	#print len(data['photos'][0]['tags'])
	for person in range(len(data['photos'][0]['tags'])):
		tags = data['photos'][0]['tags'][person]
		cen=tags['nose']
		tar=(0,0,0)
		thresh=50
		ct=30


		fw=tags['width']
		fh=tags['height']
		(iw,ih)=idata.size
		cx=int(cen['x']*iw/100.0)
		cy=int(cen['y']*ih/100.0)
		print "nose",cx,cy
		vis={}
		for x in range(iw):
			for y in range(ih):
				vis[(x,y)]=0
		sr=0.20*(fw/100.0)*iw #search radius for nostril
		print "serach radius", sr
		res=[]
		for x in range(iw):
			for y in range(ih):
				if check(x,y)==1 and dist(tar,norm(pix[x,y]))<thresh:
					tx=0
					ty=0
					cn=0 
					dfs(x,y,pix)
					print "final", tx,ty,cn
					#print x,y,cn
					if(cn>ct):
						res.append((tx/cn,ty/cn))
		if(len(res)>=2):
			print res[0],res[1]
			draw_line(idata,res[0],res[1])
			mx=max(mx,dist(res[0],res[1]))
	save_image(idata,"andrew.png")
	return mx

def eye_stuff(data,idata):
	for person in range(len(data['photos'][0]['tags'])):
		tags = data['photos'][0]['tags'][person]
		a = tags['eye_left']
		la=(a['x'],a['y'])	
		b = tags['eye_right']
		lb=(b['x'],b['y'])	
		(iw,ih)=idata.size
		la=(la[0]*iw/100.0,la[1]*ih/100.0)
		lb=(lb[0]*iw/100.0,lb[1]*ih/100.0)
		print la,lb
		save_image(draw_line(idata,la,lb),"mid.png")

if __name__ == "__main__":
	#url="http://oi58.tinypic.com/302n9j7.jpg"
	url="http://i61.tinypic.com/2m2e79i.jpg"
	data=process_sky_biometry(url)
	idata=image_process(url)
	eye_stuff(data,idata)
	nose_stats(data,idata)
	for el in range(len(dirs)):
		print dirs[el][0],dirs[el][1]

