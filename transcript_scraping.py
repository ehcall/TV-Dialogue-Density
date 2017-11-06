import csv
import re





'''
series_names = {}
series_names[series] = {}
series_names[series][episode] = {}
series_names[series][episode]['runtime']
series_names[series][episode]['season #']
series_names[series][episode]['episode #']
series_names[series][episode]['year']
###then add
series_names[series][episode]['word count']
series_names[series][episode]['wpm']

Series Title	Episode Title	Episode Runtime	Season #	Episode # 	Year


'''
series_names = {}

#all_data = []
with open('zz-to_wpm.csv') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        #print row
        series = row[0]
        episode = row[1]
        runtime = row[2]
        season_num = row[3]
        episode_num = row[4]
        year = row[5]
        series_names[series] = series_names.get(series,{})
        series_names[series][episode] = series_names[series].get(episode,{"runtime": runtime,"season #": season_num, "episode #":episode_num, "year":year})
        #print series_names[series]
        #print series_names[series][episode]

import urllib2




from bs4 import BeautifulSoup
transcript_webpage = "http://transcripts.foreverdreaming.org/index.php"

import urllib2

def getSoup(webpage):

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    req = urllib2.Request(webpage, headers=hdr)

    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()
    soup = BeautifulSoup(page)
    return soup

mysoup = getSoup(transcript_webpage)
all_links = mysoup.find_all("a", class_="forumlink")
with open('zz-episode_data_wpm.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    ### go through each of the letter sections
    for link in all_links:
        href = link.get('href')
        url = "http://transcripts.foreverdreaming.org" + href[1:]

        ### get all the series links
        mysoup = getSoup(url)
        series_links = mysoup.find_all("a", class_="forumlink")
        #print series_links
        ### go through all the series links
        for series in series_links:
            href = series.get('href')
            url = "http://transcripts.foreverdreaming.org" + href[1:]
            #print url
            mysoup = getSoup(url)
            title = mysoup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['boxheading']).h2.string
            #print title
            ### check if the series name is within the list
            if title in series_names:
                episode_links = mysoup.find_all("a", class_="topictitle")
                try:
                    pages = mysoup.find("b", class_="pagination")
                    page_links = pages.findAll("a")
                    page_links = page_links[:-1]
                    #print page_links
                    for page in page_links:
                        href = page.get('href')
                        #print href
                        url = "http://transcripts.foreverdreaming.org" + href[1:]
                        #print url
                        mysoup = getSoup(url)
                        more_links = mysoup.find_all("a", class_="topictitle")
                        #print more_links
                        episode_links.extend(more_links)
                except:
                    print "no pagination"
                #print episode_links
                for episode in episode_links:
                    print episode
                    ### go to the episode webpage
                    href = episode.get('href')
                    url = "http://transcripts.foreverdreaming.org" + href[1:]
                    #print url
                    ### check if the episode name is within the series list
                    mysoup = getSoup(url)
                    ep_title = mysoup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['boxheading']).h2.string
                    #   ep_title = str(ep_title)
                    ep_title = re.sub(".*?\s-\s", "", ep_title)
                    #### I NEED TO FIX THIS
                    print ep_title
                    #print title
                    #if ep_title in series_names[title]: ### This may need to be changed to a different structure. coding it like this for now
                    ### if it is
                    ### get all paragraph tags
                    paragraphs = mysoup.find_all('p', class_=None)
                    #print paragraphs
                    word_count = 0
                    for line in paragraphs:


                        ### remove all lines with [], music notes, remove the character names if they exist

                        if len(line) > 0:
                            line = re.sub("<p>|</p>", "", str(line))
                            line = re.sub("\[.*?\]", " ", str(line))
                            line = re.sub("\(.*?\)", " ", str(line))
                            line = re.sub("^.*?: ", " ", str(line))
                            if len(line) > 0 and re.match("\w",line[0]):

                                ### remove all punctuation
                                line = re.sub("[^\s\w]","",line)
                                line = re.sub("<em>|</em>|<p>|</p>|<br/>|<strong>|</strong>", "", str(line))
                                #print line
                                ### get total word count for the episode
                                words = line.split()
                                word_count = word_count + len(words)
                                ### then add that to the other information...

                            #elif re.match("<",line[0]):



                    try:
                        series_names[title][ep_title]['word count'] = word_count
                        print word_count
                        runtime = series_names[title][ep_title]['runtime']
                        wpm = float(word_count)/float(runtime)
                        series_names[title][ep_title]['wpm'] = wpm
                        writer.writerow([title, ep_title, series_names[title][ep_title]["runtime"],
                                         series_names[title][ep_title]['season #'],
                                         series_names[title][ep_title]['episode #'],
                                         series_names[title][ep_title]['year'],
                                         series_names[title][ep_title]['word count'],
                                         series_names[title][ep_title]['wpm']])

                        print title, ep_title, series_names[title][ep_title]
                    except:
                        print "episode not found"
                        #del series_names[title][str(ep_title)]

