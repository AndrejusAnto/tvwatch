#!/usr/bin/env python
# coding: utf-8

from threading import Thread
from datetime import datetime
from typing import Union
import imdb
import json
import os
import copy
import sys

tod = datetime.today()
listtod = [tod.year, tod.month, tod.day]
ia = imdb.IMDb()

# testuoju static typing dėl hint'ų
# Union[list, str] reiškia, kad funkcija convert_dates gali priimti tiek list'ą, tiek string'ą ir taip grąžinti tiek list'ą, tiek string'ą
def convert_dates(dates: Union[list, str]) -> Union[list, str]:
	if type(dates) == list:
		dates[0] = str(dates[0])
		if len(dates) == 1:
			return dates[0]
		else:
			if dates[1] == 1:
				dates[1] = "January"
			elif dates[1] == 2:
				dates[1] = "February"
			elif dates[1] == 3:
				dates[1] = "March"
			elif dates[1] == 4:
				dates[1] = "April"
			elif dates[1] == 5:
				dates[1] = "May"
			elif dates[1] == 6:
				dates[1] = "June"
			elif dates[1] == 7:
				dates[1] = "July"
			elif dates[1] == 8:
				dates[1] = "August"
			elif dates[1] == 9:
				dates[1] = "September"
			elif dates[1] == 10:
				dates[1] = "October"
			elif dates[1] == 11:
				dates[1] = "November"
			elif dates[1] == 12:
				dates[1] = "December"

			if len(dates) == 2:
				return " ".join(dates)
			else:
				dates[2] = str(dates[2])
				return " ".join(dates)
	elif type(dates) == str:
		d = dates.split()
		d[0] = int(d[0])
		if len(d) == 1:
			return d
		else:
			if d[1] == "January":
				d[1] = 1
			elif d[1] == "February":
				d[1] = 2
			elif d[1] == "March":
				d[1] = 3
			elif d[1] == "April":
				d[1] = 4
			elif d[1] == "May":
				d[1] = 5
			elif d[1] == "June":
				d[1] = 6
			elif d[1] == "July":
				d[1] = 7
			elif d[1] == "August":
				d[1] = 8
			elif d[1] == "September":
				d[1] = 9
			elif d[1] == "October":
				d[1] = 10
			elif d[1] == "November":
				d[1] = 11
			elif d[1] == "December":
				d[1] = 12

			if len(d) == 2:
				return d
			else:
				d[2] = int(d[2])
				return d


watchseries = [
	"Attack on Titan",
	"Better Call Saul",
	"Black Mirror",
	"Brooklyn Nine-Nine",
	"Killing Eve",
	"Lucifer",
	"One Punch Man",
	"Star Trek: Picard",
	"Stranger Things",
	"The Blacklist",
	"The Good Doctor",
	"The Grand Tour",
	"The Mandalorian",
	"The Orville",
	"The Outsider",
	"The Witcher",
	"Sherlock",
	"True Detective",
	"Westworld",
	"Goliath",
	"Doom Patrol",
	"F Is for Family",
	"The Boys",
	"The Expanse",
	"The Umbrella Academy",
	"Altered Carbon",
	"Curb Your Enthusiasm",
]

dictseries = {}


def pirmasal(tod, ed):
	if ed != {}:
		pirmasalis = list(ed.keys())[0]
		data = convert_dates(ed[pirmasalis])
		return data
	else:
		return ed


def getrd(rd):
	countrydate = {}
	for reldate in rd['raw release dates']:
		dates = list(reversed(reldate["date"].split()))
		sdates = " ".join(dates)
		countryname = reldate['country'].rstrip("\n")
		if countryname == "USA":
			countryname = "United States"
		if countryname == "UK":
			countryname = "United Kingdom"
		countrydate[countryname] = sdates
	for k, v in countrydate.items():
		countrydate[k] = convert_dates(v)
	sortedcd = dict(sorted(countrydate.items(), key=lambda x: x[1]))
	return sortedcd


def sorted_dates(cntr, sd, sic):
	sortedcountries = dict(sorted(cntr.items(), key=lambda x: x[1]))
	pirmasalis = list(sortedcountries.values())[0]
	for k, v in sd.copy().items():
		if v < pirmasalis:
			del sd[k]

	laiks = list(sd.keys())
	laikd = list(sd.values())
	for idx, v in enumerate(zip(laiks, laikd)):
		if v[0] in sic:
			if v[1] <= laikd[0]:
				laiks.remove(v[0])
				laikd.pop(idx)
				laiks.insert(0, v[0])
				laikd.insert(0, v[1])
	sortedcdn = dict(zip(laiks, laikd))
	return sortedcdn


