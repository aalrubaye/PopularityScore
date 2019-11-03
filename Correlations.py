import numpy
from scipy.stats import linregress
import urllib2
import pprint
from pymongo import MongoClient
import simplejson
from datetime import datetime
import time
import xlwt
import networkx as nx
import numpy as np
from iteration_utilities import unique_everseen

__author__ = 'Abdul Rubaye'

client = MongoClient()
database = client.github_10_01_2018
events = database.events
final_db = database.final
test_db = database.test
followers_db = database.final_follower
new_followers_db = database.new_final_follower

privateVar = open("privateVar.txt",'r').read()
client_id = privateVar.split('\n', 1)[0]
client_secret = privateVar.split('\n', 1)[1]

results = xlwt.Workbook(encoding="utf-8")

def remaining_rate():
    u = add_client_id_client_secret_to_url('https://api.github.com/rate_limit')
    el = fetch_info_from_url(u)
    # print ('*'*100)
    # print 'remaining limit = '+str(el['rate']['remaining'])
    # print ('*'*100)
    return el['rate']['remaining']

# appends the client id and the client secret to urls
def add_client_id_client_secret_to_url(url):
    query = '?per_page=100&client_id='+client_id+'&client_secret='+client_secret
    return url+query

#using a url fetch the callback object
def fetch_info_from_url(url):
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        data = simplejson.load(response)
        return data
    except urllib2.URLError, e:
        return None


# updates existing data objects in our mongo database
def update_database(entry, size, owner_followers):
    final_db.update({"_id": entry['_id']},
    {
        "forks": entry['forks'],
        "repo_created_at": entry['repo_created_at'],
        "repo_forks_count": entry['repo_forks_count'],
        "repo_language": entry['repo_language'],
        "repo_name": entry['repo_name'],
        "repo_stargazers_count": entry['repo_stargazers_count'],
        "repo_url": entry['repo_url'],
        "repo_watchers_count": entry['repo_watchers_count'],
        "stars": entry['stars'],
        "fork_array": entry['fork_array'],
        "star_array": entry['star_array'],
        "fork_array_one_week": entry['fork_array_one_week'],
        "star_array_one_week": entry['star_array_one_week'],
        "fork_array_two_weeks": entry['fork_array_two_weeks'],
        "star_array_two_weeks": entry['star_array_two_weeks'],
        "fork_array_three_weeks": entry['fork_array_three_weeks'],
        "star_array_three_weeks": entry['star_array_three_weeks'],
        "monthly_ps": entry['monthly_ps'],
        "one_week_ps": entry['one_week_ps'],
        "two_weeks_ps": entry['two_weeks_ps'],
        "three_weeks_ps": entry['three_weeks_ps'],
        "repo_size": size,
        "repo_owner_follower_count": owner_followers
    })

#going over each element in the database we fetch all the required info
# and create/update a new table in our database with the new data
def extract_info_from_db(offset, position):
    i = offset
    for e in final_db.find()[offset:position]:
        url = add_client_id_client_secret_to_url(e['repo_url'])
        elem = fetch_info_from_url(url)
        if elem is not None:
            size = elem['size']
            owner_url = add_client_id_client_secret_to_url(elem['owner']['url'])
            owner_elem = fetch_info_from_url(owner_url)
            if owner_elem is not None:
                owner_follwers_count = owner_elem['followers']
            else:
                owner_follwers_count = 0
        else:
            owner_follwers_count = 0
            size = 0


        update_database(e,size,owner_follwers_count)

        if i%50 == 0:
            u = add_client_id_client_secret_to_url('https://api.github.com/rate_limit')
            el = fetch_info_from_url(u)
            print ('*'*100)
            print 'remaining limit = '+str(el['rate']['remaining'])
            print ('*'*100)
        print i
        i+=1

