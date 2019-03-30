from pyecharts import Page, Bar, Pie

from util.chart_util import make_word_cloud
from util.nlp_util import get_summary_and_weight
from util.db_util import get_product_by_pid


class JDPage:

    def __init__(self, product):
        self.page = Page()
        self.product = product
        self.attr_title_dict = {'product_size': "不同配置购买量", 'product_color': "不同颜色购买量",
                                'level': "用户等级", 'client': "用户客户端", 'after_days': '购买多少天后评论'}

    def generate_stacked_bar_charts(self):
        """
        生成不同配置购买量、不同颜色购买量、用户等级和用户客户端的层叠条形图
        """
        titles = ['好评', '中评', '差评']
        for attr in self.attr_title_dict.keys():
            d = {}
            for c in self.product.get_all_comments():
                temp = getattr(c, attr)
                if c.score > 3:
                    index = 0
                elif c.score > 1:
                    index = 1
                else:
                    index = 2

                if d.get(temp):
                    d[temp][index] += 1
                else:
                    d[temp] = [0, 0, 0]
                    d[temp][index] = 1

            v = [[], [], []]
            if attr == 'after_days':
                # 使得x轴名称能按照从少到多的顺序
                a = ['0-10天', '11-20天', '21-30天', '31-60天', '60天后']
                for k in a:
                    for i in range(3):
                        v[i].append(d.get(k)[i])
            else:
                a = []
                for k in d.keys():
                    if k == '':
                        a.append('网页')
                    else:
                        a.append(k)
                    for i in range(3):
                        v[i].append(d.get(k)[i])

            chart = Bar(self.attr_title_dict.get(attr))
            for i in range(3):
                chart.add(titles[i], a, v[i], xaxis_interval=0, is_stack=True)
            self.page.add(chart)

    def generate_pie_charts(self):
        """
        生成饼图
        """
        # 生成各种评价占比的饼图
        a = ["默认好评", "好评", "中评", "差评"]
        v = [self.product.default_good_count, self.product.good_count - self.product.default_good_count,
             self.product.general_count, self.product.poor_count]
        pie = Pie("好评，中评，差评")
        pie.add("", a, v, is_label_show=True)
        self.page.add(pie)

        comments = self.product.get_all_comments()
        # 匿名评论情况饼图
        v = [0, 0]
        for c in comments:
            if c.isAnonymous:
                v[0] += 1
            else:
                v[1] += 1

        chart = Pie('匿名评论情况')
        chart.add('', ['匿名', '非匿名'], v, xaxis_interval=0)
        self.page.add(chart)

        # 生成不同配置购买量、不同颜色购买量、用户等级和用户客户端的饼图
        for attr in self.attr_title_dict.keys():
            d = {}
            for c in comments:
                temp = getattr(c, attr)
                if d.get(temp):
                    d[temp] += 1
                else:
                    d[temp] = 1
            a = []
            v = []
            for k in d.keys():
                if k == '':
                    a.append('网页')
                else:
                    a.append(k)
                v.append(d.get(k))

            if attr == 'level':
                # 解决图例过长遮挡标题的bug
                chart = Pie('')
            else:
                chart = Pie(self.attr_title_dict.get(attr))

            chart.add("", a, v, is_label_show=True)
            self.page.add(chart)

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
        hot_tags_wc = make_word_cloud("热评词云", attr, val)
        self.page.add(hot_tags_wc)

        # 好评，中评，差评词云
        d = [('好评词云', 'good_comments'), ('中评词云', 'general_comments'), ('差评词云', 'poor_comments')]
        for i in range(3):
            a, v = get_summary_and_weight(getattr(self.product, d[i][1]))
            wc = make_word_cloud(d[i][0], a, v)
            self.page.add(wc)


if __name__ == '__main__':
    prod = get_product_by_pid(100000822981)
    p = JDPage(prod)
    # p.foo()
    # p.generate_stacked_bar_charts()
    # p.generate_word_cloud_charts()
    p.generate_pie_charts()
    # p.generate_bar_chart_about()
    p.page.render()
