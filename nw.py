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
	#print i,j 
	if vis[i][j]==1:
		return
	print pix[i,j]
	tx+=i
	ty+=j 
	cn+=1
	#print tx,ty,cn
	vis[i][j]=1
	for (dx,dy) in dirs:
		nx=dx+i
		ny=dy+j
		nco=norm(pix[nx,ny])
		if check(nx,ny)==1 and dist(tar,nco)<thresh:
			dfs(nx,ny,pix)


def nose_stats(data, idata):
	global iw,ih,cx,cy,sr,tar,tx,ty,cn,vis,tar,thresh
	tags = data['photos'][0]['tags'][0]
	cen=tags['nose']
	vis=[[]]
	tar=(0,0,0)
	thresh=100
	ct=30

	save_image(idata,"andrew.png")

	cx=cen['x']
	cy=cen['y']
	fw=tags['width']
	fh=tags['height']
	(iw,ih)=idata.size
	vis=[[0]*iw]*ih
	pix=idata.load()
	sr=0.80*(fw/100.0)*iw #search radius for nostril
	print "serach radius", sr
	res=[]
	for x in range(iw):
		for y in range(ih):
			if check(x,y)==1 and dist(tar,norm(pix[x,y]))<thresh and vis[x][y]==0:
				tx=0
				ty=0
				cn=0 
				dfs(x,y,pix)
				#print "final", tx,ty,cn
				print x,y,cn
				if(cn>ct):
					res.append((tx/cn,ty/cn))
	print res
	return 0

if __name__ == "__main__":
	url="http://tinyurl.com/673cksr"
	data=process_sky_biometry(url)
	idata=image_process(url)
	nose_stats(data,idata)

