import pprint
import urllib2
from pymongo import MongoClient
import simplejson
from datetime import datetime, timedelta
import time

__author__ = 'Abdul Rubaye'

client = MongoClient()
database = client.github_10_01_2018
final_db = database.final


print final_db.count()

