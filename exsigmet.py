#!/usr/bin/python3

#http://aviation.bmkg.go.id/latest/taf.php?y=2019&m=1&i=waaa

import numpy as np
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import csv
import sys
import pycurl
import sys

#setting
dummyfile = 'contoh_cmss.html'
sigmetkml = 'assets/sigmet.kml'
strmarker = ['TOP', '=']
height = 100
waktu = 'ALL'

def get_time(sandi):
	sekarangdefault = datetime.utcnow()
	fragsandi = sandi.split(' ')
	valid = fragsandi[7]
	try:
		sekarangsandi = valid[:6]
		nantisandi = valid[7:13]
		tahunsekarang = int(sekarangdefault.strftime('%Y'))
		bulansekarang = int(sekarangdefault.strftime('%m'))
		harisekarang = int(sekarangsandi[:2])
		jamsekarang = int(sekarangsandi[2:4])
		menitsekarang = int(sekarangsandi[4:6])
		sekarang = datetime(tahunsekarang, bulansekarang, harisekarang, jamsekarang, menitsekarang)
		
		harinanti = int(nantisandi[:2])
		jamnanti = int(nantisandi[2:4])
		menitnanti = int(nantisandi[4:6])
		if harisekarang == harinanti:
			selisihjam = jamnanti - jamsekarang
		else:
			selisihjam = 24 - jamsekarang + jamnanti
		selisihmenit = menitnanti - menitsekarang
		if selisihjam > 4 or selisihjam < 0:
			return 'invalid sandi'
		else:
			nanti = sekarang + timedelta(hours = selisihjam, minutes = selisihmenit)
		return sekarang, nanti
	except ValueError:
		return 'invalid sandi'


def get_polygon(sandi):
	akhir = -1
	awal = sandi.find('OBS WI')
	for i in range(len(strmarker)):
		akhir = sandi.find(strmarker[i], awal)
		if akhir != -1:
			break
	if awal == -1:
		return awal, akhir
	else:
		return awal+len('OBS WI'), akhir

def get_polygon_coor(polygonstr):
	try:
		polygonstrfrag = polygonstr.split('-')
		polycoorall = []
		for i in range(len(polygonstrfrag)):
			frag = polygonstrfrag[i].strip().split(' ')
			lonroundnumber = float(frag[1][1:4])
			lonpointnumber = float(frag[1][4:6]) / 100.
			lon = lonroundnumber + lonpointnumber
			if frag[1][0] == 'W':
				lon = -1. * lon
			latroundnumber = float(frag[0][1:3])
			latpointnumber = float(frag[0][3:5]) / 100.
			lat = latroundnumber + latpointnumber
			if frag[0][0] == 'S':
				lat = -1. * lat
			polycoorall.append([lat, lon])
	except IndexError:
		return 'invalid sandi'
	except ValueError:
		return 'invalid sandi'
	return polycoorall


def validate_polygon(polyarray):
	if polyarray[0] == polyarray[-1]:
		return True
	else:
		return False

if len(sys.argv) > 1:
	try:
		waktu = sys.argv[1]
		int(waktu)
		if len(waktu) != 6:
			print('input invalid, include all hour')
			waktu = 'ALL'
	except ValueError:
		print('input invalid, include all hour')
#read dummy data
dummyopen = open(dummyfile)
alldata = dummyopen.read()

allsandi = []
awal = 0
while True:
	awal = alldata.find('<PRE>', awal)
	if awal == -1:
		break
	akhir = alldata.find('</PRE>', awal+len('</PRE>'))
	if akhir == -1:
		break
	sandi = alldata[awal+len('<PRE>'):akhir]
	awal = awal+len('<PRE>')
	akhir = akhir+len('</PRE>')
	allsandi.append(sandi)

msg = '<?xml version="1.0" encoding="UTF-8"?>\n'
msg += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
for i in range(len(allsandi)):
	while '\n' in allsandi[i]:
		allsandi[i] = allsandi[i].replace('\n', ' ')
	while '\t' in allsandi[i]:
		allsandi[i] = allsandi[i].replace('\t', ' ')
	while '  ' in allsandi[i]:
		allsandi[i] = allsandi[i].replace('  ', ' ')
	allsandi[i] = allsandi[i].strip()
	ptrawal, ptrakhir = get_polygon(allsandi[i])
	if ptrawal == -1 or ptrakhir == -1:
		continue
	
	if waktu == 'ALL':
		pass
	
	polystr = allsandi[i][ptrawal:ptrakhir].strip()
	frag = get_polygon_coor(polystr)
	
	if frag == 'invalid sandi':
		continue
	if not validate_polygon(frag):
		continue
	print(frag)
	print(polystr)
	
	#build xml
	msg += '<Placemark>\n'
	msg += '<name>%s</name>\n'%(allsandi[i])
	msg += '<Polygon>\n'
	msg += '<extrude>1</extrude>\n'
	msg += '<altitudeMode>relativeToGround</altitudeMode>\n'
	msg += '<outerBoundaryIs>\n'
	msg += '<LinearRing>\n'
	msg += '<coordinates>\n'
	for i in range(len(frag)):
		msg += '%f,%f,%i\n'%(frag[i][1], frag[i][0], height)
	msg += '</coordinates>\n'
	msg += '</LinearRing>\n'
	msg += '</outerBoundaryIs>\n'
	msg += '</Polygon>\n'
	msg += '</Placemark>\n'
#	allsandi[i] = allsandi[i].split()
#print(allsandi)
msg += '</kml>'

sigmetsave = open(sigmetkml, 'w')
sigmetsave.write(msg)
