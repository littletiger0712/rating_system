# rating_system
移动应用安全隐私评级模型

主要思想：利用应用商店的用户评论预测此app是否存在安全隐私风险。设置五个标签：系统问题；盗取隐私；垃圾广告；恶意扣费；病毒木马。
将问题作为五个独立的二分类问题来解决。

### 模型建设步骤：

1.数据获取：利用数据采集框架Scrapy爬取小米应用商店的40w条用户评论并标记。

2.数据格式设置：利用jieba分词，去除停用词。

3.特征提取：利用词袋模型构造特征向量，并利用tf-idf加权。

4.特征选择：利用基于决策树的特征选择方法，去除冗余特征。

5.数据不均衡的处理：采用smote过采样算法，对少数类进行扩增。

6.分类器构造：利用AdaBoost分类器，五个分类器都达到95%以上的正确率。其中：系统问题：90.03%；盗取隐私：92.78%；垃圾广告：96.98%；恶意扣费：93.44%；病毒密码：82.08%

7.系统实现：利用flask框架构造web应用实现安全评级系统。系统原理为：输入app id，
