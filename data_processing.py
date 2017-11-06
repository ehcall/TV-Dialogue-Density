import csv

series_names = {}
with open('zz-to_datamap.csv') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        # print row
        series = row[0]
        episode = row[1]
        runtime = row[2]
        season_num = row[3]
        episode_num = row[4]
        year = row[5]
        word_count = row[6]
        wpm = row[7]
        series_names[series] = series_names.get(series, {})
        series_names[series][episode] = series_names[series].get(episode, {"runtime": runtime, "season #": season_num,
                                                                           "episode #": episode_num, "year": year,
                                                                           "word count": word_count, "wpm": wpm})
        #print series, episode, series_names[series][episode]

total_average = []
years = {}
for series in series_names:
    seasons = {}
    series_wpm = []
    for episode in series_names[series]:
        season_num = series_names[series][episode]["season #"]
        wpm = series_names[series][episode]["wpm"]
        year = series_names[series][episode]["year"]
        years[year] = years.get(year, [])
        years[year].append(float(wpm))
        seasons[season_num] = seasons.get(season_num, [])
        seasons[season_num].append(float(wpm))
    for season in seasons:
        #print seasons[season]
        season_wpm = sum(seasons[season])/len(seasons[season])
        print series, ",", season,",", season_wpm
        series_wpm.append(season_wpm)
    print series, ",", "average",",", sum(series_wpm)/len(series_wpm)
    total_average.append(sum(series_wpm)/len(series_wpm))

print "total average",",", sum(total_average)/len(total_average)
for year in years:
    print year,",", (sum(years[year])/len(years[year]))
### get the average word count for each season
### get the average word count for each series
### get average word count total for all 40+ min shows
## get the average word count for each year

### graph!!!

### show better call saul and gilmore girls in context
### show averages for all episodes
### show averages for all seasons
### show averages for all seasons
### show averages for years
### (scatterplot?)