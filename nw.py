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
def getB(data,idata):
	global brig
	tags = data['photos'][0]['tags'][0]
	w = data['photos'][0]['width'] / 100.0
	h = data['photos'][0]['height'] / 100.0
	fw=tags['width']*w
	fh=tags['height']*h	
	gs=idata.convert('L')
	pix=gs.load()
	(iw,ih)=gs.size
	sm=0
	cx=int(tags['nose']['x']*iw/100.0)
	cy=int(tags['nose']['y']*ih/100.0)
	rad=(fw+fh)/4
	cnt=0
	for x in range(iw):
		for y in range(ih):
			if dist((cx,cy),(x,y))<rad:
				cnt+=1
				sm+=pix[x,y]
				pix[x,y]=0
	save_image(gs,"gray.png")
	brig=sm/cnt

def nose_stats(data, idata):
	global iw,ih,cx,cy,sr,tar,tx,ty,cn,vis,tar,thresh,ncx,ncy
	pix=idata.load()
	mx=0
	#print len(data['photos'][0]['tags'])
	for person in range(len(data['photos'][0]['tags'])):
		tags = data['photos'][0]['tags'][person]		
		cen=tags['nose']
		tar=(0,0,0)
		thresh=brig
		ct=10
		fw=tags['width']
		fh=tags['height']
		(iw,ih)=idata.size
		cx=int(cen['x']*iw/100.0)
		cy=int(cen['y']*ih/100.0)
		ncx=cx
		ncy=cy
		#print "nose",cx,cy
		vis={}
		for x in range(iw):
			for y in range(ih):
				vis[(x,y)]=0
		sr=0.12*(fw/100.0)*iw #search radius for nostril
		#print "serach radius", sr
		res=[]
		for x in range(iw):
			for y in range(ih):
				if check(x,y)==1 and dist(tar,norm(pix[x,y]))<thresh:
					tx=0
					ty=0
					cn=0 
					dfs(x,y,pix)
					#print "final", tx,ty,cn
					#print x,y,cn
					if(cn>ct):
						res.append((tx/cn,ty/cn))
		if(len(res)>=2):
			#print res[0],res[1]
			draw_line(idata,res[0],res[1])
			ncx=(res[0][0]+res[1][0])/2
			ncy=(res[0][1]+res[1][1])/2
			mx=max(mx,dist(res[0],res[1]))
	return mx*100.0/iw

def eye_stuff(data,idata):
	global ecx,ecy
	mx=0
	for person in range(len(data['photos'][0]['tags'])):
		tags = data['photos'][0]['tags'][person]
		a = tags['eye_left']
		la=(a['x'],a['y'])	
		b = tags['eye_right']
		lb=(b['x'],b['y'])	
		(iw,ih)=idata.size
		la=(la[0]*iw/100.0,la[1]*ih/100.0)
		lb=(lb[0]*iw/100.0,lb[1]*ih/100.0)
		ecx=(la[0]+lb[0])/2
		ecy=(la[1]+lb[1])/2
		#print la,lb
		mx=max(mx, dist(la,lb))
		draw_line(idata,la,lb)
	return mx*100.0/iw

def face_ratio(data,idata,steps=500):
	tags = data['photos'][0]['tags'][0]
	w = data['photos'][0]['width'] / 100.0
	h = data['photos'][0]['height'] / 100.0
	fw=tags['width']*w
	fh=tags['height']*h
	cx=tags['center']['x']*w
	cy=tags['center']['y']*h
	#draw_line(idata,(cx-fw/2,cy-fh/2),(cx-fw/2,cy+fh/2))
	#draw_line(idata,(cx+fw/2,cy-fh/2),(cx+fw/2,cy+fh/2))
	#draw_line(idata,(cx-fw/2,cy+fh/2),(cx+fw/2,cy+fh/2))
	#draw_line(idata,(cx-fw/2,cy-fh/2),(cx+fw/2,cy-fh/2))
	rad=((fw+fh)/4)*1.25
	pix=idata.load()
	for ii in xrange(0,steps):
		i=ii*math.pi/steps
		nx=int(cx+rad*math.sin(i))
		ny=int(cy+rad*math.cos(i))
		pix[nx,ny]=(0,0,255)
		nx=int(cx-rad*math.sin(i))
		ny=int(cy-rad*math.cos(i))
		pix[nx,ny]=(0,0,255)
	return (tags['width']*w*1.0)/(tags['height']*h)

