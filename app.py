import json
import random

# from pyecharts import Scatter3D
from flask import Flask, render_template

from util.redis_util import insert_into_redis

app = Flask(__name__)
REMOTE_HOST = "https://pyecharts.github.io/assets/js"
PREFIX = 'https://item.jd.com/'


@app.route('/')
def index():
    return render_template('index.html')


# 将获取的pid与网址前缀连接，插入到任务队列
@app.route('/crawl/jd/<string:pid>', methods=['GET'])
def jd_crawler(pid):
    insert_into_redis('jd:items_urls', PREFIX + pid)
    result = {'result': 'ok'}
    return json.dumps(result)


@app.route('/analyze/jd/<string:pid>', methods=['GET'])
def jd_analyze(pid):
    pass

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
