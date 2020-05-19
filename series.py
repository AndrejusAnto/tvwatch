#!/usr/bin/env python
# coding: utf-8

from threading import Thread
import imdb
from datetime import datetime
import json
import calendar
import os

tod = datetime.today()
listtod = [tod.year, tod.month, tod.day]
ia = imdb.IMDb()


def convert_dates(dates):
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
	"The Boys",
	"The Expanse",
	"The Good Doctor",
	"The Grand Tour",
	"The Mandalorian",
	"The Orville",
	"The Outsider",
	"The Witcher",
	"Sherlock",
	"True Detective",
	"Westworld",
]

dictseries = {}
atvaizdavimas = []
threads = []


def atrupdate(tod, ed):
	if ed != {}:
		pirmasalis = list(ed.keys())[0]
		data = convert_dates(ed[pirmasalis])
		return [1 if x == y else 0 for x, y in zip(data, tod) if len(data) < 3]


def collect_series(tv):
	try:
		seriesdict = {}
		ifserie = []
		tvseries = ia.search_movie(tv)
		for serie in tvseries:
			if not ifserie:
				seriesid = serie.movieID
				serieinfo = ia.get_movie(seriesid)
				serieyear = serieinfo["series years"]
				print(f'{serieinfo["title"]} | {serieyear} | ID{seriesid}')
				if serieinfo['kind'] == 'tv series' and tv == serieinfo['title']:
					ifserie.append(serieinfo['title'])
					pavad = f'{serieinfo["title"]} | {serieyear} | ID{seriesid}'
					seriesdict[pavad] = {}
					ia.update(serieinfo, 'episodes')
					seasonlist = []
					for i in serieinfo['episodes']:
						if i >= 0:
							seasonlist.append(i)
					for s in list(sorted(seasonlist)):
						listepiz = []
						sstring = f"S{s}"
						seriesdict[pavad][sstring] = {}
						print("episodes number", len(serieinfo['episodes'][s]))
						for k in serieinfo['episodes'][s]:
							listepiz.append(k)
						for e in listepiz:
							estring = f"E{e}"
							episodeid = serieinfo['episodes'][s][e].movieID
							seriesdict[pavad][sstring][estring] = {}
							countrydate = {}
							realesedata = ia.get_movie_release_dates(episodeid)['data']
							if realesedata:
								for reldate in realesedata['raw release dates']:
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
								countries = {k: v for (k, v) in sortedcd.items() if k in serieinfo['countries']}
								if countries:
									sortedcountries = dict(sorted(countries.items(), key=lambda x: x[1]))
									pirmasalis = list(sortedcountries.values())[0]
									for k, v in sortedcd.copy().items():
										if v < pirmasalis:
											del sortedcd[k]

									for k, v in sortedcd.items():
										sortedcd[k] = convert_dates(v)

									laiks = list(sortedcd.keys())
									laikd = list(sortedcd.values())
									for idx, v in enumerate(zip(laiks, laikd)):
										if v[0] in serieinfo['countries']:
											if convert_dates(v[1]) <= convert_dates(laikd[0]):
												laiks.remove(v[0])
												laikd.pop(idx)
												laiks.insert(0, v[0])
												laikd.insert(0, v[1])
									sortedcdn = dict(zip(laiks, laikd))
									seriesdict[pavad][sstring][estring][serieinfo['episodes'][s][e]['title']] = sortedcdn
									dictseries.update(seriesdict)
								else:
									seriesdict[pavad][sstring][estring][serieinfo['episodes'][s][e]['title']] = sortedcdn
									dictseries.update(seriesdict)
							else:
								seriesdict[pavad][sstring][estring][serieinfo['episodes'][s][e]['title']] = {}
								dictseries.update(seriesdict)
			else:
				continue
	except KeyError:
		pass


if not os.path.isfile("data_file.json"):
	for tvserie in watchseries:
		threads.append(Thread(target=collect_series, args=(tvserie,)))

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()

	with open("data_file.json", "w") as write_file:
		json.dump(dictseries, write_file, ensure_ascii=False, indent=4)
