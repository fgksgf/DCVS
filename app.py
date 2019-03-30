import json
import time

from flask import Flask, render_template, session, send_file, request

from config import *
from service.jd_service import JDPage
from util.code_util import *
from util.db_util import get_product_by_pid, redis_client

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/crawl/jd/', methods=['POST'])
def jd_crawler():
    pid = request.values.get('pid', 0)
    # 验证码忽略大小写
    code = str(request.values.get('captcha', 0)).lower()

    # 判断验证码是否正确
    if code != session.get('captcha'):
        result = {'result': 'wrong_code'}
        return json.dumps(result)

    # 查询数据库中是否已存在该商品
    product = get_product_by_pid(pid)
    if product is None:
        # 若无，将获取的pid与网址前后缀连接，插入到任务队列
        redis_client.lpush('jd:items_urls', PREFIX + pid + POSTFIX)
        # 每两秒查询一次，爬取任务是否完成
        while int(redis_client.get(pid)) > 0:
            time.sleep(2)
    elif len(product.comments) < WORK_LOAD:
        # 说明当前爬取任务正在进行中
        # 每两秒查询一次，爬取任务是否完成
        while int(redis_client.get(pid)) > 0:
            time.sleep(2)

    result = {'result': 'ok', 'pid': pid}
    return json.dumps(result)


@app.route('/analyze/jd/<string:pid>/')
def jd_dashboard(pid):
    product = get_product_by_pid(pid)
    if product is None:
        return '404!!!'
    return render_template('dashboard.html', product=product)


@app.route('/analyze/jd/<string:chart>/<string:pid>', methods=['GET'])
def jd_charts(chart, pid):
    product = get_product_by_pid(pid)
    if product is None:
        return '404!!!'
    jd_page = JDPage(product)
    chart_type = 1
    if chart == 'bar':
        jd_page.generate_stacked_bar_charts()
    elif chart == 'pie':
        jd_page.generate_pie_charts()
        chart_type = 2
    elif chart == 'wordcloud':
        jd_page.generate_word_cloud_charts()
        chart_type = 3
    else:
        return '404!'

    return render_template(
        "dashboard.html",
        pid=pid,
        chart_type=chart_type,
        myechart=jd_page.page.render_embed(),
        host=REMOTE_HOST,
        script_list=jd_page.page.get_js_dependencies()
    )


@app.route('/captcha')
def get_captcha():
    filename = pick_a_random_captcha()
    code = filename[:4]
    fp = './static/img/captcha/' + code + '.png'
    session['captcha'] = code
    return send_file(fp, mimetype='image/png')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
