
import scrapy
from itemloaders.processors import MapCompose, TakeFirst



def raw_into_str(raw_data):
    new_data = raw_data.strip('\n ')
    if new_data:
        return new_data


def price_to_digit(raw_price):
    price = raw_price.replace(' ', '')
    if price.isdigit():
        return int(price)
    return price

class ParserlmItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    price = scrapy.Field(output_processor=TakeFirst(),input_processor=MapCompose(price_to_digit))
    link = scrapy.Field(output_processor=TakeFirst())
    specs = scrapy.Field(input_processor=MapCompose(raw_into_str))
    _id = scrapy.Field()