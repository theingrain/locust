from locust import HttpLocust, TaskSet, task
import locust.stats
import requests
import json
from tests.no_flow import SingleRequests
from tests.flow import SingleSessionMultipleRequests, MultiSessionMultipleRequests
import sys
sys.path.append('')
locust.stats.CSV_STATS_INTERVAL_SEC = 1

class NoFlowRequests(HttpLocust):
    task_set = SingleRequests
    host = ''
    min_wait = 5000
    max_wait = 20000

class SingleSessionFlowRequests(HttpLocust):
    task_set = SingleSessionMultipleRequests
    host = ''
    min_wait = 5000
    max_wait = 20000

class MultipleSessionFlowRequests(HttpLocust):
    task_set = MultiSessionMultipleRequests
    host = ''
    min_wait = 5000
    max_wait = 20000