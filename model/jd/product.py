from model.jd.comment import Comment


class Product:
    def __init__(self, item):
        # 商品id
        self.pid = item.get('pid')
        # 商品描述
        self.desc = item.get('desc')
        # 商品价格
        self.price = item.get('price')
        # 商品图片URL
        self.img = item.get('img_url')
        # 商品可选属性名称列表，例如颜色、尺码等
        self.attributes = item.get('attributes')
        # 商品属性选项列表，列表元素也为列表类型
        self.choices = item.get('choices')

        # 好评数
        self.good_count = int(item.get('comment_summary').get('goodCount'))
        # 中评数
        self.general_count = int(item.get('comment_summary').get('generalCount'))
        # 差评数
        self.poor_count = int(item.get('comment_summary').get('poorCount'))
        # 默认好评数
        self.default_good_count = int(item.get('comment_summary').get('defaultGoodCount'))

        # 热评标签
        self.hot_comment_tags = item.get('hot_comments')
        # 评论
        self.good_comments = []
        self.general_comments = []
        self.poor_comments = []

        # 将评论根据评分分类
        for c in item.get('comments'):
            comment = Comment(c)
            if comment.score >= 4:
                self.good_comments.append(comment)
            elif comment.score >= 2:
                self.general_comments.append(comment)
            else:
                self.poor_comments.append(comment)

    def get_all_comments(self):
        return self.good_comments + self.general_comments + self.poor_comments