def collect_series(tv, d):
	try:
		seriesdict = {}
		ifserie = True
		tvseries = ia.search_movie(tv)
		for serie in tvseries:
			if ifserie:
				seriesid = serie.movieID
				serieinfo = ia.get_movie(seriesid)
				serieyear = serieinfo["series years"]
				if serieinfo['kind'] == 'tv series' and tv == serieinfo['title']:
					ifserie = False
					pavad = f'{serieinfo["title"]} | {serieyear} | ID{seriesid}'
					print(pavad)
					seriesdict[pavad] = {}
					ia.update(serieinfo, 'episodes')
					seasonlist = [s for s in sorted(serieinfo['episodes'].keys()) if s > 0]
					for s in seasonlist:
						sstring = f"S{s}"
						seriesdict[pavad][sstring] = {}
						print("episodes number", len(serieinfo['episodes'][s]))
						for e in serieinfo['episodes'][s]:
							estring = f"E{e}"
							episodeid = serieinfo['episodes'][s][e].movieID
							seriesdict[pavad][sstring][estring] = {}
							releasedate = ia.get_movie_release_dates(episodeid)['data']
							if releasedate:
								sortedcd = getrd(releasedate)
								countries = {k: v for (k, v) in sortedcd.items() if k in serieinfo['countries']}
								if countries:
									sortedcdn = sorted_dates(countries, sortedcd, serieinfo['countries'])
									for k, v in sortedcdn.items():
										sortedcdn[k] = convert_dates(v)
									seriesdict[pavad][sstring][estring][serieinfo['episodes'][s][e]['title']] = sortedcdn
									d.update(seriesdict)
								else:
									for k, v in sortedcd.items():
										sortedcd[k] = convert_dates(v)
									seriesdict[pavad][sstring][estring][serieinfo['episodes'][s][e]['title']] = sortedcd
									d.update(seriesdict)
							else:
								seriesdict[pavad][sstring][estring][serieinfo['episodes'][s][e]['title']] = {}
								d.update(seriesdict)
			else:
				continue
	except KeyError:
		pass


def add_new(sie, d, sk, sa, series):
	atjsez = [s for s in sa if s not in sk]
	epzsk = [len(sie['episodes'][x]) for x in atjsez]
	for s, e in zip(atjsez, epzsk):
		laikepz = {}
		laiksez = {}
		for ee in range(1, e + 1):
			laikdata = {}
			episodeid = sie['episodes'][s][ee].movieID
			epzname = sie['episodes'][s][ee]['title']
			releasedate = ia.get_movie_release_dates(episodeid)['data']
			sstring = f"S{s}"
			estring = f"E{ee}"
			if releasedate:
				sortedcd = getrd(releasedate)
				countries = {k: v for (k, v) in sortedcd.items() if k in sie['countries']}
				if countries:
					sortedcdn = sorted_dates(countries, sortedcd, sie['countries'])
					for k, v in sortedcdn.items():
						sortedcdn[k] = convert_dates(v)
					laikdata = {epzname: sortedcdn}
					laikepz[estring] = laikdata
					laiksez[sstring] = laikepz
					d[series].update(laiksez)
				else:
					for k, v in sortedcd.items():
						sortedcd[k] = convert_dates(v)
					laikdata = {epzname: sortedcd}
					laikepz[estring] = laikdata
					laiksez[sstring] = laikepz
					d[series].update(laiksez)
			else:
				laikdata = {epzname: {}}
				laikepz[estring] = laikdata
				laiksez[sstring] = laikepz
				d[series].update(laiksez)


def update_old(d, series, s, e, ep, sei):
	episodeid = sei['episodes'][int(s[1:])][int(e[1:])].movieID
	epzname = sei['episodes'][int(s[1:])][int(e[1:])]['title']
	releasedate = ia.get_movie_release_dates(episodeid)['data']
	if releasedate:
		if epzname != ep:
			d[series][s][e][epzname] = d[series][s][e].pop(ep)

		sortedcd = getrd(releasedate)
		countries = {k: v for (k, v) in sortedcd.items() if k in sei['countries']}
		if countries:
			sortedcdn = sorted_dates(countries, sortedcd, sei['countries'])
			for k, v in sortedcdn.items():
				sortedcdn[k] = convert_dates(v)
			d[series][s][e].update({epzname: sortedcdn})
		else:
			for k, v in sortedcd.items():
				sortedcd[k] = convert_dates(v)
			d[series][s][e].update({epzname: sortedcd})


