# app.py config
REMOTE_HOST = "https://pyecharts.github.io/assets/js"
PREFIX = 'https://item.jd.com/'
POSTFIX = '.html'
WORK_LOAD = 150

# redis config
REDIS_HOST = '39.96.94.81'
REDIS_PORT = 6379
REDIS_PASSWORD = 'iE23fP$d9yTQCgmc'

# mongodb config
MONGODB_URL = 'mongodb://localhost:27017/'

# CAPTCHA config
# 字母，为防止混淆，去除o，O，i，I，i，L, q,b,g,u,v,U,V
LETTERS = "acdefhjkmnpstwxyABCDEFGHJKLMNPQRSTWXY"
# 数字，为防止混淆，去除0，1, 6, 9
NUMBERS = "234578"
# 字体路径
FONT_PATH = "./Verdana.ttf"
# 允许的字符集合
CHARS = LETTERS + NUMBERS


class Config:
    # flask config
    SECRET_KEY = 'you-will-never-guess'
