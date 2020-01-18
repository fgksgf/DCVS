from scrapy import cmdline

if __name__ == '__main__':
    cmd = 'scrapy crawl comment_spider'
    cmdline.execute(cmd.split())
