import json
import time
from datetime import datetime


def all_price(price, start_time, end_time):
    price: dict = json.loads(price)
    start_time: datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time: datetime = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    hour = start_time.hour
    minute = start_time.minute
    second = start_time.second
    end_hour = end_time.hour
    end_minute = end_time.minute
    end_second = end_time.second
    item_price = price.get(str(hour))
    end_item_price = price.get(str(end_hour))
    start_price = item_price * (((24 - hour) * 3600 - minute * 60 - second) / (24 * 3600))
    end_price = end_item_price * ((end_minute * 60 + end_second) / (24 * 3600))
    middle_price = 0
    if start_time.day != end_time.day:
        end_hour += 24
    for i in range(hour + 1, end_hour):
        if i >= 24:
            i -= 24
        print(i)
        middle_price += price.get(str(i))
    return format(start_price + middle_price + end_price, '.4f')