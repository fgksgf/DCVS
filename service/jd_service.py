from pyecharts.charts import Page, Bar, Pie
from pyecharts import options as opts
from pyecharts.globals import ThemeType

from util.chart_util import generate_wordcloud, generate_pie_chart, generate_bar_chart
from util.nlp_util import cal_summary_and_weight
from util.db_util import get_product_by_pid


class JDPage:
    def __init__(self, product):
        self.page = Page()
        self.product = product
        self.attr_title_dict = {'product_size': "不同版本购买量", 'product_color': "不同颜色购买量",
                                'after_days': '购买多少天后评论'}

    def generate_bar_charts(self):
        """
        生成不同版本购买量、不同颜色购买量、用户等级和用户客户端的条形图
        """
        if self.product:
            for attr in self.attr_title_dict.keys():
                d = {}
                for c in self.product.get_all_comments():
                    temp = getattr(c, attr)
                    if d.get(temp):
                        d[temp] += 1
                    else:
                        d[temp] = 1

                y_axis = []
                if attr == 'after_days':
                    # 使得x轴名称能按照从少到多的顺序
                    a = ['0-10天', '11-20天', '21-30天', '31-60天', '60天后']
                    for k in a:
                        y_axis.append(d.get(k))
                else:
                    a = []
                    for k in d.keys():
                        a.append(k)
                        y_axis.append(d.get(k))

                self.page.add(generate_bar_chart(title=self.attr_title_dict.get(attr),
                                                 x_axis=a, y_axis=y_axis, y_name="数量"))

    # TODO: refactor to reduce duplicated code
    def generate_pie_charts(self):
        """
        生成饼图
        """
        # 生成各种评价占比的饼图
        k = ["默认好评", "好评", "中评", "差评"]
        v = [self.product.default_good_count, self.product.good_count,
             self.product.general_count, self.product.poor_count]
        self.page.add(generate_pie_chart(title="好评，中评，差评情况", data=[list(z) for z in zip(k, v)]))

        k = ['1星', '2星', '3星', '4星', '5星']
        v = self.product.score_count[1:]
        self.page.add(generate_pie_chart(title="评论打分情况", data=[list(z) for z in zip(k, v)]))

        comments = self.product.get_all_comments()
        # 匿名评论情况饼图
        k = ['匿名', '非匿名']
        v = [0, 0]
        for c in comments:
            if c.is_anonymous:
                v[0] += 1
            else:
                v[1] += 1
        self.page.add(generate_pie_chart(title='匿名评论情况', data=[list(z) for z in zip(k, v)]))

        # plus会员与非会员评论情况
        k = ['PLUS会员', '非会员']
        v = [0, 0]
        for c in comments:
            if c.is_plus:
                v[0] += 1
            else:
                v[1] += 1
        self.page.add(generate_pie_chart(title='会员与非会员评论情况', data=[list(z) for z in zip(k, v)]))

        # 生成不同配置购买量、不同颜色购买量的饼图
        for attr in self.attr_title_dict.keys():
            d = {}
            for c in comments:
                temp = getattr(c, attr)
                if d.get(temp):
                    d[temp] += 1
                else:
                    d[temp] = 1
            v = []
            for key in d.keys():
                v.append(d.get(key))
            self.page.add(generate_pie_chart(title=self.attr_title_dict.get(attr),
                                             data=[list(z) for z in zip(d.keys(), v)]))

    def generate_word_cloud_charts(self):
        """
        生成词云图，并添加到page中
        """
        # 生成热评词云图
        words = []
        for t in self.product.hot_comment_tags:
            item = (t.get('name'), int(t.get('count')))
            words.append(item)
        self.page.add(generate_wordcloud(title="热评词云图", words=words))

        # 分别生成好评，中评，差评词云图
        d = [('好评词云图', 'good_comments'), ('中评词云图', 'general_comments'), ('差评词云图', 'poor_comments')]
        for i in range(3):
            words = cal_summary_and_weight(getattr(self.product, d[i][1]))
            self.page.add(generate_wordcloud(title=d[i][0], words=words))
