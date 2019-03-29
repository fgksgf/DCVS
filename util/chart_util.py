from pyecharts import WordCloud
from pyecharts.engine import create_default_environment
from util.db_util import get_product_by_pid


def make_word_cloud(title, attr, val):
    wc = WordCloud(width=600, height=400, title=title)
    wc.add('', attr, val, word_size_range=[20, 70], shape='diamond')
    return wc


if __name__ == '__main__':
    product = get_product_by_pid(100000822981)
    # w1, w2 = foo(product.good_comments)
    # wc = make_word_cloud('', w1, w2)
    #
    # # 为渲染创建一个默认配置环境
    # env = create_default_environment("html")
    # env.render_chart_to_file(wc, path='3.html')
