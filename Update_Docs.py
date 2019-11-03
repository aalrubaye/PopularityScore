import pprint
from pymongo import MongoClient
import datetime

__author__ = 'Abdul Rubaye'

client = MongoClient()
database = client.github_10_01_2018
final_db = database.final


def update_database(entry, f_array, s_array):
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
        "fork_array": f_array,
        "star_array": s_array
    })

def update_database_weekly(entry, f_array, s_array):
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
        "fork_array_three_weeks": f_array,
        "star_array_three_weeks": s_array
    })


i = 1

# totalWeeklyForks = [0] * 265
# totalWeeklyStars = [0] * 265

for e in final_db.find():
    print e['repo_url']
    print ('-'*100)

    # forkArray = [0] * 88
    # starArray = [0] * 88
    #
    # for rf in e['forks']:
    #     forkDate = e['forks'][rf]['date']
    #     year = int(forkDate[0:4])
    #     month = int(forkDate[5:7])
    #     day = int(forkDate[8:10])
    #     dt = datetime.date(year, month, day)
    #     dd = dt.isocalendar()
    #     yyyy = dd[0]
    #     week = dd[1]
    #     if year > 2013:
    #         # fork_index = ((year-2014)*12)+(month-1)
    #         fork_index = (((yyyy-2014)*53)+(week)-1) / 3
    #         forkArray[fork_index] += 1
    #     # totalMonthlyForks[fork_index] += 1
    #
    # for rf in e['stars']:
    #     starDate = e['stars'][rf]['date']
    #     # print starDate
    #     year = int(starDate [0:4])
    #     month = int(starDate [5:7])
    #     day = int(starDate[8:10])
    #     dt = datetime.date(year, month, day)
    #     dd = dt.isocalendar()
    #     yyyy = dd[0]
    #     week = dd[1]
    #     if year > 2013:
    #         # star_index = ((year-2014)*12)+(month-1)
    #         star_index = (((yyyy-2014)*53)+(week)-1) / 3
    #         starArray[star_index] += 1
    #     # totalMonthlyStars[star_index] += 1
    #
    # # print forkArray
    # # print starArray
    # print ('-'*100)
    # update_database_weekly(e, forkArray, starArray)
    # print i
    # i += 1

# print totalMonthlyForks
# print totalMonthlyStars


#2017-09-05
#year = [0:4]
#month= [5:7]
#day  = [8:10]

# Please visit http://git-awards.com/about for more information


# s = '2018-12-31'
# year = int(s[0:4])
# month= int(s[5:7])
# day  = int(s[8:10])
#
# dt = datetime.date(year, month, day)
# dd = dt.isocalendar()
# y = dd[0]
# w = dd[1]
#
# index = ((y-2014)*53)+(w)-1
# index_2 = (((y-2014)*53)+(w)-1) / 3
# print dd
# print index + 1
# print index_2 + 1

