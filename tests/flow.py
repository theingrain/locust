from locust import HttpLocust, TaskSet, task
import packages.locust_util as utility
import requests
import json
import packages.models as model
import packages.requests_handler as http_request

class SingleSessionMultipleRequests(TaskSet):
    cookies = None

    def on_start(self) :
        request = model.RequestModel('API_1')
        response = http_request.make_post_request(self.client, request)
        self.cookies = utility.get_cookie(response.json())
        if response.json()['detail']['user_name'] == request.body['user_name'] :
            response.success()
        else :
            response.failure('Got Wrong Response')

    @task
    def test_two(self):
        request = model.RequestModel('API_3')
        request.headers['Cookie'] = self.cookies
        response = http_request.make_post_request(self.client, request)
        if response.json()['result'] == 'successful' :
            response.success()
        else :
            response.failure('Got Wrong Response')


class MultiSessionMultipleRequests(TaskSet):
    cookies = None
    @task
    def test_three(self):
        request = model.RequestModel('API_1')
        response = http_request.make_post_request(self.client, request)
        self.cookies = utility.get_cookie(response.json())
        if response.json()['detail']['user_name'] == request.body['user_name'] :
            response.success()
        else :
            response.failure('Got Wrong Response')
        request = model.RequestModel('API_3')
        request.headers['Cookie'] = self.cookies
        response = http_request.make_post_request(self.client, request)
        if response.json()['result'] == 'successful' :
            response.success()
        else :
            response.failure('Got Wrong Response')        