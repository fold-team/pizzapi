from .menu import Menu
from .proxy import ProxyMeta
from .urls import Urls, COUNTRY_USA
from .utils import request_json


class Store(metaclass=ProxyMeta):
    """The interface to the Store API

    You can use this to find store information about stores near an
    address, or to find the closest store to an address. 
    """
    def __init__(self, data={}, country=COUNTRY_USA):
        self.id = str(data.get('StoreID', -1))
        self.country = country
        self.urls = Urls(country)
        self.data = data

    def get_details(self):
        details = request_json(self.urls.info_url(), store_id=self.id, proxies=self.proxies)
        return details

    def get_menu(self, lang='en'):
        response = request_json(self.urls.menu_url(), store_id=self.id, lang=lang, proxies=self.proxies)
        menu = Menu(response, self.country, proxies=self.proxies)
        return menu
