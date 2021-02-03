import cfscrape
import time
import json
from random import uniform


# This file implements the scrapping process from website https://www.autotrader.co.uk/car-reviews
def multi_decoder(s: bytes) -> str:
    """
    :param s: bytes-format to be decoded with
    :return: decoded string
    """
    try:
        ds = str(s, 'utf_8_sig')
    except UnicodeDecodeError:
        try:
            ds = str(s, 'gbk')
        except UnicodeDecodeError:
            try:
                ds = str(s, 'GB18030')
            except UnicodeDecodeError:
                ds = str(s, 'gb2312', 'ignore')
    return ds


def fac(n):
    if n <= 1:
        return 1
    else:
        rest = fac(n-1)
        return n*rest


class WEB(object):
    def __init__(self):
        self.s = cfscrape.create_scraper()
        print('Web scrapping core initialized.')

    def get_car_brand(self) -> list:
        url = 'https://www.autotrader.co.uk/json/owner-reviews/results-page-data?channel=cars'
        rsp = self.s.get(url)
        text = multi_decoder(rsp.content)
        d = json.loads(text)
        brand_info = d['selectOptions']['makes']
        id_2_brand = [(x['label'], x['value']) for x in brand_info]
        return id_2_brand

    def get_car_model(self,
                      brand_info: list) -> dict:
        """
        :param brand_info: brand info of cars on website
        :return: specific models from each brand, dictionary format
        """
        brand_model = {}
        for brand, id in brand_info:
            print('Currently processing brand {}'.format(brand))
            url = 'https://www.autotrader.co.uk/json/vds/select-options?vehicleType=Car&channel=cars&make={}'
            url = url.format(id)
            rsp = self.s.get(url)
            time.sleep(uniform(1, 2))
            text = multi_decoder(rsp.content)
            d = json.loads(text)
            brand_model[(brand, id)] = dict([((x['label'], x['value']), []) for x in d['models']])
        return brand_model

    def get_car_review(self,
                       brand_model_info: dict) -> dict:
        """
        :param brand_model_info: car brand - car model dictionary, refer to return from self.get_car_model
        :return: fetched review under car brand - car model - model generation - reviews, dictionary format
        """
        for brand, brand_id in brand_model_info:
            for model, model_id in brand_model_info[(brand, brand_id)]:
                print('Currently executing model: {} from car brand: {}'.format(model, brand))
                url = 'https://www.autotrader.co.uk/json/vds/select-options?vehicleType=Car&channel=cars&make={}&model={}'
                url = url.format(brand_id, model_id)
                rsp = self.s.get(url)
                time.sleep(uniform(1, 2)) if uniform(0, 1) > 0.14 else time.sleep(uniform(9, 10))
                text = multi_decoder(rsp.content)
                d = json.loads(text)
                gen_info = dict([((x['label'], x['value']), []) for x in d['generations']])
                for gen, gen_id in gen_info:
                    p = 0
                    while True:
                        url = 'https://www.autotrader.co.uk/json/owner-reviews?generation={}&page={}'.format(gen_id, p)
                        rsp = self.s.get(url)
                        time.sleep(uniform(1, 2)) if uniform(0, 1) > 0.1 else time.sleep(uniform(5, 8))
                        text = multi_decoder(rsp.content)
                        d = json.loads(text)
                        if not d['reviews']:
                            if not p:
                                gen_info[(gen, gen_id)] = []
                            break
                        gen_info[(gen, gen_id)] += d['reviews']
                        p += 1
                brand_model_info[(brand, brand_id)][(model, model_id)] = gen_info
        return brand_model_info


