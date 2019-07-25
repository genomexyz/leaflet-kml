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
strmarker = ['TOP', '=']

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

#def validate_polygon(polygonstr):
	

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
	polystr = allsandi[i][ptrawal:ptrakhir].strip()
	print(polystr)
#	allsandi[i] = allsandi[i].split()
#print(allsandi)
