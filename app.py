import json

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/crawl/jd/<string:url>', methods=['GET'])
# def jd_crawler(url):
#     print(url)
#     result = {'result': 'ok'}
#     return json.dumps(result)


@app.route('/crawl/jd/<string:pid>', methods=['GET'])
def jd_crawler(pid):
    print(pid)
    result = {'result': 'ok'}
    return json.dumps(result)


if __name__ == '__main__':
    app.run()
