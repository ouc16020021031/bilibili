#####  该项目实现爬取bilibili番剧信息功能 

运行 [openMongo.py](openMongo.py)  开启数据库

直接运行  [main.py](main.py)  开始爬虫

用MongoDB compass打开，connet：http://localhost:27017/

数据存于scrapy_data/bilibili，大于等于2912条

-------------------------------------------------
# 数据可视化部分说明
## 前置条件
- 模块需求：numpy, pymongo, wordcloud, matplotlib, PIL
- 原始数据：mongoDB数据库，运行openMongo.py打开
### 程序功能
- 读取数据库
- 展示番剧集数分布饼状图
- 展示番剧标签词云
- 展示番剧cv词云
- 展示评分最高的若干番剧/展示番剧评分分布饼状图
### 运行说明
- 看程序中文注释即可
### 函数解释
- randomColor：生成绘制饼状图所需的随机颜色块
- drawBar：绘制条状图
    - 输入：标签list，值list，图表名称string
    - 输出：无
- drawPie：绘制饼状图
    - 输入：标签list，值list，图表名称string
    - 输出：无
- readDatabase()：读取数据库
    - 输入：无
    - 输出：番剧更新集数list，番剧名称list，番剧关注人数list，番剧播放量list，番剧评分list，番剧标签list，番剧配音list，番剧点击量list
- indexShowProcess：根据番剧集数绘制饼状图
    - 输入：番剧更新集数list
    - 输出：无
- tagsShowProcess：根据番剧列表绘制词云显示最常见标签
    - 输入：番剧标签list
    - 输出：无
- cvShowProcess：根据番剧cv绘制词云显示最常见cv
    - 输入：番剧配音list
    - 输出：无
- scoreShowProcess：根据番剧评分统计前若干名番剧标签词云显示最常见标签/番剧评分分布饼状图
    - 输入：番剧评分list，番剧名称list，番剧标签list，番剧统计范围
    - 输出：无
