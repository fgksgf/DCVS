def convert_day_to_str(day):
    """
    将天数转换为对应的文字

    :param day: 天数
    :return: 对应的字符串
    """
    day = int(day)
    lst = ['0-10天', '11-20天', '21-30天', '31-60天', '60天后']
    if day > 60:
        index = -1
    elif day >= 31:
        index = -2
    elif day >= 21:
        index = -3
    elif day >= 11:
        index = -4
    else:
        index = -5
    return lst[index]


class Comment:
    def __init__(self, item):
        # 评论内容, 删除评价中的无关字符'hellip'与首尾空格
        self.content = str(item.get('content')).strip().replace('hellip', '')
        # 评分：1为差评，2-3为中评，4-5为好评
        self.score = int(item.get('score'))
        # 购买后多少天评论
        self.after_days = convert_day_to_str(item.get('days'))
        # 商品颜色
        self.product_color = str(item.get('productColor'))
        # 商品配置
        self.product_size = str(item.get('productSize'))
        # 点赞数
        self.votes = int(item.get('usefulVoteCount'))
        # 客户端
        self.client = str(item.get('userClientShow')).replace('来自京东', '')
        # 用户等级
        self.level = str(item.get('userLevelName'))
        # 是否匿名
        self.isAnonymous = int(item.get('anonymousFlag')) == 1
