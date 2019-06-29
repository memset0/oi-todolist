import user
import config
import problem
from function import *

import os
import re
import yaml
import requests

########## UOJ - begin ##########

def split_uoj_problem_list(text):
	return {
		'UOJ #' + it.split('>#')[1].split('<')[0]:
		it.split('<')[-3].split('>')[-1]
		for it in re.findall(r'<td>#[0-9]*</td><td class="text-left"><a href="/problem/[0-9]*">[\s\S]*?</a></td>', text)
	}

def split_uoj_max_page(text):
	base_result = re.findall(r'/problems\?page=', text)
	result = len(base_result) // 2
	return result

def get_uoj_problem_list():
	req = request_get('http://uoj.ac/problems')
	req.encoding = 'utf8'
	max_page = split_uoj_max_page(req.text)
	result = split_uoj_problem_list(req.text)
	for page in range(2, max_page + 1):
		req = request_get('http://uoj.ac/problems?page=%d' % page)
		req.encoding = 'utf8'
		result.update(split_uoj_problem_list(req.text))
	return result

def get_uoj_ac_list(user):
	url = 'http://uoj.ac/user/profile/{id}'.format(id=user.id)
	req = request_get(url, cookies=user.cookie)
	text = req.text
	base_result = re.findall(r'<a href="/problem/[0-9]*" style="display:inline-block; width:4em;">[0-9]*</a>', text)
	result = { 'UOJ #' + it.split('>')[1].split('<')[0] for it in base_result }
	return result

########## UOJ - end ##########

def set_ac_list(user):
	if type(user) == User:
		user.ac_list = set()
		for i in range(0, len(user.account)):
			user.account[i] = set_ac_list(user.account[i])
			user.ac_list = user.ac_list | user.account[i].ac_list
		return user
	elif type(user) == Account:
		if user.site == 'uoj':
			user.ac_list = get_uoj_ac_list(user)
		return user
	
def download_problem_list():
	result = dict()
	result.update(get_uoj_problem_list())
	return result

def get_problem_list():
	if os.path.isfile('problem_list.yml'):
		result = yaml.load(open('problem_list.yml', 'r+', encoding='utf8').read())
		return result
	else:
		result = download_problem_list()
		open('problem_list.yml', 'w+', encoding='utf8').write(yaml.dump(result))
		return result

def get_url(name):
	url_dict = {
		'UOJ': 'https://uoj.ac/problem/%s',
		'LOJ': 'https://loj.ac/problem/%s'
	}
	return url_dict[name.split(' #')[0]] % name.split(' #')[1]

def get(user_set):
	for i in range(0, len(user_set)):
		user_set[i] = set_ac_list(user_set[i])
	return user_set

if __name__ == '__main__':
	# print(set_ac_list(User('memset0', [Account('uoj', 'only30iq')])).ac_list)
	# print(get()[0].ac_list)
	for key, val in get_problem_list().items():
		print(key, val)