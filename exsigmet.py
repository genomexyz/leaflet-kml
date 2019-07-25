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
dummyfile = 'contoh_cmss'

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

print(allsandi)
