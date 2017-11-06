from imdb import IMDb
import csv
import re

#with open('zz-episode_data.csv', 'a') as csvfile:
#    writer = csv.writer(csvfile)

# process each title
with open('approved_titles.txt') as titles:
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
                #print title
                i.update(show, 'episodes')
                ### process each season and episode, print to csv
                for season in show['episodes']:
                    #print show['episodes'][season]
                    for episode in show['episodes'][season]:
                        #print episode
                        ep = show['episodes'][season][episode]
                        i.update(ep)

                        with open('zz-episode_data.csv', 'a') as myfile:
                            writer = csv.writer(myfile)
                            try:
                                epseries = ep['series title']
                            except:
                                epseries = "ZZ - SERIES NOT FOUND"
                               # print "series problem"

                            try:
                                eptitle = ep['title']
                            except:
                                eptitle = "ZZ - TITLE NOT FOUND"
                               # print "title problem"

                            try:
                                epruntime = ep['runtime'][-1].encode('ascii', 'ignore')
                                epruntime = re.sub('\D', '', epruntime)
                            except:
                                epruntime = 0
                                #print "runtime problem"

                            try:
                                epseason = ep['season']
                            except:
                                epseason = 0
                                #print "series number problem"

                            try:
                                epepisode = ep['episode']
                            except:
                                epepisode = 0
                                #print "episode number problem"

                            try:
                                epyear = ep['year']
                                #print epyear
                            except:
                                epyear = 0000
                                #print epyear

                            writer.writerow([epseries, eptitle, epruntime, epseason, epepisode, epyear])
                            print str(epseries), "|", str(eptitle), "|", epruntime,"|",  epseason,"|",  epepisode,"|",  epyear
                            #print [epseries, eptitle, epruntime, epseason, epepisode, epyear]
                        #with open('zz-episode_data.csv', 'a') as myfile:
                            #print "checking"
                            #writer = csv.writer(myfile)
                            #epseries = ep['series title']
                            #eptitle = ep['title']
                            #print ep['runtime'][-1]

                            #epruntime = ep['runtime'][-1].encode('ascii', 'ignore')
                            #epruntime = re.sub('\D', '', epruntime)
                            #print epruntime
                           # epseason = ep['season']
                            #epepisode = ep['episode']
                            #epyear = ep['year']
                            #try:
                            #    writer.writerow([epseries, eptitle, epruntime, epseason, epepisode, epyear])
                            #    print [epseries, eptitle, epruntime, epseason, epepisode, epyear]
                            #except:
                                # do nothing
                            #    print("episode skipped")
                '''
                            try:
                                epruntime = ep['runtime'][0]
                                epruntime = re.sub('\D', '', epruntime)
                                epruntime = epruntime.encode('ascii', 'ignore')
                                epruntime = int(epruntime)
                            except:
                                epruntime = 0
                                epseason = ep['season']
                                epepisode = ep['episode']
                                epyear = ep['year']
                                try:
                                    writer.writerow([epseries, eptitle, epruntime, epseason, epepisode, epyear])
                                    print [epseries, eptitle, epruntime, epseason, epepisode, epyear]
                                except:
                                    # do nothing
                                    print("episode skipped")
                                    '''
        except:
            print "error...skipping"