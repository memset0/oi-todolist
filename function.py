import yaml, requests

class Problem:
	def __init__(self, id, tag=[], note=''):
		self.id = id
		self.tag = tag
		self.note = note
	def __str__(self):
		return '[{id}]'.format(
			id = self.id,
			tag = self.tag,
			note = self.note
		)
	def to_dict(self):
		return {
			'id': self.id,
			'tag': self.tag,
			'note': self.note
		}

class Account:
	def __init__(self, site, id, name='', note='', cookie=None, ac_list=set()):
		self.site = site
		self.id = id
		self.name = name
		self.note = note
		self.cookie = cookie
		self.ac_list = ac_list
	def __str__(self):
		return '{Account: [%s]%s}' % (self.site, self.id)

class User:
	def __init__(self, name, account, note='', ac_list=set()):
		self.name = name
		self.account = [
			Account(**it) if type(it) == dict else it
			for it in account
		]
		self.note = note
		self.ac_list = ac_list
	def __str__(self):
		result = '\{\'name\': {name}, \'account\': ['.format(name=self.name)
		for i in range(0, len(account)):
			if i > 0:
				result += ', '
			result += str(account)
		result += ']}'
		return result

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