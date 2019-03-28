from pyecharts import WordCloud
from pyecharts.engine import create_default_environment
from util.nlp_util import *
from util.mongo_util import get_product_by_pid


def make_word_cloud(title, attr, val):
    wc = WordCloud(width=600, height=300)
    wc.add(title, attr, val, word_size_range=[20, 80], shape='diamond')
    return wc


if __name__ == '__main__':
    product = get_product_by_pid(100000822981)
    w1, w2 = foo(product.poor_comments)
    wc = make_word_cloud('',w1,w2)
    print(w1)
    print(w2)
    # 为渲染创建一个默认配置环境
    # file_type: 'html', 'svg', 'png', 'jpeg', 'gif' or 'pdf'
    env = create_default_environment("html")
    env.render_chart_to_file(wc, path='1.html')