#Finding the age of a repository in days
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def cal_correlation():
    i = 0

    # days = []
    # for e in final_db.find():
    #     d1 = (e['repo_created_at'])[0:10]
    #     d2 = (str(datetime.now()))[0:10]
    #     days.append(days_between(d1,d2))
    #     print i
    #     i+=1
    #
    # print days
    # k = 1
    # for ee in test_db.find():
    #     if k == 4:
    #         f_count = ee['repo_forks_count']
    #         lang = ee['repo_language']
    #         name = ee['repo_name']
    #         s_count = ee['repo_stargazers_count']
    #         url = ee['repo_url']
    #         w_count = ee['repo_watchers_count']
    #         size = ee['repo_size']
    #         o_f = ee['repo_owner_follower_count']
    #         m_ps = ee['monthly_ps']
    #         w_ps = ee['one_week_ps']
    #         two_w_ps = ee['two_weeks_ps']
    #         three_w_ps = ee['three_weeks_ps']
    #     k += 1
    #     print k



    # entry = {
    #     "repo_forks_count": f_count,
    #     "repo_language": lang,
    #     "repo_name": name,
    #     "repo_stargazers_count": s_count,
    #     "repo_url": url,
    #     "repo_watchers_count": w_count,
    #     "monthly_ps": m_ps,
    #     "one_week_ps": w_ps,
    #     "two_weeks_ps": two_w_ps,
    #     "three_weeks_ps": three_w_ps,
    #     "repo_size": size,
    #     "repo_owner_follower_count": o_f,
    #     "age": days
    # }
    #
    # test_db.insert(entry)

#Export repositories info to xls
def export_to_xls():
    sheet1 = results.add_sheet("Hello")
    i = 1
    j = 0
    for e in test_db.find():
        if i == 5:
            x1 = e["repo_name"]
            x2 = e["age"]
            x3 = e["repo_language"]
            x4 = e["repo_forks_count"]
            x5 = e["repo_stargazers_count"]
            x6 = e["repo_watchers_count"]
            x7 = e["repo_size"]
            x8 = e["repo_owner_follower_count"]
            x9 = e["one_week_ps"]
            x10 = e["two_weeks_ps"]
            x11 = e["three_weeks_ps"]
            x12 = e["monthly_ps"]
            x13 = e["repo_url"]

            for k in range(0, len(x1)):
                # if x12[k] != 0:
                sheet1.write(j, 0, x1[k])
                sheet1.write(j, 1, x2[k])
                sheet1.write(j, 2, x3[k])
                sheet1.write(j, 3, x4[k])
                sheet1.write(j, 4, x5[k])
                sheet1.write(j, 5, x6[k])
                sheet1.write(j, 6, x7[k])
                sheet1.write(j, 7, x8[k])
                sheet1.write(j, 8, x9[k])
                sheet1.write(j, 9, x10[k])
                sheet1.write(j, 10, x11[k])
                sheet1.write(j, 11, x12[k])
                sheet1.write(j, 12, x13[k])
                j += 1
            print j

        i += 1

    results.save("new_sheet2.xls")

def age_forks():
    # i = 1
    # af = [0] * 138
    # af_count = [0] * 138
    #
    #
    # for e in test_db.find():
    #
    #     if i == 5:
    #         age = e["age"]
    #         forks = e["repo_forks_count"]
    #         for j in range(0, len(age)):
    #             index = age[j]/30
    #             af[index] += (forks[j])
    #             af_count[index] += 1
    #     i+=1
    #
    #
    # print af
    # print af_count
    #
    sheet1 = results.add_sheet("Hello")
    # for k in range(0, len(af)):
    #     sheet1.write(k, 0, af[k])
    #     sheet1.write(k, 1, af_count[k])


    # index = 0

    month = [0]*60
    for e in final_db.find():
        forks = e['fork_array']
        ftotal = e['repo_stargazers_count']
        print forks
        # if index == 500:
        #     for i in range (0, len(forks)):
        #         print forks[i]
        #         if forks[i] != 0:
        #             fraction = float(forks[i]*100)/float(ftotal)
        #             month[i] += fraction
        #     # print month
        #     break
        # index+=1

    print month
    for k in range(0, len(month)):
        sheet1.write(k, 0, month[k])

    results.save("age_correlations3.xls")

#Find the correlation between age and other popularity measurements
def age_correlations():
    i = 1
    for e in test_db.find():
        if i == 5:
            # a = e['age']
            a = e["one_week_ps"]
            b = e["repo_size"]

            r = linregress(a, b)
            print r
            print "slope => "+ str(r[0])
            print "coeff => "+ str(r[2])
        i+=1

def fetch_followers(url):
    new_url = add_client_id_client_secret_to_url(url)
    elem = fetch_info_from_url(new_url)
    return elem

