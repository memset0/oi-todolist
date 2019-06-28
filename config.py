import yaml

def init():
	global data
	text = open('config.yml', 'r+', encoding='utf8')
	data = yaml.load(text)

init()