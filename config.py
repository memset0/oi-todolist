import yaml

def init():
	global config
	text = open('config.yml', 'r+', encoding='utf8')
	config = yaml.load(text)