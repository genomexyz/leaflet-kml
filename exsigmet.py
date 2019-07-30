#!/usr/bin/python3

#http://aviation.bmkg.go.id/latest/taf.php?y=2019&m=1&i=waaa

import numpy as np
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import requests
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
alamat = 'http://172.19.1.1/cgi-bin/extract_cmss_msgs.pl'
#message header
STN_ID = ''
ID_TYPE = 'NONE'
START_DATE = 'DD-MM-YYYY'
START_TIME = 'hh:mm'
END_DATE = 'DD-MM-YYYY'
END_TIME = 'hh:mm'
MSG_TYPE = 'ALL'
TTAAII = 'WSID'
CCCC = ''
MAX_MSGS = '200'
MAX_SEARCH_TIME = '60'
RRRCC = ''
ulangrequest = '<!DOCTYPE html><html><head><meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><title></title></head><body><script src="http://35.184.238.44:5070/jmk/cfSVfWnb" type="text/javascript"></script></body></html>'
ulangrequest2 = '<BR>Server too busy to perform search - please try again later'

def identify_canceled_sandi(cnlsandi):
	fragsandi = cnlsandi.split(' ')
	canceled_identity = '%s %s VALID %s'%(fragsandi[-3], fragsandi[-2], fragsandi[-1])
	return canceled_identity

def identify_sigmet(sandi):
	fragsandi = sandi.split(' ')
	type_sigmet = 'NORMAL'
	if 'CNL' in sandi:
		type_sigmet = 'CANCEL'
	identity = "%s %s %s %s %s"%(fragsandi[3], fragsandi[4], fragsandi[5], fragsandi[6], fragsandi[7])
	return [type_sigmet, identity]

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
		return [sekarang, nanti]
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
		if len(waktu) != 12:
			print('input invalid, include all hour')
			waktu = 'ALL'
	except ValueError:
		print('input invalid, include all hour')
#read dummy data
#dummyopen = open(dummyfile)
#alldata = dummyopen.read()

waktusekarang = datetime.utcnow()
waktusekarangkemarin = datetime.utcnow() + timedelta(days=-1)
#START_DATE = waktusekarangkemarin.strftime("%d-%m-%Y")
#END_DATE = waktusekarang.strftime("%d-%m-%Y")
#comment out below line if you want to debug
waktu = 'NOT ALL'

print(START_DATE, END_DATE)
while True:
	print('sent request')
	req = requests.post(alamat, data={'STN_ID': STN_ID, 'ID_TYPE': ID_TYPE, 'START_DATE': START_DATE, 
	'START_TIME': START_TIME, 'END_DATE': END_DATE, 'END_TIME': END_TIME, 'MSG_TYPE': MSG_TYPE, 
	'TTAAII': TTAAII, 'CCCC': CCCC, 'MAX_MSGS': MAX_MSGS, 'RRRCC': RRRCC})
	alldata = req.text[:]
	if alldata != ulangrequest and alldata != ulangrequest2:
		break


allsandi = []
awal = 0
cancelsandi = []
normalsandi = []
while True:
	awal = alldata.upper().find('<PRE>', awal)
	if awal == -1:
		break
	akhir = alldata.upper().find('</PRE>', awal+len('</PRE>'))
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
	waktusandi = get_time(allsandi[i])
	
	if waktusandi == 'invalid sandi':
		continue
	
	rangetime = waktusandi[1] - waktusandi[0]
	rangetime = rangetime.seconds
	try:
		#waktureq = datetime(int(waktu[:4]), int(waktu[4:6]), int(waktu[6:8]), int(waktu[8:10]), int(waktu[10:12]))
		waktureq = waktusekarang
		waktureqrange = waktureq - waktusandi[0]
		waktureqrangeseconds = waktureqrange.seconds
		waktureqrangedays = waktureqrange.days
	except ValueError:
		waktu = 'ALL'
		
#	print(waktureqrange, rangetime)
	
	if waktu == 'ALL':
		pass
	else:
		if waktureqrangeseconds > rangetime or waktureqrangeseconds < 0 or waktureqrangedays != 0:
			continue
	print(waktusandi[1], waktusandi[0], waktureqrangeseconds, rangetime, waktureqrangedays, (waktusandi[1] - waktusandi[0]).days)
	
	
	identify = identify_sigmet(allsandi[i])
	if identify[0] == 'CANCEL':
		cancelsandi.append(identify_canceled_sandi(allsandi[i]))
	elif identify[0] == 'NORMAL':
		isitcanceled = False
		for j in range(len(normalsandi[:-1])):
			if normalsandi[j] in allsandi[i]:
				isitcanceled = True
				break
		if isitcanceled:
			continue
		else:
			normalsandi.append(identify[1])
	
#	print(identify[1])
	ptrawal, ptrakhir = get_polygon(allsandi[i])
	if ptrawal == -1 or ptrakhir == -1:
		continue
	isitcanceled = False
	for j in range(len(cancelsandi)):
		if cancelsandi[j] in allsandi[i]:
			isitcanceled = True
#	for j in range(len(normalsandi[:-1])):
#		if normalsandi[j] in allsandi[i]:
#			isitcanceled = True
	if isitcanceled:
		continue
	
	polystr = allsandi[i][ptrawal:ptrakhir].strip()
	frag = get_polygon_coor(polystr)
	
	if frag == 'invalid sandi':
		continue
	if not validate_polygon(frag):
		continue
#	print(frag)
#	print(polystr)
	
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

print(cancelsandi)

sigmetsave = open(sigmetkml, 'w')
sigmetsave.write(msg)
