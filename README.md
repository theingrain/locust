# API Load Testing (Locust/Python)

The tool supports and provide a rich envirnoment for http/https protocol based load testing.
Current project is build using locust version 0.9.0 and python 3.6

## **Installation**
1. Download and Install python version 3.6 based on your device from https://www.python.org/downloads/
2. Install locust version 0.9.0 via https://docs.locust.io/en/latest/installation.html

### **Dependencies Libraries:**
1. Plotly
2. Panda
3. Yattag
4. Ymal

## **Writing Tests**
There are very basic steps which are needed to be followed :
1. Add an API for which you need to make a `request to data/requests.yaml`
```
API_1 :
    TYPE : POST
    ENDPOINT : 
    HEADERS :
      Content-Type : application/json
    BODY :
      ent_id: 
      password: 
      remember_me: 
      service: 
      user_name: 
 ```
 #### Here :
 * `API_1` is your API description.
 * `TYPE` is your HTTP/HTTPS request type.
 * `ENDPOINT` is your api end point.
 * `HEADERS` are the header which you want to send with your request.
 * `BODY` is your body container.(Currently it resembles a json body but can be modified as well)
 
 2. Create a test class inside `locust/tests/` where we can add a test something like:
 ```
 class DemoTest(TaskSet):
 
    @task
    def test_demo(self):
        request = model.RequestModel('API_1')
        response = http_request.make_post_request(self.client, request)
        if response.status_code == 200 :
            response.success()
        else :
            response.failure('Wrong Response Code')

 ```
 #### Here :
 * Firstly a `request` object is created for `API_1` via model class present at ` locust/packages/models.py`.
 * `request` object is passed to `make_post_request` method at ` locust/packages/requests_handler.py` which is generic function for making POST requests.
 * The returned `response` object is then used to validate via assertions.
 
 3. Add your class to `locustfile.py`.
 

## **Running Your Tests**

There are basically two ways to launch/run the project :

### 1. Locust Web Interface
You could directly run the current test set by launching a command prompt / shell based on your choice of operating system and type in `locust --host=<Your Host Name>` in there inside your project directory. This will launch the localserver at 8089 port from where you could provide the number of user and hatch rate.
