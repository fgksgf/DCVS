import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter

# 字母，为防止混淆，去除o，O，i，I，i，L, q,b,g,u,v,U,V
LETTERS = "acdefhjkmnpstwxyABCDEFGHJKLMNPQRSTWXY"
# 数字，为防止混淆，去除0，1, 6, 9
NUMBERS = "234578"
# 字体路径
FONT_PATH = "./Verdana.ttf"
# 允许的字符集合
CHARS = LETTERS + NUMBERS


def generate_verify_image(size=(130, 40), fg_color='blue', font_size=26, length=4, n_line=(3, 5)):
    """
    生成验证码图片

    :param size: 图片的大小，格式（宽，高），默认为(120, 30)
    :param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
    :param font_size: 验证码字体大小
    :param length: 验证码字符个数
    :param n_line: 干扰线的条数范围，格式元组，默认为(1, 2)
    :return: 返回元组，[0]: 验证码图片, [1]: 验证码图片中的字符串
    """
    width, height = size  # 宽， 高
    img = Image.new("RGB", size, (255, 255, 255))  # 创建图形
    draw = ImageDraw.Draw(img)  # 创建画笔

    # 生成给定长度的字符串，返回列表格式
    code = random.sample(CHARS, length)

    # 绘制干扰线
    line_num = random.randint(*n_line)  # 干扰线条数
    for i in range(line_num):
        # 起始点
        begin = (random.randint(0, size[0]), random.randint(0, size[1]))
        # 结束点
        end = (random.randint(0, size[0]), random.randint(0, size[1]))
        draw.line([begin, end], fill=(0, 0, 0))

    # 绘制干扰点
    chance = min(100, max(0, int(2)))  # 大小限制在[0, 100]
    for w in range(width):
        for h in range(height):
            tmp = random.randint(0, 100)
            if tmp > 100 - chance:
                draw.point((w, h), fill=(0, 0, 0))

    # 绘制验证码字符
    string = ' '.join(code)  # 每个字符前后以空格隔开
    font = ImageFont.truetype(FONT_PATH, font_size)
    font_width, font_height = font.getsize(string)
    draw.text(((width - font_width) / 5, (height - font_height) / 4),
              string, font=font, fill=fg_color)

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100, 0, 0, 0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500, 0.001,
              float(random.randint(1, 2)) / 500]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）

    string = ''.join(code).lower()
    return img, string


if __name__ == "__main__":
    img, s = generate_verify_image()
    fp = '../static/img/' + s + '.png'
    img.save(fp, 'png')
    print(s)
