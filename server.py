from function import *
import user
import config
import problem
import spider

from flask import Flask
from flask import render_template
app = Flask(__name__)

user_set = user.load()
problem_set = problem.load()
name_set = spider.get_problem_list()
url_set = spider.get_url_list(name_set)

@app.route('/')
def index():
    global user_set, problem_set, name_set, url_set
    user_set = spider.get(user_set)
    data = {
        'users': [ it.name for it in user_set ],
        'lists': [
            {
                'id': problem.id,
                'url': url_set[problem.id],
                'name': name_set[problem.id],
                'status': [
                    (problem.id in user.ac_list)
                    for user in user_set
                ]
            }
            for problem in problem_set
        ]
    }
    return render_template('index.html', **data)

if __name__ == '__main__':
    app.run(port=23333)