else:
	with open("data_file.json", "r") as read_file:
		data = json.load(read_file)

	for series, seriesinfo in data.items():
		laiksez = []
		for sezonas, sezonoi in seriesinfo.items():
			laiksez.append(int(sezonas[1:]))

		seriesid = [i.strip() for i in series.split("|")][-1]
		seriesid = "".join([i for i in seriesid if i.isdigit()])
		seriesy = [i.strip() for i in series.split("|")][1]
		seriesy = [i for i in seriesy.split("-") if i.isdigit()]
		aratn = True
		serieinfo = True
		for sezonas, sezonoi in seriesinfo.items():
			for epizodas, epizodoi in sezonoi.items():
				for epizodopavad, epizododatos in epizodoi.items():
					atr = atrupdate(listtod, epizododatos)
					if not epizododatos or ((sum(atr) == 1 and len(atr) == 1) or (sum(atr) == 2 and len(atr) == 2)):
						if aratn:
							print(series, epizodopavad, sezonas, epizodas)
							aratn = False
							print("Atnaujinama")
							serieinfo = ia.get_movie(seriesid)
							ia.update(serieinfo, 'episodes')

						print(series, epizodopavad, sezonas, epizodas)
						countrydate = {}
						epzname = serieinfo['episodes'][int(sezonas[1:])][int(epizodas[1:])]['title']
						episodeid = serieinfo['episodes'][int(sezonas[1:])][int(epizodas[1:])].movieID
						realesedata = ia.get_movie_release_dates(episodeid)['data']
						if realesedata:
							for reldate in realesedata['raw release dates']:
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
							countries = {k: v for (k, v) in sortedcd.items() if k in serieinfo['countries']}
							if countries:
								sortedcountries = dict(sorted(countries.items(), key=lambda x: x[1]))
								pirmasalis = list(sortedcountries.values())[0]
								for k, v in sortedcd.copy().items():
									if v < pirmasalis:
										del sortedcd[k]

								for k, v in sortedcd.items():
									sortedcd[k] = convert_dates(v)

								laiks = list(sortedcd.keys())
								laikd = list(sortedcd.values())
								for idx, v in enumerate(zip(laiks, laikd)):
									if v[0] in serieinfo['countries']:
										if convert_dates(v[1]) <= convert_dates(laikd[0]):
											laiks.remove(v[0])
											laikd.pop(idx)
											laiks.insert(0, v[0])
											laikd.insert(0, v[1])
								sortedcdn = dict(zip(laiks, laikd))
								data[series][sezonas][epizodas] = {epzname: sortedcdn}
							else:
								data[series][sezonas][epizodas] = {epzname: sortedcdn}
						else:
							continue
					else:
						if len(seriesy) < 2:
							print("len(seriesy) < 2", series, epizodopavad, sezonas, epizodas)
		else:
			continue

	with open("data_file.json", "w") as write_file:
		json.dump(data, write_file, ensure_ascii=False, indent=4)


with open("data_file.json", "r") as read_file:
	data = json.load(read_file)

atvaizdavimas = []
for sp in data.items():
	lepdict = {}
	lepdict[sp[0]] = []
	for s in sp[1].items():
		for e in s[1].items():
			for p in e[1].items():
				lepinfo = []
				ldatos = []
				for sd in p[1].items():
					a = sd[1].split()
					if len(a) == 3:
						if datetime.today() <= datetime.strptime(sd[1], "%Y %B %d"):
							met = int(a[0])
							men = list(calendar.month_name).index(a[1])
							die = int(a[2])
							if (met >= tod.year):
								if (men == tod.month) and (die >= tod.day):
									ldatos.append(sd)
								elif (men > tod.month):
									ldatos.append(sd)
					else:
						continue
				if ldatos:
					lepinfo = [s[0], e[0], p[0]]
					lepinfo.append(ldatos)
					lepdict[sp[0]].append(lepinfo)
	if lepdict[sp[0]]:
		atvaizdavimas.append(lepdict)

for i in atvaizdavimas:
	for k, v in i.items():
		print('---------------------------------------------')
		print('---------------------------------------------')
		print(tod.strftime("%Y %B %d"))
		print(f'Serialas "{k}"')
		for j in v:
			print('---------------------------------------------')
			print(f'****** {j[0]} {j[1]} "{j[2]}"')
			for d in j[-1]:
				print(f'****** {" ".join(d)}')
