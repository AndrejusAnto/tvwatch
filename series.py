#!/usr/bin/env python
# coding: utf-8

import imdb
import datetime
import json
import calendar
import os

tod = datetime.datetime.today()
ia = imdb.IMDb()

watchseries = [
	# "Attack on Titan",
	# "Better Call Saul",
	# "Black Mirror",
	# "Brooklyn Nine-Nine",
	# "Killing Eve",
	# "Lucifer",
	# "One Punch Man",
	# "Star Trek: Picard",
	# "Stranger Things",
	# "The Blacklist",
	# "The Boys",
	# "The Expanse",
	# "The Good Doctor",
	# "The Grand Tour",
	# "The Mandalorian",
	# "The Orville",
	# "The Outsider",
	"The Witcher",
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
					print("movieID", serie.movieID)
					serieid = ia.get_movie(serie.movieID)
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
								if ia.get_movie_release_dates(episodeid)['data']:
									for reldate in ia.get_movie_release_dates(episodeid)['data']['raw release dates']:
											dates = list(reversed(reldate["date"].split()))
											sdates = " ".join(dates)
											countryname = reldate['country'].rstrip("\n")
											countrydate[countryname] = sdates
									seriesdict[serieid['title']][sstring][estring][serieid['episodes'][s][e]['title']] = countrydate
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
				print("p", p)
				for sd in p[1].items():
					# print(sd)
					a = sd[1].split()
					if len(a) == 3:
						# print("p1", p[1])
						# print("sp0", sp[1])
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
	duomenys.append(lepdict)

print("duomenys", duomenys)
for i in duomenys:
	for k, v in i.items():
		if v:
			print('---------------------------------------------')
			print('---------------------------------------------')
			print(tod.strftime("%Y %B %d"))
			print(f'Serialas "{k}"')
			for j in v:
				print('---------------------------------------------')
				print(f'****** {j[0]} {j[1]} "{j[2]}"')
				for d in j[-1]:
					print(f'****** {" ".join(d)}')


