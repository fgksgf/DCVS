import math

from snownlp import SnowNLP
from util.mongo_util import get_product_by_pid


def get_summary_and_weight(comments):
    """
    获得评论内容的摘要和权重

    :param comments: 需要分析的评论列表
    :return: 返回摘要列表和对应的权重列表
    """
    d = {}
    att = []
    val = []
    for c in comments:
        nlp = SnowNLP(c.content)
        # 评论获赞数越多，权重越高，取对数来平滑极差
        w = int(math.log(c.votes + 1) + 1) ** 2
        for kw in nlp.summary():
            if d.get(kw):
                d[kw] += w
            else:
                d[kw] = w
    for k in d.keys():
        att.append(k)
        val.append(d.get(k))
    return att, val


if __name__ == '__main__':
    product = get_product_by_pid(100000822981)