def create_db_with_followers():
    i = 1
    for e in test_db.find():
        if i == 5:
            name = e["repo_name"]
            age = e["age"]
            lang = e["repo_language"]
            fork = e["repo_forks_count"]
            star = e["repo_stargazers_count"]
            watch = e["repo_watchers_count"]
            size = e["repo_size"]
            of = e["repo_owner_follower_count"]
            wtps_1w = e["one_week_ps"]
            wtps_2w = e["two_weeks_ps"]
            wtps_3w = e["three_weeks_ps"]
            wtps_m = e["monthly_ps"]
            url = e["repo_url"]

            for k in range(12261, len(of)):
                x = url[k]
                followers_array = []
                if of[k] != 0:
                    for h in range(len(x)-1, 0, -1):
                        if x[h] == '/':
                            f_url = 'https://api.github.com/users'+x[28:h]+'/followers'
                            break

                    followers = fetch_followers(f_url)

                    if followers != None :
                        for ii in range(0, len(followers)):
                            followers_array.append(followers[ii]['login'])

                entry = {
                    "fork": fork[k],
                    "lang": lang[k],
                    "name": name[k],
                    "star": star[k],
                    "url": url[k],
                    "watch": watch[k],
                    "wtps_m": wtps_m[k],
                    "wtps_3w": wtps_3w[k],
                    "wtps_2w": wtps_2w[k],
                    "wtps_1w": wtps_1w[k],
                    "size": size[k],
                    "owner_f": len(followers_array) if len(followers_array) > of[k] else of[k],
                    "age": age[k],
                    "followers": followers_array
                }

                followers_db.insert(entry)

                rr = remaining_rate()
                print str(k) + "- Rate = " + str(rr)
                if rr < 60:
                    time.sleep(60)

        i += 1

def create_Model():
    graph = nx.Graph()
    s = []
    i = 0
    for e in new_followers_db.find():
        if (e['lang'] == 'Java') and (e['wtps_m'] > 0):
            s.append(e['name'])
            graph.add_node(e['name'], t=1, fork=e['fork'], star=e['star'], watch=e['watch'], wtps=e['wtps_m'], lang=('None' if e['lang']== None else e['lang']))
            for k in range (0, len(e['followers'])):
                graph.add_node(e['followers'][k], t=-1, fork=-1, star=-1, watch=-1, wtps=-1, lang='None')
                graph.add_edge(e['followers'][k], e['name'])
            i +=1
            if i>250:
                break
    # for kk in range (0, len(s)):
    #     for jj in range (kk+1, len(s)):
    #         graph.add_edge(s[kk], s[jj])


    graph.remove_nodes_from(list(nx.isolates(graph)))
    print nx.number_connected_components(graph)

    nx.write_graphml(graph, "/Users/Abduljaleel/Desktop/250.graphml")

def betweenness():
    graph = nx.read_graphml("/Users/Abduljaleel/Desktop/500.graphml")
    # nx.write_graphml(graph, "/Users/Abduljaleel/Desktop/watch_graph1500.graphml")
    # the node attribute in which we stored the popularity measurements
    # popularity_type = 'wtps'
    # popularity_type = 'fork'
    popularity_type = 'star'
    # popularity_type = 'watch'

    name = []
    popularity = []

    for (p, d) in graph.nodes(data=True):
        if d['t'] == 1:
            name .append(p)
            popularity.append(graph.nodes[p][popularity_type])

    print name
    print popularity

    n = numpy.argsort(popularity)

    z = 0
    print "---------------------------"
    # print nx.average_clustering(graph)
    print "---------------------------"
    for i in range (len(name)-1,1,-1):
        # print name[n[i]]
        graph.remove_node(name[n[i]])
        z += 1
        if z % 50 == 0:
            # graph.remove_nodes_from(list(nx.isolates(graph)))
            print z
            print nx.average_clustering(graph)
            print "---------------------------"

        if z == 500:
            nx.write_graphml(graph, "/Users/Abduljaleel/Desktop/watch_graph1000.graphml")
        elif z == 1000:
            nx.write_graphml(graph, "/Users/Abduljaleel/Desktop/watch_graph500.graphml")




if __name__ == "__main__":
    # age_forks()
    # age_correlations()
    # create_db_with_followers()
    create_Model()
    # betweenness()

    # for e in new_followers_db.find():
    #     pprint.pprint(e)



