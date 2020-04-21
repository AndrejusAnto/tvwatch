#!/usr/bin/env python
# coding: utf-8

import imdb
from datetime import datetime
import json
import calendar
import os

tod = datetime.today()
ia = imdb.IMDb()


def convert_dates(date):
	d = date.split()
	if len(d) == 1:
		return d[0]
	else:
		if d[1] == "January":
			d[1] = "1"
		elif d[1] == "1":
			d[1] = "January"
		elif d[1] == "February":
			d[1] = "2"
		elif d[1] == "2":
			d[1] = "February"
		elif d[1] == "March":
			d[1] = "3"
		elif d[1] == "3":
			d[1] = "March"
		elif d[1] == "April":
			d[1] = "4"
		elif d[1] == "4":
			d[1] = "April"
		elif d[1] == "May":
			d[1] = "5"
		elif d[1] == "5":
			d[1] = "May"
		elif d[1] == "June":
			d[1] = "6"
		elif d[1] == "6":
			d[1] = "June"
		elif d[1] == "July":
			d[1] = "7"
		elif d[1] == "7":
			d[1] = "July"
		elif d[1] == "August":
			d[1] = "8"
		elif d[1] == "8":
			d[1] = "August"
		elif d[1] == "September":
			d[1] = "9"
		elif d[1] == "9":
			d[1] = "September"
		elif d[1] == "October":
			d[1] = "10"
		elif d[1] == "10":
			d[1] = "October"
		elif d[1] == "November":
			d[1] = "11"
		elif d[1] == "11":
			d[1] = "November"
		elif d[1] == "December":
			d[1] = "12"
		elif d[1] == "12":
			d[1] = "December"
		return " ".join(d)

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

seriesdict = dict()

if not os.path.isfile("data_file.json"):
	try:
		for tv in watchseries:
			ifserie = []
			tvseries = ia.search_movie(tv)
			for serie in tvseries:
				if not ifserie:
					print("TV ID", serie.movieID)
					serieid = ia.get_movie(serie.movieID)
					print(serieid['countries'])
					if serieid['kind'] == 'tv series' and tv == serieid['title']:
						ifserie.append(serieid['title'])
						seriesdict[serieid['title']] = {}
						ia.update(serieid, 'episodes')
						seasonlist = list()
						for i in serieid['episodes']:
							if i >= 0:
								seasonlist.append(i)
						for s in list(sorted(seasonlist)):
							listepiz = list()
							sstring = f"S{s}"
							seriesdict[serieid['title']][sstring] = {}
							print("episodes number", len(serieid['episodes'][s]))
							for k in serieid['episodes'][s]:
								listepiz.append(k)
							for e in listepiz:
								estring = f"E{e}"
								episodeid = serieid['episodes'][s][e].movieID
								seriesdict[serieid['title']][sstring][estring] = {}
								countrydate = dict()
								laiks = list()
								laikd = list()
								if ia.get_movie_release_dates(episodeid)['data']:
									for reldate in ia.get_movie_release_dates(episodeid)['data']['raw release dates']:
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
									for k, v in sortedcd.items():
										sortedcd[k] = convert_dates(v)
									for k, v in sortedcd.items():
										laiks.append(k)
										laikd.append(v)
									for idx, v in enumerate(zip(laiks, laikd)):
										if v[0] in serieid['countries']:
											laiks.remove(v[0])
											laikd.pop(idx)
											laiks.insert(0, v[0])
											laikd.insert(0, v[1])
									sortedcdn = dict(zip(laiks, laikd))
									seriesdict[serieid['title']][sstring][estring][serieid['episodes'][s][e]['title']] = sortedcdn
				else:
					continue
	except KeyError:
		pass

	with open("data_file.json", "w") as write_file:
		json.dump(seriesdict, write_file, ensure_ascii=False, indent=4)


with open("data_file.json", "r") as read_file:
	data = json.load(read_file)

duomenys = list()
for sp in data.items():
	lepdict = dict()
	lepdict[sp[0]] = list()
	for s in sp[1].items():
		for e in s[1].items():
			for p in e[1].items():
				lepinfo = list()
				ldatos = list()
				for sd in p[1].items():
					a = sd[1].split()
					if len(a) == 3:
						if datetime.today() <= datetime.strptime(sd[1], "%Y %B %d"):
							# print(datetime.today() <= datetime.strptime(sd[1], "%Y %B %d"))
							met = int(a[0])
							men = list(calendar.month_name).index(a[1])
							die = int(a[2])
							if (met >= tod.year):
								if (men == tod.month) and (die >= tod.day):
									ldatos.append(sd)
								elif (men > tod.month):
									ldatos.append(sd)
					# nepamiršti, kad jei naujausios serijos naujausia data jau praėjo
					# tai nerodyti visų datų
					else:
						continue
				if ldatos:
					lepinfo = [s[0], e[0], p[0]]
					lepinfo.append(ldatos)
					lepdict[sp[0]].append(lepinfo)
	if lepdict[sp[0]]:
		duomenys.append(lepdict)

# print("duomenys", duomenys)

for i in duomenys:
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
