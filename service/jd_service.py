from pyecharts import Page, Bar, Pie

from util.chart_util import make_word_cloud
from util.jieba_util import convert_comments_to_sentence, extract_tags_by_tf_idf, separate_tags
from util.mongo_util import get_product_by_pid


class JDPage:
    def __init__(self, product):
        self.page = Page()
        self.product = product

    @staticmethod
    def make_word_clouds(comments, title):
        sentence = convert_comments_to_sentence(comments)
        tags = extract_tags_by_tf_idf(sentence)
        att, val = separate_tags(tags)
        return make_word_cloud(title, att, val)

    def generate_bar_or_pie_charts(self, bar=True):
        """
        生成不同配置购买量、不同颜色购买量、用户等级和用户客户端的条形图或饼图

        :param bar: bar为True时，生成条形图；为False生成饼图
        """
        attr_title_dict = {'product_size': "不同配置购买量", 'product_color': "不同颜色购买量",
                           'level': "用户等级", 'client': "用户客户端"}
        for attr in attr_title_dict.keys():
            d = {}
            for c in self.product.comments:
                temp = getattr(c, attr)
                if d.get(temp):
                    d[temp] += 1
                else:
                    d[temp] = 1
            a = []
            v = []
            for k in d.keys():
                if k == '':
                    a.append('其他')
                else:
                    a.append(k)
                v.append(d.get(k))
            if bar:
                chart = Bar(attr_title_dict.get(attr))
                chart.add("", a, v, xaxis_interval=0)
            else:
                chart = Pie(attr_title_dict.get(attr))
                chart.add("", a, v, is_label_show=True)
            self.page.add(chart)

    def generate_pie_charts(self):
        """
        生成饼图
        """
        # 生成各种评价占比的饼图
        a = ["好评", "中评", "差评"]
        v = [self.product.good_count, self.product.general_count, self.product.poor_count]
        pie = Pie("好评，中评，差评")
        pie.add("", a, v, is_label_show=True)
        self.page.add(pie)

        # 生成不同配置购买量、不同颜色购买量、用户等级和用户客户端的饼图
        self.generate_bar_or_pie_charts(bar=False)

    def generate_word_cloud_charts(self):
        """
        生成词云图
        """
        # 热评词云
        attr = []
        val = []
        for t in self.product.hot_comment_tags:
            attr.append(t.get('name'))
            val.append(int(t.get('count')))
        self.page.add(make_word_cloud("热评标签", attr, val))

        # 好评，中评，差评词云
        self.page.add(self.make_word_clouds(self.product.good_comments, "好评"))
        self.page.add(self.make_word_clouds(self.product.general_comments, "中评"))
        self.page.add(self.make_word_clouds(self.product.poor_comments, "差评"))


if __name__ == '__main__':
    product = get_product_by_pid(22042025230)
    # product = get_product_by_pid(100000323510)
    p = JDPage(product)
    p.generate_word_cloud_charts()
    p.page.render()
