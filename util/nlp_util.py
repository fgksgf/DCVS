import math

from snownlp import SnowNLP
from util.db_util import get_product_by_pid


# TODO: 评论内容去停用词、标点符号
def cal_summary_and_weight(comments):
    """
    计算评论内容的摘要及其对应权重

    :param comments: 需要分析的评论列表
    :return: 返回列表，列表元素为元组，元组中包含摘要和其对应的权重
    """
    d = {}
    ret = []
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
        ret.append((k, d.get(k)))
    return ret


if __name__ == '__main__':
    product = get_product_by_pid(100000822981)
