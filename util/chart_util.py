from pyecharts.charts import WordCloud, Bar, Pie
from pyecharts import options as opts
from pyecharts.globals import SymbolType, ThemeType


def generate_bar_chart(title, x_axis, y_axis, y_name) -> Bar:
    c = (
        Bar({"theme": ThemeType.MACARONS})
        .add_xaxis(x_axis)
        .add_yaxis(y_name, y_axis)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(title_opts=opts.TitleOpts(title=title))
    )
    return c


def generate_pie_chart(title, data) -> Pie:
    c = (
        Pie()
        .add("", data)
        .set_global_opts(title_opts=opts.TitleOpts(title=title))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}"))
    )
    if len(data) > 5:
        c.set_global_opts(legend_opts=opts.LegendOpts(item_gap=5, item_width=20, item_height=10))
    return c


def generate_wordcloud(title, words, shape=SymbolType.DIAMOND) -> WordCloud:
    c = (
        WordCloud()
        .add("", words, word_size_range=[20, 70], shape=shape)
        .set_global_opts(title_opts=opts.TitleOpts(title=title))
    )
    return c
