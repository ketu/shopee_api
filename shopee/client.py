# /usr/bin/env python
# -*- coding:utf8 -*-
import time
import json
import hmac, hashlib
from urllib.parse import urljoin
from requests import Request, Session, exceptions
from .order import Order
from .product import Product
from .item import Item
from .variation import Variation
from .logistic import Logistic
from .rma import RMA
from .category import Category
from .setting import BASE_URL

# installed sub-module
installed_module = {
    "order": Order,
    "product": Product,  # will be removed
    "item": Item,
    "variation": Variation,
    "logistic": Logistic,
    "rma": RMA,
    "category": Category
}


class ClientMeta(type):
    def __new__(mcs, name, bases, dct):
        klass = super().__new__(mcs, name, bases, dct)
        setattr(
            klass, "installed_module",
            installed_module
        )
        return klass


class Client(object, metaclass=ClientMeta):
    __metaclass__ = ClientMeta
    cached_module = {}

    def __init__(self, shop_id: int, partner_id: int, secret_key: str):
        self.shop_id = shop_id
        self.partner_id = partner_id
        self.secret_key = secret_key

    def __getattr__(self, name):
        try:
            value = super(Client, self).__getattribute__(name)
        except AttributeError as e:
            value = self.get_cached_module(name)
            if not value:
                raise e
        return value

    def make_timestamp(self):
        return int(time.time())

    def make_default_parameter(self):
        return {
            "partner_id": self.partner_id,
            "shopid": self.shop_id,
            "timestamp": self.make_timestamp()
        }

    def sign(self, url, body):
        bs = url + "|" + json.dumps(body)
        dig = hmac.new(self.secret_key.encode(), msg=bs.encode(), digestmod=hashlib.sha256).hexdigest()
        return dig

    def build_request(self, uri, method, body):
        method = method.upper()
        url = urljoin(BASE_URL, uri)
        authorization = self.sign(url, body)
        headers = {
            "Authorization": authorization
        }
        req = Request(method, url, headers=headers)

        if body:
            if req.method in ["POST", "PUT", "PATH"]:
                req.json = body
            else:
                req.params = body
        return req

    def execute(self, uri, method, body=None):
        parameter = self.make_default_parameter()

        if body is not None:
            parameter.update(body)

        req = self.build_request(uri, method, parameter)
        prepped = req.prepare()
        s = Session()
        resp = s.send(prepped)
        resp = self.build_response(resp)
        return resp

    def build_response(self, resp):
        try:
            return resp.json()
        except (ValueError, json.JSONDecodeError) as e:
            raise resp.raise_for_status()

    def get_cached_module(self, key):
        cache_key = str(self.partner_id) + key

        cached_module = self.cached_module.get(cache_key)

        if not cached_module:
            installed = self.installed_module.get(key)
            if not installed:
                return None
            cached_module = installed(self)
            self.cached_module.setdefault(cache_key, cached_module)
        return cached_module
