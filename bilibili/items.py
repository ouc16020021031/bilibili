# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliItem(scrapy.Item):
    # define the fields for your item here like:
    badge= scrapy.Field()
    badge_type= scrapy.Field()
    is_finish= scrapy.Field()
    media_id= scrapy.Field()
    index_show= scrapy.Field()
    follow= scrapy.Field()
    play= scrapy.Field()
    pub_date= scrapy.Field()
    pub_real_time= scrapy.Field()
    renewal_time= scrapy.Field()
    score= scrapy.Field()
    season_id= scrapy.Field()
    title = scrapy.Field()
    tags= scrapy.Field()
    brief= scrapy.Field()
    cv= scrapy.Field()
    staff= scrapy.Field()
    count= scrapy.Field()

    pass