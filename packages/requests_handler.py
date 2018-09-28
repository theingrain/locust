# Generic function for generating POST requests
def make_post_request(request_object, request_data):
	with request_object.post(request_data.endpoint, 
		headers=request_data.headers, data=str(request_data.body), catch_response=True) as response :
		return response