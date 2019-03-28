import math

import jieba.analyse
from snownlp import SnowNLP

from util.mongo_util import get_product_by_pid


def convert_comments_to_sentence(comments):
    """
    将所有评论内容连接成一句话

    :param comments: 列表类型，列表中元素为Comment类型
    :return: 返回字符串类型的结果
    """
    contents = []
    for c in comments:
        contents.append(c.content)
    return ' '.join(contents)


def extract_tags_by_tf_idf(sentence, top=30):
    """
    使用TF-IDF算法提取句子中的关键形容词，默认取三十个

    :param sentence: 待提取的文本，字符串类型
    :param top:提取关键词数量
    :return: 返回列表类型，列表元素为元组类型：(关键词, 权重)
    """
    return jieba.analyse.extract_tags(sentence, topK=top, allowPOS='a', withWeight=True)


def separate_tags(tags):
    """
    将标签列表划分为两个列表：关键词列表和对应的权重列表

    :param tags: 待划分的标签
    :return: 返回关键词列表和对应的权重列表
    """
    attr = []
    value = []
    for tag in tags:
        attr.append(tag[0])
        # 权重都是介于0-1的浮点数，为了便于生成词云，将它们扩大一千倍并转换为整数
        value.append(int(tag[1] * 1000))
    return attr, value


def foo(comments):
    contents = []
    for c in comments:
        nlp = SnowNLP(c.content)
        # 评论获赞数越多，权重越高，取对数来平滑极差
        w = int(math.log(c.votes + 1)) ** 2
        for i in range(w):
            contents.extend(nlp.summary())
    return contents


if __name__ == '__main__':
    product = get_product_by_pid(100000822981)
    contents = foo(product.poor_comments)
    print(contents)
    sen = ' '.join(contents)
    t = extract_tags_by_tf_idf(sen)
    print(t)
