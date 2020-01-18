from pyquery import PyQuery as pq

if __name__ == '__main__':
    d = pq(url='https://item.jd.com/40669500211.html')
    attributes = []
    choices = []
    for i in range(1, 10):
        v = []
        query = '#choose-attr-' + str(i)
        if len(d(query)) != 0:
            attributes.append(d(query).attr('data-type'))
            for div in d(query + ' .item'):
                v.append(pq(div).attr('data-value'))
            choices.append(v)
        else:
            break
    print(attributes)
    print(choices)
