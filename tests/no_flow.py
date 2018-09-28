from locust import HttpLocust, TaskSet, task
import requests
import json
import packages.models as model
import packages.requests_handler as http_request

class SingleRequests(TaskSet):

    @task
    def test_one(self):
        request = model.RequestModel('API_2')
        response = http_request.make_post_request(self.client, request)
        if response.json()['result'] == 'successful' :
            response.success()
        else :
            response.failure('Got Wrong Response')

    @task
    def test_four(self):
        request = model.RequestModel('API_1')
        response = http_request.make_post_request(self.client, request)
        if response.json()['result'] == 'successful' :
            response.success()
        else :
            response.failure('Got Wrong Response')

