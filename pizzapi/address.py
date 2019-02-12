from .store import Store
from .utils import request_json
from .urls import Urls, COUNTRY_USA

class Address(object):
    """Create an address, for finding stores and placing orders.

    The Address object describes a street address in North America (USA or
    Canada, for now). Callers can use the Address object's methods to find
    the closest or nearby stores from the API.

    Attributes:
        street (String): Street address
        apt_num (String - Optional): Apartment Number
        city (String): North American city
        region (String): North American region (state, province, territory)
        zip (String): North American ZIP code
        urls (String): Country-specific URLs
        country (String): Country
    """

    def __init__(self, street, city, region='', zip='', delivery_instructions='', country=COUNTRY_USA, type='House', apt_num='', *args):
        assert type in ('House', 'Apartment')
        self.street = street.strip()
        self.city = city.strip()
        self.region = region.strip()
        self.zip = str(zip).strip()
        self.urls = Urls(country)
        self.delivery_instructions = delivery_instructions.strip()
        self.country = country
        self.type = type
        self.apt_num = apt_num

    @property
    def data(self):
        resp = {'Street': self.street, 'City': self.city,
                'Region': self.region, 'PostalCode': self.zip,
                'DeliveryInstructions': self.delivery_instructions,
                'Type': self.type}
        if self.type == 'Apartment':
            resp['UnitNumber'] = self.apt_num
            resp['UnitType'] = 'APT'
        return resp

    @property
    def line1(self):
        resp = '{Street}'.format(**self.data)
        if self.type == 'Apartment':
            resp += ' #{UnitNumber}'.format(**self.data)
        return resp

    @property
    def line2(self):
        return '{City}, {Region}, {PostalCode}'.format(**self.data)

    def nearby_stores(self, service='Delivery', show_closed=False):
        """Query the API to find nearby stores.

        nearby_stores will by default filter the information we receive from
        the API to exclude stores that are not currently online
        (!['IsOnlineNow']), and stores that are not currently in service
        (!['ServiceIsOpen']).

        optional show_closed param returns all results, even if not open/ online
        """
        data = request_json(self.urls.find_url(), line1=self.line1, line2=self.line2, type=service)
        if not show_closed:
            return [Store(x, self.country) for x in data['Stores']
                    if x['IsOnlineNow'] and x['ServiceIsOpen'][service]]
        return [Store(x, self.country) for x in data['Stores']]

    def closest_store(self, service='Delivery'):
        stores = self.nearby_stores(service=service)
        if not stores:
            raise Exception('No local stores are currently open')
        return stores[0]
