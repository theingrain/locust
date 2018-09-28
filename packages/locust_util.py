import json
import requests

def get_cookie(login_req_body) :
	cookie_template = 'sid=<session_id>;path=/;uid=<user_id>;path=/'
	cookie_template = cookie_template.replace('<session_id>', login_req_body['detail']['session_id'])
	cookie_template = cookie_template.replace('<user_id>', login_req_body['detail']['user_id'])
	return cookie_template

def to_json(string_data) :
	string_data = string_data.replace("'", "\"")
	return json.loads(string_data)