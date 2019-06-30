import yaml, requests

class Problem:
	def __init__(self, id, tag=[], note=''):
		self.id = id
		self.tag = tag
	def __str__(self):
		return '[{id}]'.format(
			id = self.id,
			tag = self.tag,
		)
	def to_dict(self):
		result = { 'id': self.id }
		if self.tag != []:
			result['tag'] = self.tag
		return result

class Account:
	def __init__(self, site, id, name='', cookie=None, ac_list=set()):
		self.site = site
		self.id = id
		self.name = name
		self.cookie = cookie
		self.ac_list = ac_list
	def __str__(self):
		return '{Account: [%s]%s}' % (self.site, self.id)
	# def to_dict(self):
	# 	result = {
	# 		'site': self.site,
	# 		'id': self.id
	# 	}
	# 	if self.name != '':
	# 		result['name'] = self.name
	# 	if self.cookie != None:
	# 		result['cookie'] = self.cookie
	# 	if self.ac_list != set():
	# 		result['ac_list'] = self.ac_list
	# 	return result

class User:
	def __init__(self, name, account, ac_list=set()):
		self.name = name
		self.account = [
			Account(**it) if type(it) == dict else it
			for it in account
		]
		self.ac_list = ac_list
	def __str__(self):
		result = '\{\'name\': {name}, \'account\': ['.format(name=self.name)
		for i in range(0, len(account)):
			if i > 0:
				result += ', '
			result += str(account)
		result += ']}'
		return result
	# def to_dict(self):
	# 	result = {
	# 		'name': self.name,
	# 		'account': [ it.to_dict() for it in self.account ]
	# 	}
	# 	if self.ac_list != set():
	# 		result['ac_list'] = self.ac_list
	# 	return result

def request_get(url, cookies=None, headers=dict()):
	headers['user-agent'] = 'Sooke AK IOI'
	while True:
		try:
			return requests.get(url, cookies=cookies, headers=headers)
		except:
			continue

def request_post(url, data, cookies=None, headers=dict()):
	headers['user-agent'] = 'Sooke AK IOI'
	while True:
		try:
			return requests.post(url, data=data, cookies=cookies, headers=headers)
		except:
			continue

def e_info(text):
	print('\033[94m[info] ' + text + '\033[0m')

def e_debug(text):
	print('\033[95m[debug] ' + text + '\033[0m')

def e_warning(text):
	print('\033[93m[warning] ' + text + '\033[0m')

def e_error(text):
	print('\033[91m[error] ' + text + '\033[0m')

if __name__ == '__main__':
	e_info('this is a info')
	e_debug('this is a debug')
	e_warning('this is a warning')
	e_error('this is a error')