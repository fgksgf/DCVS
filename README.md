# JD Distributed Crawler and Visualization System

The JD Distributed Crawler and Visualization System (JD-DCVS) is the graduation project of my undergraduate. 

It can crawl comments of given [JD](www.jd.com) goods' url. After that, users can visualize and analyze the data by several statistics charts, such as pie charts, line charts and wordcloud charts, which can help users judge whether the goods are good.

## Features

+   **Distributed architecture design**. By sharing the crawl queue, distributed crawlers can dynamically add nodes at any time without downtime, which is extremely scalable. 
+   **Anti-anti-crawler measures**. In order to enable the crawler to cope with common anti-crawler measures, I also designed and implemented an [IP proxy pool](https://github.com/fgksgf/IP-Proxy-Pool) to provide a large number of highly anonymous IP proxies. 
+   **NoSQL storage**. In the case of crawler high concurrent processing, the system uses non-relational database (NoSQL) to store data to improve the efficiency of reading and writing data. 
+   **Node management**. The Gerapy framework provides users with a graphical interface to easily manage and deploy crawler nodes. 
+   **Data visualization**. Use the Pyecharts library to quickly generate crawl data into simple, beautiful, interactive statistical charts.

## Architecture

There are four main modules in the system: 

1.  Distributed crawler module. The code of all crawler nodes is the same and all URLs to be requested are obtained from the same queue. In this way, if the scale of the crawled data is expanded, only the crawler nodes need to be added to meet the demand, which has extremely high scalability.
2.  IP proxy pool module. An IP proxy pool module is designed as an independent node. It contains three sub-modules: proxy getter, proxy tester, and interface module. 
3.  Data storage module. MongoDB is responsible for storing the semi-structured data crawled by the crawler, and Redis is responsible for storing the URL to be crawled and proxy information. 
4.  Web application module. It mainly contains four sub-modules: node management, data processing, data visualization, and adding tasks. The module also acts as an independent node.

![](./static/img/dcvs-1.jpg)