from imdb import IMDb
import csv
import re

with open('episode_data.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Series Title", "Episode Title", "Episode Runtime", "Season #", "Episode #, Year"])

#process each title
with open('titles.txt') as titles:
    for line in titles.readlines():
        title = line[:-1]
        i = IMDb()
        try:

            show_search = i.search_movie(title)
            ### get the id of the first search result

            tv_show = show_search[0].movieID

            ### use id to get the specific show
            show = i.get_movie(tv_show)
            if show['kind'] == 'tv series':
                ### get the runtime of the show, only process if it's >= 40m...or available
                try:
                    runtime = show['runtime']
                    stringrun = runtime[0].encode('ascii', 'ignore')
                    if int(stringrun) >= 40:
                        i.update(show, 'episodes')
                        ### process each season and episode, print to csv
                        for season in show['episodes']:
                            for episode in show['episodes'][season]:
                                ep = show['episodes'][season][episode]
                                i.update(ep)
                                with open('episode_data.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile)
                                    epseries = ep['series title']
                                    eptitle = ep['title']
                                    try:
                                        epruntime = ep['runtime'][-1]
                                        epruntime = re.sub('\D', '', epruntime)
                                        epruntime = epruntime.encode('ascii', 'ignore')
                                        epruntime = int(epruntime)
                                    except:
                                        epruntime = 0
                                    epseason = ep['season']
                                    epepisode = ep['episode']
                                    epyear = ep['year']
                                    try:
                                        if epruntime >= 40:
                                            writer.writerow([epseries, eptitle, epruntime, epseason, epepisode, epyear])
                                        print [epseries, eptitle, epruntime, epseason, epepisode, epyear]
                                    except:
                                        # do nothing
                                        print("episode skipped")
                except:
                    runtime = 0

            '''
           
                

                
                                '''
        except:
            print "error...skipping"