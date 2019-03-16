import json
import random

# from pyecharts import Scatter3D
import time

from flask import Flask, render_template

from util.mongo_util import find_one_by_pid
from util.redis_util import redis_client

app = Flask(__name__)
REMOTE_HOST = "https://pyecharts.github.io/assets/js"
PREFIX = 'https://item.jd.com/'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/crawl/jd/<string:pid>', methods=['GET'])
def jd_crawler(pid):
    # eg. pid: '100000822969.html'
    # 将获取的pid与网址前缀连接，插入到任务队列
    redis_client.lpush('jd:items_urls', PREFIX + pid)
    # eg. pid: '100000822969'
    pid = pid[:-5]

    # 每两秒查询一次，爬取任务是否完成
    while int(redis_client.get(pid)) > 0:
        time.sleep(2)

    result = {'result': 'ok', 'pid': pid}
    return json.dumps(result)


@app.route('/analyze/jd/<string:pid>')
def jd_analyze(pid):
    product = find_one_by_pid(pid)


#
# @app.route('/chart')
# def hello():
#     s3d = scatter3d()
#     return render_template(
#         "chart.html",
#         myechart=s3d.render_embed(),
#         host=REMOTE_HOST,
#         script_list=s3d.get_js_dependencies(),
#     )
#
#
# def scatter3d():
#     data = [generate_3d_random_point() for _ in range(80)]
#     range_color = [
#         "#313695",
#         "#4575b4",
#         "#74add1",
#         "#abd9e9",
#         "#e0f3f8",
#         "#fee090",
#         "#fdae61",
#         "#f46d43",
#         "#d73027",
#         "#a50026",
#     ]
#     scatter3D = Scatter3D("3D scattering plot demo", width=1200, height=600)
#     scatter3D.add("", data, is_visualmap=True, visual_range_color=range_color)
#     return scatter3D
#
#
# def generate_3d_random_point():
#     return [
#         random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)
#     ]


if __name__ == '__main__':
    app.run()
