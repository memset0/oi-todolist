import user
import config
import problem
from function import *

config.init()
from config import config

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
	e_info('downloading problem list of bzoj')
	req = request_get('http://uoj.ac/problems')
	req.encoding = 'utf8'
	max_page = split_uoj_max_page(req.text)
	result = split_uoj_problem_list(req.text)
	for page in range(2, max_page + 1):
		req = request_get('http://uoj.ac/problems?page=%d' % page)
		req.encoding = 'utf8'
		result.update(split_uoj_problem_list(req.text))
	e_info('downloaded problem list of uoj, there are %d pages and %d problems' % (max_page, len(result)))
	return result

def get_uoj_ac_list(user):
	url = 'http://uoj.ac/user/profile/{id}'.format(id=user.id)
	req = request_get(url, cookies=user.cookie)
	base_result = re.findall(r'<a href="/problem/[0-9]*" style="display:inline-block; width:4em;">[0-9]*</a>', req.text)
	result = { 'UOJ #' + it.split('>')[1].split('<')[0] for it in base_result }
	return result

########## UOJ - end ##########

########## LOJ - begin ##########

def split_loj_problem_list(text):
	id_list = [
		it[7:-9]
		for it in re.findall(r'<td><b>[0-9]+</b></td>', text)
	]
	name_list = [
		it.split('>')[-1][:-1]
		for it in re.findall(r'<a style="vertical-align: middle; " href="/problem/[0-9]*">[\s\S]*?\n', text)
	]
	return {
		'LOJ #' + id_list[i]: name_list[i]
		for i in range(len(id_list))
	}

def split_loj_max_page(text):
	result = 0
	base_result = re.findall(r'<a class="item" href="/problems\?page=[0-9]*">[0-9]*</a>', text)
	for it in base_result:
		page = int(it.split('<')[-2].split('>')[-1])
		if page > result:
			result = page
	return result

def get_loj_problem_list():
	e_info('downloading problem list of loj')
	req = request_get('https://loj.ac/problems')
	max_page = split_loj_max_page(req.text)
	result = split_loj_problem_list(req.text)
	for page in range(2, max_page + 1):
		req = request_get('https://loj.ac/problems?page=%d' % page)
		result.update(split_loj_problem_list(req.text))
	e_info('downloaded problem list of loj, there are %d pages and %d problems' % (max_page, len(result)))
	return result

def get_loj_ac_list(user):
	url = 'https://loj.ac/find_user?nickname={id}'.format(id=user.id)
	req = request_get(url, cookies=user.cookie)
	base_result = re.findall(r'<a href="/problem/[0-9]*">[0-9]*</a>', req.text)
	result = { 'LOJ #' + it.split('>')[1].split('<')[0] for it in base_result }
	return result

########## LOJ - end ##########

########## BZOJ - begin ##########

def split_bzoj_problem_list(text):
	return {
		'BZOJ #' + it[24:28]: it[30:-4]
		for it in re.findall(r"<a href='problem.php\?id=[0-9]*'>[\S\ss]*?</a>", text)
	}

def split_bzoj_max_page(text):
	result = 0
	base_result = re.findall(r"<a href='problemset.php\?page=[0-9]*'>[0-9]*</a>", text)
	for it in base_result:
		page = int(it.split('<')[-2].split('>')[-1])
		if page > result:
			result = page
	return result

def get_bzoj_problem_list():
	e_info('downloading problem list of bzoj')
	req = request_get('https://lydsy.com/JudgeOnline/problemset.php', cookies=config['cookies']['bzoj'])
	req.encoding = 'utf8'
	max_page = split_bzoj_max_page(req.text)
	result = split_bzoj_problem_list(req.text)
	for page in range(2, max_page + 1):
		req = request_get('https://lydsy.com/JudgeOnline/problemset.php?page=%d' % page, cookies=config['cookies']['bzoj'])
		req.encoding = 'utf8'
		result.update(split_bzoj_problem_list(req.text))
	e_info('downloaded problem list of bzoj, there are %d pages and %d problems' % (max_page, len(result)))
	return result

def get_bzoj_ac_list(user):
	url = 'https://lydsy.com/JudgeOnline/userinfo.php?user={id}'.format(id=user.id)
	req = request_get(url, cookies=user.cookie)
	base_result = re.findall(r'p([0-9]+)', req.text)
	result = { 'BZOJ #' + it[2:-1] for it in base_result }
	return result

########## BZOJ - end ##########

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
		elif user.site == 'loj':
			user.ac_list = get_loj_ac_list(user)
		return user
	
def download_problem_list():
	e_info('downloading problem list, it may take a bit time')
	result = dict()
	result.update(get_uoj_problem_list())
	result.update(get_loj_problem_list())
	result.update(get_bzoj_problem_list())
	e_info('downloaded problem list')
	return result

def get_problem_list():
	if os.path.isfile('problem_list.yml'):
		result = yaml.load(open('problem_list.yml', 'r+', encoding='utf8').read())
		return result
	else:
		e_warning('problem list cache has not found, will be downloaded')
		result = download_problem_list()
		open('problem_list.yml', 'w+', encoding='utf8').write(yaml.dump(result))
		return result

def get_url(name):
	url_dict = {
		'UOJ': 'https://uoj.ac/problem/%s',
		'LOJ': 'https://loj.ac/problem/%s',
		'BZOJ': 'https://lydsy.com/JudgeOnline/problem.php?id=%s'
	}
	key, val = name.split(' #')
	return url_dict[key] % val

def download_user_set():
	e_info('downloading user set')
	data = dict()
	user_set = user.load()
	data['basic'] = user_set
	for i in range(0, len(user_set)):
		user_set[i] = set_ac_list(user_set[i])
	data['crawl'] = user_set
	open('user.cache.yml', 'w+').write(yaml.dump(data))
	e_info('downloaded user set')
	return user_set

def get_user_set():
	data = yaml.load(open('user.cache.yml', 'r+').read())
	if type(data) == type(None) or not 'basic' in data.keys() or data['basic'] != user.load():
		return download_user_set()
	return data['crawl']

if __name__ == '__main__':
	# print(set_ac_list(User('memset0', [Account('uoj', 'only30iq')])).ac_list)
	# print(get()[0].ac_list)
	for key, val in download_problem_list().items():
		print(key, val)