def nose_height(data,idata):
	draw_line(idata,(ncx,ncy),(ecx,ecy))
	leng=dist((ncx,ncy),(ecx,ecy))*100.0/ih
	return leng
	
def gender(data,idata):
	tags = data['photos'][0]['tags'][0]
	atrs=tags['attributes']
	return atrs['gender']['value']

def mood(data,idata):
	tags = data['photos'][0]['tags'][0]
	atrs=tags['attributes']
	return atrs['mood']['value']
	

def lips(data,idata):
	tags = data['photos'][0]['tags'][0]
	atrs=tags['attributes']
	return atrs['lips']['value']


def glasses(data,idata):
	tags = data['photos'][0]['tags'][0]
	atrs=tags['attributes']
	return atrs['glasses']['value']

def smiling(data,idata):
	tags = data['photos'][0]['tags'][0]
	atrs=tags['attributes']
	return atrs['smiling']['value']

def surreal_analysis(url):
	data=process_sky_biometry(url)
	idata=image_process(url)
	getB(data,idata)
	
	save_image(idata, 'final.png')
	returns = {
	        'brightness': brig,
	        'nose_width': nose_stats(data, idata),
	        'eye_length': eye_stuff(data, idata),
	        'face_ratio': face_ratio(data, idata),
	        'nose_length': nose_height(data, idata),
	        'gender': gender(data, idata),
	        'glasses': glasses(data, idata),
	        'mood': mood(data, idata),
	        'smiling': smiling(data, idata),
	        'lips': lips(data, idata),
	        'output_image': 'final.png'
	        }
	if (glasses(data, idata) != 'true'):
		returns['eye_area'] = eye_area(data, idata, brig)
		
	        

if __name__ == "__main__":
	#url="http://i62.tinypic.com/25h20xd.jpg" #zach without glasses
	#url="http://i60.tinypic.com/2it4l6f.jpg" #zach with glasses
	#url="http://i62.tinypic.com/dnbmea.jpg"#eugene without glasses
	#url="http://i62.tinypic.com/2hi886e.jpg" #eugene with glasses
	#url="http://i61.tinypic.com/21k9qba.jpg" #bojan looking forward
	#url="http://i58.tinypic.com/35a3gwk.jpg" #andrew normal
	#url="http://i59.tinypic.com/2lixyjq.jpg" #brenda too white
	#url="http://i61.tinypic.com/xnursl.jpg"	 #bojan creep face
	#url="http://i61.tinypic.com/2m2e79i.jpg" #akshat and multiple randoms
	#url="http://i61.tinypic.com/rrmas7.jpg" #harry
	#BAD url="http://i59.tinypic.com/90uek8.jpg" #bojan and akshat
	#url="http://i59.tinypic.com/fxs5cg.jpg" #bojan with glasses and birdie
	url="http://i62.tinypic.com/24zkfty.jpg"
	data=process_sky_biometry(url)
	idata=image_process(url)
	getB(data,idata)
	print "birghtness value=",brig
	if(glasses(data,idata)!='true'):
		print "normalized eye area= ",eye_area(data,idata,brig)
	print "normalized nose width= ",nose_stats(data,idata)
	print "normalized eye length= ",eye_stuff(data,idata)
	print "face ratio= ",face_ratio(data,idata)
	print "normalized nose length= ",nose_height(data,idata)
	print "gender= ",gender(data,idata)
	print "glasses= ",glasses(data,idata)
	print "mood= ",mood(data,idata)
	print "smiling= ",smiling(data,idata)
	print "lips= ",lips(data,idata)
	
	save_image(idata,"final.png")
