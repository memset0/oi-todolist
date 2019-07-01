import re

from function import *
import user
import config
import problem
import spider

from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

config.init()
from config import config 

user_set = spider.get_user_set()
name_set = spider.get_problem_list()

@app.route('/api/download_user_set', methods=['POST'])
def download_user_set():
    global user_set
    user_set = spider.get_user_set()
    return ''

@app.route('/api/download_problem_name', methods=['POST'])
def download_problem_name():
    global name_set
    name_set = spider.download_problem_list()
    return ''

@app.route('/api/delete_problem', methods=['POST'])
def delete_problem():
    global problem_set
    problem.delete(int(request.form['index']))
    problem_set = problem.load()
    return ''

@app.route('/api/add_problem', methods=['POST'])
def add_problem():
    content = request.form['content']
    for it in content.split('\n'):
        if 'UOJ' in it or 'uoj' in it:
            id = re.findall(r'[0-9]+', it)
            if len(id) == 1:
                problem.append(Problem('UOJ #' + id[0]))
        elif 'LOJ' in it or 'loj' in it or 'LibreOJ' in it or 'libreoj' in it:
            id = re.findall(r'[0-9]+', it)
            if len(id) == 1:
                problem.append(Problem('LOJ #' + id[0]))
        elif 'BZOJ' in it or 'bzoj' in it or 'lydsy' in it:
            id = re.findall(r'[0-9]+', it)
            if len(id) == 1:
                problem.append(Problem('BZOJ #' + id[0]))
    return ''

@app.route('/')
def index():
    global user_set, name_set, problem_set
    problem_set = problem.load()
    data = {
        'users': [ it.name for it in user_set ],
        'lists': [
            {
                'id': problem.id,
                'url': spider.get_url(problem.id),
                'name': name_set[problem.id],
                'index': problem_set.index(problem),
                'status': [
                    problem.id in user.ac_list
                    for user in user_set
                ]
            }
            for problem in problem_set
        ]
    }
    return render_template('index.html', **data)

if __name__ == '__main__':
    app.run(port=config['port'])