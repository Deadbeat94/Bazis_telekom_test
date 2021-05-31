import pytest
import requests
import random
import string


def test_create_user(user_generator):
	url = user_generator[0] + 'users'	
	payload = {'username': f'{user_generator[1]}', 'password1': f'{user_generator[2]}', 'password2': f'{user_generator[2]}'}
	page = requests.post(url, json=payload)
	assert page.status_code == 201 and page.json()["result"] == f'New user {user_generator[1]} successfully created'


def test_login(existing_user):
	url = existing_user[0] + 'login'
	payload = {'username': f'{existing_user[1]}', 'password': f'{existing_user[2]}'}
	page = requests.post(url, json=payload)
	assert page.status_code == 200 and page.json()['access_token']


def test_update_pswd(existing_user):
	url = existing_user[0] + 'users'
	payload = {'username': f'{existing_user[1]}', 'old_password': f'{existing_user[2]}', 'password1': 'password', 'password2': 'password'}
	page = requests.put(url, json=payload)
	assert page.status_code == 202 and page.json()['result'] == 'Password successfully updated!'


def test_create_user_with_existing_name(existing_user):	
	url = existing_user[0] + 'users'	
	payload = {'username': f'{existing_user[1]}', 'password1': f'{existing_user[2]}', 'password2': f'{existing_user[2]}'}
	page = requests.post(url, json=payload)
	assert page.status_code == 400 and page.json()["message"] == 'User Already exist'


def test_create_user_with_exceeded_name_lenght(user_generator):
	url = user_generator[0] + 'users'	
	payload = {'username': f'{user_generator[3]}', 'password1': f'{user_generator[2]}', 'password2': f'{user_generator[2]}'}
	page = requests.post(url, json=payload)
	assert page.status_code == 400 and page.json()["message"] == 'Username to long. Max length is 32 chars'


def test_create_user_with_exceeded_pwd_lenght(user_generator):
	url = user_generator[0] + 'users'	
	payload = {'username': f'{user_generator[1]}', 'password1': f'{user_generator[4]}', 'password2': f'{user_generator[4]}'}
	page = requests.post(url, json=payload)
	assert page.status_code == 400 and page.json()["message"] == 'Password to long. Max length is 20 chars'


def test_create_user_with_not_matching_pwds(user_generator):
	url = user_generator[0] + 'users'
	payload = {'username': f'{user_generator[1]}', 'password1': f'{user_generator[2]}', 'password2': 'password'}
	page = requests.post(url, json=payload)
	assert page.status_code == 400 and page.json()["message"] == 'Passwords does not match'


def test_create_user_with_empty_pswd(user_generator):	
	url = user_generator[0] + 'users'	
	payload = {'username': f'{user_generator[0]}', 'password1': None, 'password2': None}
	page = requests.post(url, json=payload)
	assert page.status_code == 500


def test_login_with_wrong_pswd(existing_user):
	url = existing_user[0] + 'login'
	payload = {'username': f'{existing_user[1]}', 'password': 'wrongpwd'}
	page = requests.post(url, json=payload)
	assert page.status_code == 400 and page.json()["message"] == 'invalid password'


def test_update_with_wrong_old_pswd(existing_user):
	url = existing_user[0] + 'users'
	payload = {'username': f'{existing_user[1]}', 'old_password': 'wrongpwd', 'password1': 'password', 'password2': 'password'}
	page = requests.put(url, json=payload)
	assert page.status_code == 400 and page.json()["message"] == 'invalid password'


@pytest.fixture
def user_generator():
	#Creates user data with randomized username and password, 
	#as well as invaliad ones with exceeded length
	url = 'http://bzteltestapi.pythonanywhere.com/'
	letters = string.ascii_letters
	nums = string.digits
	pool = letters + nums
	name_length = random.randint(6,32)
	pwd_length = random.randint(6, 20)
	name = random.sample(pool, name_length)
	pwd = random.sample(pool, pwd_length)
	invalid_name = random.sample(pool, 50)
	invalid_pwd = random.sample(pool, 25)
	invalid_name = ''.join(invalid_name)
	invalid_pwd = ''.join(invalid_pwd)
	name = ''.join(name)
	pwd = ''.join(pwd)
	return url, name, pwd, invalid_name, invalid_pwd


@pytest.fixture
def existing_user():
	#Creates user with fixed name and password for login testing
	url = 'http://bzteltestapi.pythonanywhere.com/'
	name = 'kenny33'
	pwd = '123456'
	payload = {'username': f'{name}', 'password1': f'{pwd}', 'password2': f'{pwd}'}
	page = requests.post(url, json=payload)
	yield (url, name, pwd)
	#Changes the password back, after testing 'updating password' feature
	url2 = url + 'users'
	payload2 = {'username': f'{name}', 'old_password': 'password', 'password1': f'{pwd}', 'password2': f'{pwd}'}
	page2 = requests.put(url2, json=payload2)
