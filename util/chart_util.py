from pyecharts import WordCloud
from pyecharts.engine import create_default_environment
from util.jieba_util import *
from util.mongo_util import get_product_by_pid


def make_word_cloud(title, attr, val):
    wc = WordCloud(width=600, height=300)
    wc.add(title, attr, val, word_size_range=[20, 80], shape='diamond')
    return wc


if __name__ == '__main__':
    p = get_product_by_pid(22042025230)
    sentence = convert_comments_to_sentence(p.poor_comments)
    t1 = extract_tags_by_tf_idf(sentence)

    att, val = separate_tags(t1)
    wc1 = make_word_cloud(att, val)

    # 为渲染创建一个默认配置环境
    # file_type: 'html', 'svg', 'png', 'jpeg', 'gif' or 'pdf'
    env = create_default_environment("html")
    env.render_chart_to_file(wc1, path='1.html')
