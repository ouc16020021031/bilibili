import scrapy
import logging
from scrapy import Request
from bilibili.items import BilibiliItem
import re
import json
class MySpider(scrapy.Spider):
    name = 'bilibili'
    allowed_domains = ['bilibili.com']
    url_head = 'https://bangumi.bilibili.com/media/web_api/search/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&pub_date=-1&style_id=-1&order=3&st=1&sort=0&season_type=1'
    start_urls = [url_head+"&page=1"]

    # 先处理列表中的番剧信息
    def parse(self, response):
        self.log('Main page %s' % response.url,level=logging.INFO)
        data=json.loads(response.text)
        next_index=int(response.url[response.url.rfind("=")-len(response.url)+1:])+1
        if(len(data['result']['data'])>0):
            # 发出Request 处理下一个网址
            next_url = self.url_head+"&page="+str(next_index)
            yield Request(next_url, callback=self.parse)
            medias=data['result']['data']
            for m in medias:
                media_id=m['media_id']
                detail_url='https://www.bilibili.com/bangumi/media/md'+str(media_id)
                yield Request(detail_url,callback=self.parse_detail,meta=m)
    # 再处理每个番剧的详细信息
    def parse_detail(self, response):
        item = BilibiliItem()
        item_brief_list=['badge','badge_type','is_finish','media_id','index_show','season_id','title']
        item_order_list=['follow','play','pub_date','pub_real_time','renewal_time','score']
        m=response.meta
        for key in item_brief_list:
            if (key in m):
                item[key]=m[key]
            else:
                item[key]=""
        for key in item_order_list:
            if (key in m['order']):
                item[key]=m['order'][key]
            else:
                item[key]=""
        tags=response.xpath('//*[@class="media-tag"]/text()').extract()
        tags_string=''
        for t in tags:
            tags_string=tags_string+" "+t
        item['tags']=tags_string
        item['brief'] = response.xpath('//*[@name="description"]/attribute::content').extract()
        detail_text = response.xpath('//script')[4].extract()
        actor_p = re.compile('actors":(.*?),')
        ratings_count_p = re.compile('count":(.*?),')
        staff_p = re.compile('staff":(.*?),')
        item['cv'] = re.findall(actor_p,detail_text)[0]
        item['staff'] = re.findall(staff_p,detail_text)[0]
        count_list=re.findall(ratings_count_p,detail_text)
        if(len(count_list)>0):
            item['count'] = count_list[0]
        else:
            item['count']=0
#        self.log(item)
        return item