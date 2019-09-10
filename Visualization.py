import collections
import os
import random
import re

import numpy as np
import pymongo
import wordcloud
from matplotlib import pyplot as plt
from PIL import Image


def randomColor(num_colors):
    color_attribute = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A',
        'B', 'C', 'D', 'E', 'F'
    ]
    color_list = []
    for color_iter in range(num_colors):
        color = ""
        for i in range(6):
            color += color_attribute[random.randint(0, 14)]
        color_list.append("#" + color)
    return color_list


def drawBar(label_items, value_items, title_name):
    axis_x = range(len(label_items))
    axis_y = value_items
    color_list = randomColor(len(label_items))
    plt.bar(axis_x, axis_y, color=color_list)
    for label_x, label_y in zip(axis_x, axis_y):
        plt.text(label_x,
                 label_y,
                 value_items[label_x],
                 ha='center',
                 va='bottom')
    plt.xticks(axis_x, label_items)
    plt.title(title_name)
    plt.show()


def drawPie(label_items, value_items, title_name):
    value_items = value_items / np.sum(value_items)
    color_list = randomColor(len(label_items))
    plt.pie(value_items,
            labels=label_items,
            autopct='%1.1f%%',
            colors=color_list,
            startangle=180)
    plt.axis('equal')
    plt.title(title_name)
    plt.show()


def readDatabase():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    datebase = client["scrapy_data"]
    crawl_data = datebase["bilibili"]

    index_show_list = []  # 番剧更新集数
    title_list = []  # 番剧名称
    follow_list = []  # 番剧关注人数
    play_list = []  # 番剧播放量
    score_list = []  # 番剧评分
    tags_list = []  # 番剧标签
    cv_list = []  # 番剧配音
    count_list = []  # 番剧点击量
    select_rules = {
        "_id": 0,
        "index_show": 1,
        "title": 1,
        "follow": 1,
        "play": 1,
        "score": 1,
        "tags": 1,
        "cv": 1,
        "count": 1
    }
    for items in crawl_data.find({}, select_rules):
        index_show_list.append(items["index_show"])
        title_list.append(items["title"])
        follow_list.append(items["follow"])
        play_list.append(items["play"])
        score_list.append(items["score"])
        tags_list.append(items["tags"])
        cv_list.append(items["cv"])
        count_list.append(items["count"])
    return index_show_list, title_list, follow_list, play_list, score_list, tags_list, cv_list, count_list


def indexShowProcess(index_show_list):
    title_name = "番剧集数"
    episode_list = []
    label_list = ["0-10", "10-20", "20-30", "30-40", "40-200", ">200"]
    value_list = [0, 0, 0, 0, 0, 0]
    for index, value in enumerate(index_show_list):
        episode_list.append(re.findall('(\d+)', value))
    for index, value in enumerate(episode_list):
        if not len(value):
            continue
        deci_num = int(value[0]) // 10
        if deci_num < 4:
            value_list[deci_num] += 1
        else:
            if deci_num < 20:
                value_list[4] += 1
            else:
                value_list[-1] += 1
    drawPie(label_list, value_list, title_name)


def tagsShowProcess(tags_list):
    tag_list = []
    for index, value in enumerate(tags_list):
        if not len(value):
            continue
        tag_str_list = value.split()
        for index, value in enumerate(tag_str_list):
            tag_list.append(value)

    word_counts = collections.Counter(tag_list)
    mask = np.array(Image.open(r'C:\Users\30110\Desktop\timg.jpg'))
    word_cloud = wordcloud.WordCloud(font_path='C:/Windows/Fonts/simhei.ttf',
                                     max_words=2000,
                                     max_font_size=200,
                                     background_color='black')
    word_cloud.generate_from_frequencies(word_counts)
    image_colors = wordcloud.ImageColorGenerator(mask)
    word_cloud.recolor(color_func=image_colors)
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()


def cvShowProcess(cv_list):
    cv_name_list = []
    for index, value in enumerate(cv_list):
        if not len(value):
            continue
        cv_index_single = value.split('\\n')
        for index_, value_ in enumerate(cv_index_single):
            temp = value_.split(r'：')
            if len(temp) < 2:
                continue
            if temp[1].find(r'"') != -1:
                temp[1] = temp[1][:-1]
            cv_name_list.append(temp[1])
    word_counts = collections.Counter(cv_name_list)
    word_cloud = wordcloud.WordCloud(font_path='C:/Windows/Fonts/simhei.ttf',
                                     width=1024,
                                     height=768,
                                     max_words=200,
                                     max_font_size=200,
                                     background_color='white')
    word_cloud.generate_from_frequencies(word_counts)
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()


def scoreShowProcess(score_list, title_list, tags_list, show_range):

    for i in range(len(score_list)):
        try:
            score_list[i] = float(score_list[i][:-1])
        except ValueError:
            score_list[i] = -1
    score_list_cp1 = score_list.copy()
    score_list_cp2 = score_list.copy()

    max_score_list = []
    max_score_name = []
    max_score_tags = []
    for i in range(show_range):
        current_max_index = score_list_cp1.index(max(score_list_cp1))
        max_score_list.append(max(score_list_cp1))
        max_score_name.append(title_list[current_max_index])
        max_score_tags.append(tags_list[current_max_index])
        score_list_cp1[current_max_index] = -1
    tagsShowProcess(max_score_tags) 

# 上下两块内容选取一块运行

"""
    score_list_cp2.sort(reverse=True)
    title_name = "番剧评分"
    label_list = [">9.5", "9.0-9.5", "8.0-9.0", "7.0-8.0", "<7.0"]
    value_list = [0, 0, 0, 0, 0]
    for index, value in enumerate(score_list_cp2):
        if value > 9.5:
            value_list[0] += 1
        elif value > 9.0:
            value_list[1] += 1
        elif value > 8.0:
            value_list[2] += 1
        elif value > 7.0:
            value_list[3] += 1
        elif value > 0:
            value_list[4] += 1
        else:
            pass
    drawPie(label_list, value_list, title_name) """


plt.rcParams['font.sans-serif'] = ['SimHei']
index_show_list, title_list, follow_list, play_list, score_list, tags_list, cv_list, count_list = readDatabase(
)

# 以下三条语句选择一条运行
#indexShowProcess(index_show_list)
#tagsShowProcess(tags_list)
#cvShowProcess(cv_list)
#scoreShowProcess(score_list, title_list, tags_list, 200)
