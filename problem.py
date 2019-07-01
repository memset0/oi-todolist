import yaml
from function import Problem

def load():
	try:
		file = open('problem.yml', 'r+', encoding='utf8')
		text = file.read()
		data = yaml.load(text)
		result = [ Problem(**it) for it in data ]
		return result
	except:
		return []

def dump(data):
	result = []
	for it in data:
		result.append(it.to_dict())
	text = yaml.dump(result)
	file = open('problem.yml', 'w+', encoding='utf8')
	file.write(text)
	
def append(val):
	data = load()
	data.append(val)
	dump(data)

def delete(index):
	data = load()
	if index >= 0 and index < len(data):
		del data[index]
	dump(data)

def move_up(id):
	data = load()
	if id <= 0:
		return
	tmp = data[id - 1]
	data[id - 1] = data[id]
	data[id] = tmp
	dump(data)

def move_down(id):
	data = load()
	if id >= len(data):
		return
	tmp = data[id + 1]
	data[id + 1] = data[id]
	data[id] = tmp
	dump(data)

if __name__ == '__main__':
	append(Problem(id='LG1000'))
	for it in load():
		print(it);