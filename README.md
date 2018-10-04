# API Load Testing (Locust/Python)

The tool supports and provide a rich envirnoment for http/https protocol based load testing.
Current project is build using locust version `0.9.0` and `python 3.6`. It is also writtten to configure with CI tools such as Jenkins with Dashboard and Email reports functionality.

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
1. Add an API for which you need to make a request to `data/requests.yaml`
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
### 2. Locust No Web Interface
You could directly run the current test set by launching a command prompt / shell based on your choice of operating system and type in `locust --host=<Your Host Name> --csv=responses --no-web -c 1000 -r 100 -t 1m` in there inside your project directory. You could look up here https://docs.locust.io/en/stable/running-locust-without-web-ui.html for more details.

## **Setting Up Your CI For Run (Using Jenkins)**
**Steps**
1. Create a freestyle project.
2. Under `Source Code Management` provide repository path.
3. Under `Build` choose `Execute Shell` option and type in following in the command area :
```
locust --host=<Your Host Name> --csv=responses --no-web -c 1000 -r 100 -t 1m
python generate_reports.py $JENKINS_HOME\\jobs\\$JOB_NAME\\builds\\$BUILD_NUMBER\\log
```
4. Configur Email notifications with email template path as `reports\\email_summary.html`.
5. Configure HTML Publisher Plugin with path `reports\\dashboard_summary.html`.

* The following kind of dashboard will be generated :
![alt text](https://slack-imgs.com/?c=1&url=https%3A%2F%2Fscreenshotscdn.firefoxusercontent.com%2Fimages%2Fd2af51be-ea6d-444f-8c27-a1ca6bbdcdf6.png%3Fembedded%3Dog "Dashboard Summary")

* The following kind of emails will be sent :
![alt text](https://slack-imgs.com/?c=1&url=https%3A%2F%2Fscreenshotscdn.firefoxusercontent.com%2Fimages%2F978da82a-a8d7-4814-84c3-2cf2bb4d8cde.png%3Fembedded%3Dog "Email Summary")
