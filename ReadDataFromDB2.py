import pprint
import urllib2
from pymongo import MongoClient
import simplejson
from datetime import datetime, timedelta
import time

__author__ = 'Abdul Rubaye'

client = MongoClient()
database = client.github_10_01_2018
events = database.events
final_db = database.final

# client id and client secret are used in calling the github API
# they will help to raise the maximum limit of calls per hour
# note: you will need your private txt file that includes the private keys
privateVar = open("privateVar2.txt",'r').read()
client_id = privateVar.split('\n', 1)[0]
client_secret = privateVar.split('\n', 1)[1]

remaining_requests = 5000
repos_stored = ''
fork_stars_counts_limit_wanted = 10000


def fetch_url_information(url,page, index):
    global remaining_requests
    if remaining_requests < 3000:
        dt = datetime.now() + timedelta(hours=1)
        stored = False
        while datetime.now() < dt:
            print ('rate limit exceeded, please wait... [currently on index = '+str(index)+']')
            if not stored:
                fw = open("repos_stored.txt","w")
                fw.write(repos_stored)
                fw.close()
                stored = True
            time.sleep(10)
        remaining_requests = 5000
        extract_data(index,index+5000)

    else:
        new_url = add_client_id_client_secret_to_url(url,page)
        try:
            request = urllib2.Request(new_url, headers={"Accept" : "application/vnd.github.v3.star+json"})
            response = urllib2.urlopen(request)
            remaining_requests -= 1
            data = simplejson.load(response)
            return data
        except urllib2.URLError, e:
            return None


# appends the client id and the client secret to urls
def add_client_id_client_secret_to_url(url,page):
    query = '?per_page=100&page='+str(page)+'&client_id='+client_id+'&client_secret='+client_secret
    return url+query


def fetch_forks(url, fork_counts, index):
    k = 1
    ee = {}
    pages = int(fork_counts/100)+1
    for page in range(pages):
        forks = fetch_url_information(url,page+1, index)
        if forks is not None:
            l = len(forks)
            for i in range(l):
                ee['fork'+str(k)] = {
                    'user': forks[i]['owner']['login'],
                    'date': forks[i]['created_at']
                }
                k += 1
    return ee


def fetch_stars(url, star_counts, index):
    k = 1
    ee = {}
    pages = int(star_counts/100)+1
    for page in range(pages):
        stars = fetch_url_information(url,page+1, index)
        if stars is not None:
            l = len(stars)
            for i in range (l):
                ee['star'+str(k)] = {
                    'user': stars[i]['user']['login'],
                    'date': stars[i]['starred_at']
                }
                k += 1
    return ee


def extract_data(offset, position):

    global repos_stored
    fw = open("repos_stored.txt",'r').read()
    repos_stored = fw

    index = offset
    for e in events.find()[offset:position]:
        repo = fetch_url_information(e['repo']['url'],1, index)
        if repo is not None:
            if (repo['forks_count'] < fork_stars_counts_limit_wanted) & (repo['stargazers_count'] < fork_stars_counts_limit_wanted):
                if repo['name'] not in repos_stored:
                    repos_stored += repo['name'] + ', '
                    entry = {
                                "repo_name": repo['name'],
                                "repo_created_at": repo['created_at'],
                                "repo_language": repo['language'],
                                "repo_forks_count": repo['forks_count'],
                                "repo_watchers_count": repo['subscribers_count'],
                                "repo_stargazers_count": repo['stargazers_count'],
                                "repo_url": e['repo']['url'],
                                # fork events
                                "forks": fetch_forks(repo['forks_url'], repo['forks_count'], index),
                                # watch events
                                "stars": fetch_stars(repo['stargazers_url'], repo['stargazers_count'], index)
                            }
                    print pprint.pprint(entry)
                    final_db.insert(entry)
        print str(index)+'...'+str(remaining_requests)
        index += 1
        print ('*'*100)


# The main function
if __name__ == "__main__":

    # finding the remaining limit rate of my GitHub requests
    remaining_requests = (fetch_url_information('https://api.github.com/rate_limit',1, 0))['resources']['core']['remaining']
    print (remaining_requests)

    offset = 500000
    position = offset + 5000

    extract_data(offset,position)