def update_series(series, data):
	seriesinfo = copy.deepcopy(data[series])
	seriesy = [i.strip() for i in series.split("|")][1]
	seriesy = [i for i in seriesy.split("-") if i.isdigit()]
	if len(seriesy) < 2:
		aratn = True
		serieinfo = True
		sezatn = []
		epzsk = []
		seriesid = [i.strip() for i in series.split("|")][-1]
		seriesid = "".join([i for i in seriesid if i.isdigit()])
		sezsk = [int(x[1:]) for x in seriesinfo.keys()]
		for sezonas, sezonoi in seriesinfo.items():
			for epizodas, epizodoi in sezonoi.items():
				for epizodopavad, epizododatos in epizodoi.items():
					atr = pirmasal(listtod, epizododatos)
					if "Episode #" in epizodopavad:
						if (len(atr) == 0) or (len(atr) == 3):
							if aratn:
								print(series)
								aratn = False
								print("Atnaujinama")
								serieinfo = ia.get_movie(seriesid)
								ia.update(serieinfo, 'episodes')

							sezatn = [s for s in sorted(serieinfo['episodes'].keys()) if s > 0]
							if sezsk != sezatn:
								add_new(serieinfo, data, sezsk, sezatn, series)
							else:
								# if sezsk != sezatn
								# if (len(atr) == 0) or (len(atr) == 3)
								update_old(data, series, sezonas, epizodas, epizodopavad, serieinfo)
						else:
							# if (len(atr) == 0) or (len(atr) == 3) salyga
							if (listtod[0] == atr[0]) and (listtod > atr):
								if aratn:
									print(series)
									aratn = False
									print("Atnaujinama")
									serieinfo = ia.get_movie(seriesid)
									ia.update(serieinfo, 'episodes')

								sezatn = [s for s in sorted(serieinfo['episodes'].keys()) if s > 0]
								if sezsk != sezatn:
									add_new(serieinfo, data, sezsk, sezatn, series)
								else:
									update_old(data, series, sezonas, epizodas, epizodopavad, serieinfo)
					else:
						# if "Episode #" in epizodopavad salyga
						if int(sezonas[1:]) == sezsk[-1]:
							if len(atr) == 0 or (listtod >= atr):
								if aratn:
									print(series)
									aratn = False
									print("Atnaujinama")
									serieinfo = ia.get_movie(seriesid)
									ia.update(serieinfo, 'episodes')

								sezatn = [s for s in sorted(serieinfo['episodes'].keys()) if s > 0]
								if sezsk != sezatn:
									add_new(serieinfo, data, sezsk, sezatn, series)
								else:
									# if sezsk != sezatn salyga
									update_old(data, series, sezonas, epizodas, epizodopavad, serieinfo)
						else:
							# if int(sezonas[1:]) == sezsk[-1] salyga
							continue


def atvaizdavimas(d):
	stdout_fileno = sys.stdout
	# Redirect sys.stdout to the file
	sys.stdout = open(f'{tod.year}_{tod.month}_{tod.day}.txt','wt')

	ifprin = True
	for serie, info in d.items():
		if ifprin:
			ifprin = False
			sys.stdout.write('---------------------------------------------'+ '\n')
			stdout_fileno.write('---------------------------------------------'+ '\n')
		ifprint = True
		for sez, sezi in info.items():
			for epz, epzi in sezi.items():
				for epzpav, epzd in epzi.items():
					ifepz = True
					ifkaz = False
					for sal, dt in epzd.items():
						ndt = convert_dates(dt)
						if (len(ndt) == 3) and ndt >= listtod:
							ifkaz = True
							if ifprint:
								ifprint = False
								sys.stdout.write('---------------------------------------------'+ '\n')
								stdout_fileno.write('---------------------------------------------'+ '\n')
								
								sys.stdout.write(tod.strftime("%Y %B %d")+ '\n')
								stdout_fileno.write(tod.strftime("%Y %B %d")+ '\n')
								
								sys.stdout.write(serie+ '\n')
								stdout_fileno.write(serie+ '\n')
							if ifepz:
								ifepz = False
								sys.stdout.write(f"***** {sez} {epz} {epzpav} *****"+ '\n')
								stdout_fileno.write(f"***** {sez} {epz} {epzpav} *****"+ '\n')
							sys.stdout.write(f'     {sal} {dt}'+ '\n')
							stdout_fileno.write(f'     {sal} {dt}'+ '\n')
					if ifkaz:
						sys.stdout.write('---------------------------------------------'+ '\n')
						stdout_fileno.write('---------------------------------------------'+ '\n')
	# Close the file
	sys.stdout.close()
	# Restore sys.stdout to our old saved file handler
	sys.stdout = stdout_fileno


def main():

	if not os.path.isfile("data_file.json"):
		threads = []

		for tvserie in watchseries:
			threads.append(Thread(target=collect_series, args=(tvserie, dictseries)))

		for thread in threads:
			thread.start()

		for thread in threads:
			thread.join()

		atvaizdavimas(dictseries)

		with open("data_file.json", "w") as write_file:
			dictseriesn = dict(sorted(dictseries.items()))
			json.dump(dictseriesn, write_file, ensure_ascii=False, indent=4)
	else:
		threads = []
		with open("data_file.json", "r") as read_file:
			data = json.load(read_file)

		seriesn = {i.split(" | ")[0]: i for i in list(data.keys())}
		for tvserie in watchseries:
			if tvserie in list(seriesn.keys()):
				threads.append(Thread(target=update_series, args=(seriesn[tvserie], data)))
			else:
				threads.append(Thread(target=collect_series, args=(tvserie, data)))

		for thread in threads:
			thread.start()

		for thread in threads:
			thread.join()

		atvaizdavimas(data)

		with open("data_file.json", "w") as write_file:
			data = dict(sorted(data.items()))
			json.dump(data, write_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
	main()