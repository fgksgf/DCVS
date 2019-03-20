class Comment:
    def __init__(self, item):
        # 评论内容, 删除评价中的无关字符'hellip'与首尾空格
        self.content = str(item.get('content')).strip().replace('hellip', '')
        # 评分：1为差评，2-3为中评，4-5为好评
        self.score = int(item.get('score'))
        # 是否使用移动端进行评论
        self.is_mobile = (item.get('isMobile') == 'true')
        # 购买后多少天评论
        self.after_days = int(item.get('days'))
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
