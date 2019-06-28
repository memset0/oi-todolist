import yaml
from function import User, Account

def load():
	text = open('user.yml', 'r+', encoding='utf8')
	data = yaml.load(text)
	result = [
		User(**it) if type(it) == dict else it
		for it in data
	]
	return result