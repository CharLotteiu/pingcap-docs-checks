---
title: Lesson Learned from Queries over 1.3 Trillion Rows of Data Within Milliseconds of Response Time at Zhihu.com
author: ['Xiaoguang Sun']
date: 2019-08-21
summary: As the business boomed and massive data in applications accrued each month, Zhihu faced severe challenges in scaling the backend system. This post introduces how Zhihu managed to keep milliseconds of query response time over a large amount of data and how TiDB, an open source MySQL-compatible HTAP database, empowered Zhihu to get real-time insights into data.
tags: ['Scalability', 'Real-time analytics', 'MySQL']
url: /success-stories/lesson-learned-from-queries-over-1.3-trillion-rows-of-data-within-milliseconds-of-response-time-at-zhihu/
customer: Zhihu
customerCategory: Internet
notShowOnLogoWall: true
aliases: ['/blog/use-case-tidb-in-eleme/', '/case-studies/gaining-3x-throughput-by-migrating-from-aurora-to-a-scale-out-mysql-alternative/', '/case-studies/japan-largest-mobile-payment-company-migrates-from-aurora-to-a-scale-out-database/', '/case-studies/category/company/Paytm-Labs/', '/case-studies/category/company/PayPay/', '/blog/gaining-3x-throughput-by-migrating-from-aurora-to-a-scale-out-mysql-alternative/']
logo: /images/blog/customers/zhihu-logo.png
---

**Industry:** Knowledge Sharing。

**Author:** Xiaoguang Sun (Backend Search Manager at Zhihu, TiKV Project Maintainer)

[Zhihu](https://en.wikipedia.org/wiki/Zhihu), which means "Do you know?" in classical Chinese, is the Quora of China: a question-and-answer website where all kinds of questions are created, answered, edited, and organized by the community of its users. As [China's biggest knowledge sharing platform](https://walkthechat.com/zhihu-chinas-largest-qa-platform-content-marketers-dream/), we currently have 220 million registered users, and 30 million questions with more than 130 million answers on the site. In August 2018, we announced that we had raised [$270 million in series E funding](https://technode.com/2018/08/08/zhihu-series-e-funding/).

As our business boomed, the data size of our applications grew out of hand. About 1.3 trillion rows of data were stored in our Moneta application (which stores posts users have already read). With approximately 100 billion rows of data accruing each month and growing, this number will reach 3 trillion in two years. We faced severe challenges in scaling our backend system while maintaining good user experience！

In this post, I'll dive deep into how we managed to keep milliseconds of query response time over such a large amount of data and how TiDB, an open source MySQL-compatible NewSQL Hybrid Transactional/Analytical Processing ([HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing_(HTAP))) database, empowered us to get real-time insights into our data. I'll introduce why we chose TiDB, how we are using it, what we learned and best practice and some thoughts about the future.

## Our pain points

This section covers the architecture for our Moneta application, and the solution we tried to build an ideal architecture, and reveals that **database scalability** is our major pain point.？

### 「System architecture requirements」

Zhihu's Post Feed service is a crucial system through which users are exposed to content posted on the site. **The Moneta application** in the backend stores the posts users have read, and filters out these posts in the post stream of Zhihu's Recommendations page.

The Moneta application has the following characteristics:

* **Requires high availability for data**. Post Feed is the first screen to appear, and it plays an important role in driving user traffic to Zhihu.
* **Handles immense write data**. For example, more than 40 thousand records are written per second at peak time, and the number of records grows by nearly 3 billion records every day.
* **Stores historical data for a long time**. Currently, about 1.3 trillion records are stored in the system. With approximately 100 billion records accruing each month and growing, historical data will reach 3 trillion records in about two years.
* **Tackles high-throughput queries**. At peak time, the system processes queries that are performed on 12 million posts on average per second.
* **Limits the response time for queries to 90 ms or less**. This occurs even for a long-tail query which takes the longest time to execute.
* **Tolerates false positives**. This means that the system can recall many interesting posts for users, even when some posts have been filtered out by mistake.

Considering the facts above, we need an application architecture with the following features:

* **High availability**. It's a bad user experience to find lots of already-read posts when a user opens Zhihu's Recommendations page.
* **Excellent system performance**. Our application has high throughput and strict requirements for response time.
* **Easy to scale out**. As our business develops and our application evolves, we hope our system can easily scale out.

### Exploration

To build an ideal architecture with the features above, we incorporated three key components in our previous architecture:

* Proxy. This forwards users' requests to available nodes, and ensures the high availability of the system.
* Cache. This temporarily deals with requests in memory, so we don't always need to process requests in the database. This improves system performance.
* Storage. Before using TiDB, we managed our business data on standalone MySQL. As data volume surged, the standalone MySQL system wasn't enough. Then we adopted the solution of MySQL sharding and Master High Availability Manager ([MHA](https://github.com/yoshinorim/mha4mysql-manager)), but this solution was undesirable when 100 billion new records flooded into our database each month.

### Shortcomings of MySQL sharding and MHA

MySQL sharding and MHA is not a good solution, because both MySQL sharding and MHA have their shortcomings.

#### Shortcomings of MySQL sharding

* The application code becomes complicated and difficult to maintain.
* It is troublesome to change the existing sharding key.
* Upgrading the application logic affects application usability.

#### Shortcomings of MHA

* We need to implement the virtual IP (VIP) configuration by writing a script or utilizing a third-party tool.
* MHA only monitors the primary database.
* To configure MHA, we need to configure passwordless Secure Shell ([SSH](https://en.wikipedia.org/wiki/Secure_Shell)). This may lead to potential security risks.
* MHA doesn't provide the read load balancing feature for the secondary server.
* MHA can only monitor whether the primary server (instead of the secondary primary) is available.

Database scalability was still the weak point of the overall system until we found TiDB and migrated data from MySQL to TiDB.

## What is TiDB?

The TiDB platform is a collection of components that when used together become a NewSQL database with HTAP capabilities.

![TiDB platform architecture](media/tidb-platform-architecture.png)
<div class="caption-center"> TiDB platform architecture </div>

Before we tried TiDB, we didn't analyze how many hardware resources we would need to support the same amount of data we had on the MySQL side. To reduce maintenance costs, we deployed MySQL in the single primary — single secondary topology. In contrast, the [Raft](https://raft.github.io/) protocol implemented in TiDB requires at least three replicas. Therefore, we needed more hardware resources to support our business data in TiDB, and we needed to prepare machine resources in advance.
