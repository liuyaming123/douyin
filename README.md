# douyin-spider

### 介绍
仓库用于抖音爬虫，根据分享的用户主页链接抓取作者信息和作品列表

### 开发说明
1.	使用抓包软件抓取抖音的请求包，获取作者信息和作品列表的接口信息
2.	分析请求参数并模拟请求参数
3.	使用requests包进行相关请求和响应的处理

### 使用说明

1.  安装依赖：`pip install -r requirements.txt`
2.  运行：python3 douyin.py
3.  根据需要可直接修改douyin.py中的share_url_list参数，该参数为待抓取的用户的主页分享链接列表
